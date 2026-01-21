"""
/start buyrug'i handleri
"""
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from database import Database
from utils import check_subscriptions, generate_referral_link
from keyboards import get_subscription_keyboard, get_main_menu_keyboard
from messages import WELCOME_MESSAGE, SUBSCRIPTION_REQUIRED
from config import REFERRAL_LIMIT

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    /start buyrug'i
    Format: /start yoki /start USER_ID (referal)
    """
    user_id = message.from_user.id
    username = message.from_user.username
    
    # Referal parametrini olish
    args = message.text.split()
    referrer_id = None
    
    if len(args) > 1:
        try:
            referrer_id = int(args[1])
            # O'z-o'ziga referal bo'lmaslik
            if referrer_id == user_id:
                referrer_id = None
        except ValueError:
            referrer_id = None
    
    # Foydalanuvchini database'ga qo'shish yoki olish
    user = await Database.get_user(user_id)
    
    if not user:
        # Yangi foydalanuvchi
        # Referal hisoblash hozir qilinmaydi, faqat obunadan keyin
        user = await Database.create_user(user_id, username, referrer_id)
    
    # Majburiy obuna tekshiruvi
    is_subscribed, missing_channels = await check_subscriptions(message.bot, user_id)
    
    if not is_subscribed:
        # Obuna bo'lmagan
        channels_text = "\n".join([f"📢 {ch['name']}" for ch in missing_channels])
        await message.answer(
            text=SUBSCRIPTION_REQUIRED.format(channels=channels_text),
            reply_markup=get_subscription_keyboard(missing_channels)
        )
    else:
        # Obuna bo'lgan - xush kelibsiz xabari
        await message.answer(
            text=WELCOME_MESSAGE,
            reply_markup=get_main_menu_keyboard()
        )
