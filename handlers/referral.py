import os
import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from database import Database
from utils import generate_referral_link
from keyboards import get_referral_keyboard
from messages import REFERRAL_STATS, CONGRATULATIONS
from services import ConfigCache

router = Router()

async def send_temp_invite(message: Message, user_id: int):
    """Vaqtinchalik invite link yuborish va o'chirish"""
    try:
        # Dinamik link (Admin panelidan o'zgartirilishi mumkin)
        link_to_send = ConfigCache.get_closed_link()
        
        warn_text = "\n\n⏳ <b>DIQQAT: Bu xabar 60 soniyadan keyin o'chiriladi!</b>\nTezroq ulanib oling, havola boshqa ishlamaydi."

        msg = await message.answer(
            text=f"🎉 <b>Siz shartni bajardingiz!</b>\n\n🔒 <b>Yopiq guruhga havola:</b>\n{link_to_send}{warn_text}",
            disable_web_page_preview=True
        )
        
        # 60 soniya kutish va o'chirish
        await asyncio.sleep(60)
        try:
            await msg.delete()
        except:
            pass
            
    except Exception as e:
        print(f"Temp invite error: {e}")


@router.message(F.text == "🔗 Referal havolam")
async def show_referral_link(message: Message):
    """Referal havolasini ko'rsatish"""
    user_id = message.from_user.id
    invited = await Database.get_referral_count(user_id)
    user = await Database.get_user(user_id) 
    
    referral_link = generate_referral_link(user_id)
    group_link = None 

    # Dynamic limit
    LIMIT = ConfigCache.get_limit()

    # Referal matnini olish (ConfigCache dan yoki messages.py dan)
    msg_text = ConfigCache.get_message().format(link=referral_link, limit=LIMIT)
    
    full_text = f"📊 <b>Sizning statistikangiz:</b> {invited}/{LIMIT}\n\n" + msg_text
    
    if invited >= LIMIT:
        if user and user.get("is_completed"):
             pass # Jim turamiz
        else:
             full_text += f"\n\n🎉 <b>Tabriklaymiz! Shart bajarildi.</b>\nYopiq guruh havolasi pastda alohida xabarda keladi 👇"
    
    markup = get_referral_keyboard(referral_link, group_link)

    # Video yuborish (Dynamic ID)
    VIDEO_ID = ConfigCache.get_video_id()
    try:
        if VIDEO_ID:
            await message.answer_video(
                video=VIDEO_ID,
                caption=full_text,
                reply_markup=markup
            )
        else:
            # Agar ID bo'lmasa matn
             await message.answer(full_text, reply_markup=markup, disable_web_page_preview=True)   
    except Exception as e:
        await message.answer(full_text, reply_markup=markup, disable_web_page_preview=True)
        
    # Link yuborish
    if invited >= LIMIT and user and not user.get("is_completed"):
        asyncio.create_task(send_temp_invite(message, user_id))
        await Database.set_completed(user_id)


@router.message(F.text == "🔒 Yopiq guruh")
async def check_closed_group_access(message: Message):
    """Fallback handler"""
    await message.answer("Menyudan Referal bo'limini tanlang.")


@router.message(F.text == "📊 Statistikam")
async def show_stats(message: Message):
    """Statistika ko'rsatish"""
    await show_referral_link(message)


from aiogram.exceptions import TelegramBadRequest

@router.callback_query(F.data == "refresh_stats")
async def refresh_stats(callback: CallbackQuery):
    """Statistikani yangilash"""
    user_id = callback.from_user.id
    invited = await Database.get_referral_count(user_id)
    user = await Database.get_user(user_id)
    referral_link = generate_referral_link(user_id)
    group_link = None
    
    LIMIT = ConfigCache.get_limit()

    msg_text = ConfigCache.get_message().format(link=referral_link, limit=LIMIT)
    full_text = f"📊 <b>Sizning statistikangiz:</b> {invited}/{LIMIT}\n\n" + msg_text
    
    if invited >= LIMIT:
        if user and user.get("is_completed"):
             pass
        else:
             full_text += f"\n\n🎉 <b>Tabriklaymiz! Shart bajarildi.</b>\nYopiq guruh havolasi pastda alohida xabarda keladi 👇"

    markup = get_referral_keyboard(referral_link, group_link)

    try:
        await callback.message.delete()
    except:
        pass

    VIDEO_ID = ConfigCache.get_video_id()
    try:
        if VIDEO_ID:
            await callback.message.answer_video(
                video=VIDEO_ID,
                caption=full_text,
                reply_markup=markup
            )
        else:
             await callback.message.answer(full_text, reply_markup=markup, disable_web_page_preview=True)
    except Exception as e:
        await callback.message.answer(full_text, reply_markup=markup, disable_web_page_preview=True)
    
    await callback.answer()
    
    if invited >= LIMIT and user and not user.get("is_completed"):
        asyncio.create_task(send_temp_invite(callback.message, user_id))
        await Database.set_completed(user_id)


async def notify_completion(bot, user_id: int):
    pass
