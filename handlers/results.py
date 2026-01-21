"""
Natijalar (Results) handleri
"""
from aiogram import Router, F
from aiogram.types import Message
from database import Database
from services import ConfigCache

router = Router()


@router.message(F.text == "🏆 Natijalar")
async def show_results(message: Message):
    """Konkurs natijalarini ko'rsatish"""
    # 1. Leaderboard (TOP 10)
    leaderboard = await Database.get_leaderboard(limit=10)
    
    # 2. G'oliblar
    winners = await Database.get_winners()
    
    # Leaderboard matni
    text = "<b>🏆 KONKURS NATIJALARI</b>\n\n"
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
    
    # G'oliblar e'loni
    if winners:
        text += "\n\n<b>🎁 SOVRIN G'OLIBLARI:</b>\n"
        for winner in winners:
            rank = winner['rank']
            user_id = winner['user_id']
            prize = winner['prize']
            proof_id = winner.get('proof_image_id')
            
            # Rank emoji
            rank_emoji = {"1": "🥇", "2": "🥈", "3": "🥉"}.get(str(rank), f"{rank}.")
            
            text += f"\n{rank_emoji} <b>{rank}-o'rin:</b> {prize}\n"
            
            # To'lov isboti
            if proof_id:
                # Rasmni yuborish
                try:
                    await message.answer_photo(
                        photo=proof_id,
                        caption=f"{rank_emoji} <b>{rank}-o'rin</b> - To'lov isboti"
                    )
                except:
                    pass
    else:
        text += "\n\n<i>G'oliblar hali e'lon qilinmagan.</i>"
    
    await message.answer(text)
