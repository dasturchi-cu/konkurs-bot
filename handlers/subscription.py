"""
Majburiy obuna tekshiruvi handleri
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from database import Database
from utils import check_subscriptions
from keyboards import get_subscription_keyboard, get_main_menu_keyboard
from messages import SUBSCRIPTION_SUCCESS, SUBSCRIPTION_REQUIRED, WELCOME_MESSAGE

router = Router()


@router.callback_query(F.data == "check_subscription")
async def callback_check_subscription(callback: CallbackQuery):
    """Obuna tekshirish callback"""
    user_id = callback.from_user.id
    
    # Obuna tekshiruvi
    is_subscribed, missing_channels = await check_subscriptions(callback.bot, user_id)
    
    if not is_subscribed:
        # Hali ham obuna bo'lmagan
        channels_text = "\n".join([f"📢 {ch['name']}" for ch in missing_channels])
        await callback.answer("❌ Hali barcha kanallarga obuna bo'lmagansiz!", show_alert=True)
        await callback.message.edit_text(
            text=SUBSCRIPTION_REQUIRED.format(channels=channels_text),
            reply_markup=get_subscription_keyboard(missing_channels)
        )
    else:
        # Obuna bo'lgan
        
        # Referalni tasdiqlsh
        is_confirmed = await Database.confirm_referral(user_id)
        
        # Agar referal tasdiqlansa, referrerga xabar yuborish (optional)
        if is_confirmed:
            user = await Database.get_user(user_id)
            if user and user.get("referrer_id"):
                 try:
                    referrer_id = user["referrer_id"]
                    # Real countni olish
                    current_count = await Database.get_referral_count(referrer_id)
                    
                    from services import ConfigCache
                    limit = ConfigCache.get_limit()
                    
                    await callback.bot.send_message(
                        chat_id=referrer_id,
                        text=f"🎉 Yangi do'st qo'shildi! (+1)\n\n👥 Jami: {current_count}/{limit}"
                    )
                 except Exception:
                    pass

        await callback.answer("✅ Ajoyib!", show_alert=False)
        try:
            await callback.message.delete()
        except:
            pass
        
        await callback.bot.send_message(
            chat_id=callback.message.chat.id,
            text=WELCOME_MESSAGE,
            reply_markup=get_main_menu_keyboard()
        )
