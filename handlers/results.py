"""
Natijalar (Results) handleri
"""
from aiogram import Router, F
from aiogram.types import Message, InputMediaPhoto
from database import Database
from services import ConfigCache

router = Router()


@router.message(F.text == "🏆 Natijalar")
@router.message(F.text.in_({"💸 Sovrindorlar 🏆", "🏆 G'oliblar"}))
async def show_results(message: Message):
    """Konkurs natijalarini va yutuqlarni ko'rsatish"""
    
    # 1. Admin saqlagan maxsus postni tekshirish
    saved_text = await Database.get_setting("winners_text")
    saved_photo_str = await Database.get_setting("winners_photo")
    
    # Agar admin post saqlagan bo'lsa, o'shani chiqaramiz
    if saved_text or (saved_photo_str and saved_photo_str != "none"):
        # Rasmlar ro'yxatini olish
        if saved_photo_str and saved_photo_str != "none":
            photo_ids = saved_photo_str.split(",")
            
            if len(photo_ids) > 1:
                # Albom ko'rsatish
                media = []
                for i, pid in enumerate(photo_ids):
                    if i == 0:
                        media.append(InputMediaPhoto(media=pid, caption=saved_text))
                    else:
                        media.append(InputMediaPhoto(media=pid))
                await message.answer_media_group(media=media)
            else:
                # Bitta rasm
                await message.answer_photo(photo=photo_ids[0], caption=saved_text)
        else:
            # Faqat matn
            await message.answer(saved_text)
        return

    # 2. Agar post bo'lmasa, eski usul (dinamik ro'yxat)
    
    # G'oliblar (avval ko'rsatamiz - muhimroq)
    winners = await Database.get_winners()
    
    # Leaderboard (TOP 10)
    leaderboard = await Database.get_leaderboard(limit=10)
    
    # Sarlavha
    text = "<b>💸 SOVRINDORLAR 🏆</b>\n\n"
    text += "<i>Qarang, ishtirokchilarimiz yutuqlari!</i>\n\n"
    
    # G'oliblar e'loni (avval)
    if winners:
        text += "<b>🎁 SOVRIN G'OLIBLARI:</b>\n\n"
        for winner in winners:
            rank = winner['rank']
            user_id = winner['user_id']
            prize = winner['prize']
            
            # Rank emoji
            rank_emoji = {"1": "🥇", "2": "🥈", "3": "🥉"}.get(str(rank), f"{rank}.")
            
            # Username yoki ID (database'dan olish)
            user = await Database.get_user(user_id)
            username = f"@{user['username']}" if user and user.get('username') else f"ID: {user_id}"
            
            text += f"{rank_emoji} {username}\n"
            text += f"💰 <b>Sovrin:</b> {prize}\n\n"
    else:
        text += "<i>G'oliblar hali e'lon qilinmagan.</i>\n\n"
    
    # Leaderboard matni
    text += "<b>📊 TOP 10 Ishtirokchilar:</b>\n"
    
    if leaderboard:
        for idx, user in enumerate(leaderboard, start=1):
            username = f"@{user.get('username')}" if user.get('username') else f"ID: {user['user_id']}"
            count = user.get('invited_count', 0)
            
            # Medal emoji
            medal = ""
            if idx == 1: medal = "🥇"
            elif idx == 2: medal = "🥈"
            elif idx == 3: medal = "🥉"
            else: medal = f"{idx}."
            
            text += f"{medal} {username} - <b>{count}</b> ta referal\n"
    else:
        text += "Hali ma'lumot yo'q.\n"
    
    await message.answer(text, parse_mode="HTML")
