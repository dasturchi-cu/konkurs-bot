from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio
from config import ADMIN_ID, ADMIN_GROUP_ID
from database import Database
from services import ConfigCache

router = Router()

def is_admin(user_id: int) -> bool:
    """Foydalanuvchi admin ekanligini tekshirish"""
    return user_id == ADMIN_ID


@router.message(Command("admin"))
async def admin_help(message: Message):
    """Admin panel yo'riqnomasi"""
    if not is_admin(message.from_user.id):
        return

    text = """👨‍💼 <b>Admin Panel Buyruqlari:</b>

⚙️ <b>Sozlamalar:</b>
/set_limit [son] - Referal limitini o'zgartirish (Hozir: {limit})
/set_link [url] - Yopiq guruh linkini o'zgartirish
/set_video [file_id] - Promo video ID sini o'zgartirish
/set_message [yangi_matn] - Referal matnini o'zgartirish

📢 <b>Kanallar (Sponsorlar):</b>
/channels - Kanallar ro'yxati
/add_channel [nomi]|[url] - Yangi kanal qo'shish
/del_channel [id] - Kanalni o'chirish (ID bo'yicha)

📊 <b>Statistika:</b>
/stats - Bot statistikasi
/leaderboard - TOP 10 ishtirokchilar

💸 <b>G'oliblar va Yutuqlar:</b>
/set_winner [rank] [user_id] [sovrin] - G'olibni belgilash
Masalan: /set_winner 1 123456 "100,000 so'm"

📸 <b>To'lov Isboti Yuklash:</b>
1-usul: Rasm yuborib, captionida /proof [rank] yozing
2-usul: Rasmga reply qilib /proof [rank] yozing
Masalan: /proof 1

📨 <b>Xabar yuborish:</b>
/send - Admin guruhidan reply qilingan xabarni hammaga yuborish

💡 <b>Eslatma:</b> G'oliblarni belgilaganingizdan keyin, to'lov isbotini yuklang. 
Bu ishonchni 2x ga oshiradi va foydalanuvchilar yutuqlarni ko'rishadi!
""".format(limit=ConfigCache.get_limit())

    await message.answer(text)


@router.message(Command("stats"))
async def show_stats(message: Message):
    """Statistika"""
    if not is_admin(message.from_user.id):
        return
        
    stats = await Database.get_stats()
    text = f"""📊 <b>Bot Statistikasi:</b>

👥 Jami foydalanuvchilar: {stats.get('total_users', 0)}
✅ Shartni bajarganlar: {stats.get('completed_users', 0)}
🔗 Referal orqali kelganlar: {stats.get('referral_users', 0)}

⚙️ Limit: {ConfigCache.get_limit()}
📢 Kanallar soni: {len(ConfigCache.get_channels())}
"""
    await message.answer(text)


@router.message(Command("set_limit"))
async def set_limit_handler(message: Message):
    if not is_admin(message.from_user.id): return
    
    try:
        limit = int(message.text.split()[1])
        if await Database.update_setting("referral_limit", str(limit)):
            await ConfigCache.refresh_settings()
            await message.answer(f"✅ Limit {limit} ga o'zgartirildi!")
        else:
            await message.answer("❌ Bazaga yozishda xatolik!")
    except:
        await message.answer("⚠️ Xato! Ishlatish: /set_limit 15")


@router.message(Command("set_link"))
async def set_link_handler(message: Message):
    if not is_admin(message.from_user.id): return
    
    try:
        link = message.text.split(maxsplit=1)[1]
        if await Database.update_setting("closed_group_link", link):
            await ConfigCache.refresh_settings()
            await message.answer(f"✅ Link o'zgartirildi!")
        else:
            await message.answer("❌ Bazaga yozishda xatolik!")
    except:
        await message.answer("⚠️ Xato! Ishlatish: /set_link https://t.me/...")


@router.message(Command("set_message"))
async def set_message_handler(message: Message):
    if not is_admin(message.from_user.id): return
    
    try:
        new_text = message.text.split(maxsplit=1)[1]
        if await Database.update_setting("referral_message", new_text):
            await ConfigCache.refresh_settings()
            await message.answer(f"✅ Referal matni o'zgartirildi!")
        else:
            await message.answer("❌ Bazaga yozishda xatolik!")
    except:
        await message.answer("⚠️ Xato! Ishlatish: /set_message YANGI_MATN")


@router.message(Command("channels"))
async def list_channels(message: Message):
    if not is_admin(message.from_user.id): return
    
    channels = ConfigCache.get_channels()
    if not channels:
        await message.answer("📢 Kanallar ro'yxati bo'sh.")
        return
        
    text = "📢 <b>Majburiy Kanallar:</b>\n\n"
    for ch in channels:
        text += f"ID: {ch.get('id', '?')} | <a href='{ch['url']}'>{ch['name']}</a>\n"
    
    text += "\nO'chirish uchun: /del_channel [ID]"
    await message.answer(text, disable_web_page_preview=True)


@router.message(Command("add_channel"))
async def add_channel_handler(message: Message):
    if not is_admin(message.from_user.id): return
    
    try:
        # Format: /add_channel Nom|Url
        args = message.text.split(maxsplit=1)[1]
        name, url = args.split("|")
        name = name.strip()
        url = url.strip()
        
        username = url.split("/")[-1] # Taxminiy username
        
        if await Database.add_channel(name, url, username):
            await ConfigCache.refresh_settings()
            await message.answer(f"✅ Kanal qo'shildi: {name}")
        else:
            await message.answer("❌ Xatolik!")
    except:
        await message.answer("⚠️ Xato! Ishlatish: /add_channel Nomi|URL\nMasalan: /add_channel Mening Kanalim|https://t.me/kanal")


@router.message(Command("del_channel"))
async def del_channel_handler(message: Message):
    if not is_admin(message.from_user.id): return
    
    try:
        ch_id = int(message.text.split()[1])
        if await Database.delete_channel(ch_id):
            await ConfigCache.refresh_settings()
            await message.answer(f"✅ Kanal (ID: {ch_id}) o'chirildi.")
        else:
            await message.answer("❌ Xatolik yoki kanal topilmadi.")
    except:
        await message.answer("⚠️ Xato! Ishlatish: /del_channel ID")


@router.message(Command("send"))
async def broadcast_msg(message: Message):
    """Xabar tarqatish (faqat Admin guruhidan reply qilinganda)"""
    if message.chat.id != ADMIN_GROUP_ID:
        return

    if not message.reply_to_message:
        await message.answer("⚠️ Xabar yuborish uchun birorta xabarga reply qilib /send deb yozing.")
        return

    source_msg = message.reply_to_message
    users = await Database.get_all_users()
    count = 0
    
    status_msg = await message.answer("🚀 Xabar yuborish boshlandi...")

    for user in users:
        try:
            await source_msg.copy_to(chat_id=user["user_id"])
            count += 1
            await asyncio.sleep(0.05) # Flood wait oldini olish
        except Exception as e:
            pass # Bloklagan userlar
            
    await status_msg.edit_text(f"✅ Xabar {count} ta foydalanuvchiga yuborildi.")


@router.message(Command("leaderboard"))
async def show_leaderboard(message: Message):
    """TOP 10 ishtirokchilarni ko'rsatish (Admin uchun)"""
    if not is_admin(message.from_user.id): return
    
    leaderboard = await Database.get_leaderboard(limit=10)
    
    if not leaderboard:
        await message.answer("Hali ishtirokchilar yo'q.")
        return
    
    text = "<b>🏆 TOP 10 Ishtirokchilar:</b>\n\n"
    for idx, user in enumerate(leaderboard, start=1):
        username = f"@{user.get('username')}" if user.get('username') else f"ID: <code>{user['user_id']}</code>"
        count = user.get('invited_count', 0)
        user_id = user['user_id']
        
        medal = ""
        if idx == 1: medal = "🥇"
        elif idx == 2: medal = "🥈"
        elif idx == 3: medal = "🥉"
        else: medal = f"{idx}."
        
        text += f"{medal} {username} - <b>{count}</b> ta (ID: {user_id})\n"
    
    await message.answer(text)

# State
class SetWinnerState(StatesGroup):
    waiting_for_post = State()

# Albomlarni vaqtincha saqlash uchun
ALBUM_CACHE = {}

@router.message(Command("set_winner"))
async def set_winner_start(message: Message, state: FSMContext):
    """G'oliblarni belgilash jarayonini boshlash"""
    if not is_admin(message.from_user.id): return
    
    # 1. Agar reply qilingan bo'lsa, o'shani birdaniga qabul qilamiz
    if message.reply_to_message:
        # Reply qilingan xabarni process funksiyasiga uzatamiz
        # Sun'iy ravishda state.set_state chaqirmasdan to'g'ridan-to'g'ri chaqiramiz
        # Lekin process_winner_post state kutadi, shuning uchun biroz boshqacha yondashamiz:
        
        # State o'rnatamiz
        await state.set_state(SetWinnerState.waiting_for_post)
        
        # Reply qilingan xabarni "yangi xabar" sifatida process funksiyasiga beramiz
        await process_winner_post(message.reply_to_message, state)
        return

    # 2. Agar reply bo'lmasa, postni kutamiz
    await message.answer("📸 Iltimos, g'oliblar postini yuboring (Rasm, Matn yoki Albom).\n\n⚠️ Bu post saqlanadi va TOP 3 ta g'olibga yuboriladi.")
    await state.set_state(SetWinnerState.waiting_for_post)


async def process_album_after_delay(first_message: Message, state: FSMContext, media_group_id: str):
    """Albomni 3 soniya kutib, barcha rasmlar yig'ilgach qayta ishlash"""
    await asyncio.sleep(3)
    
    album_data = ALBUM_CACHE.pop(media_group_id, None)
    if not album_data or album_data.get("processed"):
        return
    
    album_data["processed"] = True
    messages = album_data["messages"]
    caption = album_data["caption"]
    
    # Rasmlarni yig'ish
    photo_ids = []
    for msg in messages:
        if msg.photo:
            photo_ids.append(msg.photo[-1].file_id)
        if msg.caption and not caption:
            caption = msg.caption
    
    if not photo_ids:
        await first_message.answer("❌ Albomda rasm topilmadi!")
        await state.clear()
        return
    
    # Bazaga saqlash
    photos_str = ",".join(photo_ids)
    await Database.update_setting("winners_photo", photos_str)
    await Database.update_setting("winners_text", caption or "")
    
    # G'oliblarga yuborish
    await send_to_winners(first_message.bot, photo_ids, caption)
    
    await first_message.answer(f"✅ Albom ({len(photo_ids)} ta rasm) saqlandi va g'oliblarga yuborildi!\n\n📋 Debug: Yig'ilgan xabarlar: {len(messages)}")
    await state.clear()

@router.message(SetWinnerState.waiting_for_post)
async def process_winner_post(message: Message, state: FSMContext):
    """Postni qabul qilish va qayta ishlash"""
    
    # Albom (MediaGroup) tekshiruvi
    media_group_id = message.media_group_id
    
    if media_group_id:
        # Agar bu albomning bir qismi bo'lsa
        if media_group_id not in ALBUM_CACHE:
            ALBUM_CACHE[media_group_id] = {
                "messages": [],
                "caption": None,
                "processed": False
            }
            # Background task yaratamiz - 3 soniyadan keyin process qilish uchun
            asyncio.create_task(process_album_after_delay(message, state, media_group_id))
        
        # Xabarni cache ga qo'shamiz
        ALBUM_CACHE[media_group_id]["messages"].append(message)
        if message.caption and not ALBUM_CACHE[media_group_id]["caption"]:
            ALBUM_CACHE[media_group_id]["caption"] = message.caption
        return

    else:
        # Oddiy xabar (bitta rasm yoki matn)
        caption = message.caption or message.text or ""
        photo_id = message.photo[-1].file_id if message.photo else "none"
        
        await Database.update_setting("winners_text", caption)
        await Database.update_setting("winners_photo", photo_id)
        
        # G'oliblarga yuborish
        photo_ids = [photo_id] if photo_id != "none" else []
        await send_to_winners(message.bot, photo_ids, caption)
        
        await message.answer("✅ Post saqlandi va g'oliblarga yuborildi!")
        await state.clear()


async def send_to_winners(bot, photo_ids: list, caption: str):
    """G'oliblarga xabar yuborish funksiyasi"""
    top_users = await Database.get_leaderboard(limit=3)
    
    if not top_users:
        return
    
    for idx, user in enumerate(top_users, start=1):
        user_id = user['user_id']
        try:
            user_caption = f"🎉 <b>TABRIKLAYMIZ!</b>\n\n🏆 Siz konkursimizda <b>{idx}-o'rinni</b> egalladingiz!\n\nAdmin tez orada bog'lanadi."
            if caption:
                user_caption += f"\n\n{caption}"
                
            if photo_ids:
                if len(photo_ids) > 1:
                    # Albom yuborish
                    media = []
                    for i, pid in enumerate(photo_ids):
                        if i == 0:
                            media.append(InputMediaPhoto(media=pid, caption=user_caption))
                        else:
                            media.append(InputMediaPhoto(media=pid))
                    await bot.send_media_group(user_id, media=media)
                else:
                    # Bitta rasm
                    await bot.send_photo(user_id, photo_ids[0], caption=user_caption)
            else:
                # Faqat matn
                await bot.send_message(user_id, user_caption)
                
            # Bazaga belgilash
            await Database.set_winner(idx, user_id, f"{idx}-o'rin (Avto)")
            
        except Exception:
            pass


@router.message(F.photo)
async def handle_photo_with_caption(message: Message):
    """Rasm captionida /proof bor-yo'qligini tekshirish"""
    if not is_admin(message.from_user.id): return
    
    if message.caption and message.caption.startswith("/proof"):
        try:
            rank = int(message.caption.split()[1]) if len(message.caption.split()) > 1 else 1
            photo_id = message.photo[-1].file_id
            
            if await Database.upload_proof(rank, photo_id):
                await message.answer(f"✅ {rank}-o'rin uchun to'lov isboti yuklandi!")
            else:
                await message.answer("❌ Xatolik! Avval g'olibni belgilaganingizga ishonch hosil qiling.")
        except Exception as e:
            await message.answer(f"⚠️ Xato: {e}")


@router.message(Command("proof"))
async def upload_proof_command(message: Message):
    """To'lov isbotini yuklash (reply usuli)"""
    if not is_admin(message.from_user.id): return
    
    # Rasmga reply qilgan holda
    if message.reply_to_message and message.reply_to_message.photo:
        try:
            rank = int(message.text.split()[1]) if len(message.text.split()) > 1 else 1
            photo_id = message.reply_to_message.photo[-1].file_id
            
            if await Database.upload_proof(rank, photo_id):
                await message.answer(f"✅ {rank}-o'rin uchun to'lov isboti yuklandi!")
            else:
                await message.answer("❌ Xatolik! Avval g'olibni belgilaganingizga ishonch hosil qiling.")
        except Exception as e:
            await message.answer(f"⚠️ Xato: {e}")
    else:
        await message.answer("⚠️ 2 usul:\n1. Rasm yuborib captionida /proof [rank]\n2. Rasmga reply qilib /proof [rank]")

