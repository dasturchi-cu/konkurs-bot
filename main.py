"""
Telegram Konkurs / Referral Bot
10 ta do'st taklif qilib yopiq guruhga kirish tizimi
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

# Config va database
from config import BOT_TOKEN, validate_config
from database import test_database

# Handlers
from handlers import start, subscription, referral, admin, results

# Middleware
from middlewares import SubscriptionMiddleware

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Bot asosiy funksiyasi"""
    
    # Konfiguratsiya validatsiyasi
    try:
        validate_config()
    except ValueError as e:
        logger.error(f"❌ Konfiguratsiya xatosi: {e}")
        return
    
    # Database ulanishini tekshirish
    logger.info("Database ulanishini tekshiryapman...")
    db_ok = await test_database()
    
    # ConfigCache va Sozlamalar
    from services import ConfigCache
    await ConfigCache.initialize()
    
    if not db_ok:
        logger.error("Database ulanishida xatolik!")
        # return # Database bo'lmasa ham ishlayversin (cache configdan oladi)
        pass
    
    # Bot va dispatcher yaratish
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Handlerlarni ro'yxatdan o'tkazish
    dp.include_router(start.router)
    dp.include_router(subscription.router)
    dp.include_router(referral.router)
    dp.include_router(admin.router)
    dp.include_router(results.router) # Natijalar
    
    # Middleware'ni qo'shish
    # Faqat Message va CallbackQuery uchun
    dp.message.middleware(SubscriptionMiddleware())
    dp.callback_query.middleware(SubscriptionMiddleware())
    
    # Bot ishga tushdi
    logger.info("Bot ishga tushdi!")
    logger.info("Polling rejimida ishlayapti...")
    
    # Polling
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot to'xtatildi")
