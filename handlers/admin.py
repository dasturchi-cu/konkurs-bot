from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
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


@router.message(Command("set_winner"))
async def set_winner_handler(message: Message):
    """G'olibni belgilash"""
    if not is_admin(message.from_user.id): return
    
    try:
        # Format: /set_winner 1 123456 "100,000 so'm"
        parts = message.text.split(maxsplit=3)
        rank = int(parts[1])
        user_id = int(parts[2])
        prize = parts[3].strip('"')
        
        if await Database.set_winner(rank, user_id, prize):
            await message.answer(f"✅ {rank}-o'rin g'olibi belgilandi!\nID: {user_id}\nSovrin: {prize}")
        else:
            await message.answer("❌ Xatolik!")
    except Exception as e:
        await message.answer(f"⚠️ Xato! Ishlatish:\n/set_winner [rank] [user_id] [sovrin]\nMasalan: /set_winner 1 123456 \"100,000 so'm\"\n\nXato: {e}")


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

