"""
Natijalar (Results) handleri
"""
from aiogram import Router, F
from aiogram.types import Message
from database import Database
from services import ConfigCache

router = Router()


@router.message(F.text == "🏆 Natijalar")
@router.message(F.text == "💸 Sovrindorlar 🏆")
async def show_results(message: Message):
    """Konkurs natijalarini va yutuqlarni ko'rsatish"""
    # 1. G'oliblar (avval ko'rsatamiz - muhimroq)
    winners = await Database.get_winners()
    
    # 2. Leaderboard (TOP 10)
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
            proof_id = winner.get('proof_image_id')
            
            # Rank emoji
            rank_emoji = {"1": "🥇", "2": "🥈", "3": "🥉"}.get(str(rank), f"{rank}.")
            
            # Username yoki ID (database'dan olish)
            user = await Database.get_user(user_id)
            if user and user.get('username'):
                username = f"@{user['username']}"
            else:
                username = f"ID: {user_id}"
            
            text += f"{rank_emoji} <b>{rank}-o'rin:</b> {username}\n"
            text += f"💰 <b>Sovrin:</b> {prize}\n\n"
            
            # To'lov isboti
            if proof_id:
                # Rasmni alohida yuborish
                try:
                    await message.answer_photo(
                        photo=proof_id,
                        caption=f"{rank_emoji} <b>{rank}-o'rin g'olibi</b>\n💰 <b>Sovrin:</b> {prize}\n\n✅ <b>To'lov isboti</b>"
                    )
                except:
                    pass
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
