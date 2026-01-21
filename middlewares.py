"""
Subscription check middleware
Har bir foydalanuvchi interaksiyasida obuna tekshiruvi
"""
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from utils import check_subscriptions
from keyboards import get_subscription_keyboard
from messages import UNSUBSCRIBED_WARNING


class SubscriptionMiddleware(BaseMiddleware):
    """
    Majburiy obuna tekshirish middleware
    /start dan tashqari har bir xabarda ishlaydi
    """
    
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        # Message yoki CallbackQuery ekanligini aniqlash
        if isinstance(event, CallbackQuery):
            user_id = event.from_user.id
            message = event.message
        else:
            user_id = event.from_user.id
            message = event
        
        # /start buyrug'i uchun middleware ishlamaydi
        if isinstance(event, Message) and event.text and event.text.startswith("/start"):
            return await handler(event, data)
        
        # Admin buyruqlari uchun ham ishlamaydi
        if isinstance(event, Message) and event.text and event.text.startswith("/"):
            # Admin buyruqlari
            admin_commands = ["/admin", "/stat", "/users", "/completed", "/broadcast", "/check"]
            if any(event.text.startswith(cmd) for cmd in admin_commands):
                return await handler(event, data)
        
        # Obuna tekshiruvi
        bot = data.get("bot") or (event.bot if isinstance(event, Message) else event.message.bot)
        is_subscribed, missing_channels = await check_subscriptions(bot, user_id)
        
        if not is_subscribed:
            # Obuna bo'lmagan - ogohlantirish
            channels_text = "\n".join([f"📢 {ch['name']}" for ch in missing_channels])
            
            if isinstance(event, CallbackQuery):
                await event.answer("⚠️ Majburiy kanallarga obuna bo'ling!", show_alert=True)
            
            await message.answer(
                text=UNSUBSCRIBED_WARNING.format(channels=channels_text),
                reply_markup=get_subscription_keyboard(missing_channels)
            )
            return  # Handler ishga tushmaydi
        
        # Obuna bo'lgan - davom etadi
        return await handler(event, data)
