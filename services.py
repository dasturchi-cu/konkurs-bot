import asyncio
from database import Database
from config import REFERRAL_LIMIT, REQUIRED_CHANNELS, CLOSED_GROUP_LINK, PROMO_VIDEO_ID, REAL_VIDEO_ID

class ConfigCache:
    """
    Sozlamalar va Kanallarni xotirada saqlash (DB ga har doim murojaat qilmaslik uchun)
    """
    _settings = {
        "referral_limit": int(REFERRAL_LIMIT or 10),
        "closed_group_link": CLOSED_GROUP_LINK or "https://t.me/...",
        "promo_video_id": REAL_VIDEO_ID,
        "referral_message": ""  # Bo'sh bo'lsa, messages.py dan olinadi
    }
    _channels = []
    
    @staticmethod
    async def initialize():
        """Boshlang'ich yuklash"""
        print("Sozlamalar yuklanmoqda...")
        
        # 1. Sozlamalarni yuklash
        limit = await Database.get_setting("referral_limit")
        if limit: ConfigCache._settings["referral_limit"] = int(limit)
        
        link = await Database.get_setting("closed_group_link")
        if link: ConfigCache._settings["closed_group_link"] = link
        
        video = await Database.get_setting("promo_video_id")
        if video: ConfigCache._settings["promo_video_id"] = video
        
        msg = await Database.get_setting("referral_message")
        if msg: ConfigCache._settings["referral_message"] = msg
        
        # 2. Kanallarni yuklash
        db_channels = await Database.get_channels()
        if db_channels:
            ConfigCache._channels = db_channels
        else:
            ConfigCache._channels = REQUIRED_CHANNELS
            
        print(f"Sozlamalar yuklandi. Limit: {ConfigCache.get_limit()}, Kanallar: {len(ConfigCache._channels)}")

    @staticmethod
    def get_limit() -> int:
        return ConfigCache._settings.get("referral_limit", 10)

    @staticmethod
    def get_closed_link() -> str:
        return ConfigCache._settings.get("closed_group_link", "")

    @staticmethod
    def get_video_id() -> str:
        return ConfigCache._settings.get("promo_video_id", "")

    @staticmethod
    def get_channels() -> list:
        return ConfigCache._channels

    @staticmethod
    def get_message() -> str:
        """Referal matnini olish (bo'sh bo'lsa messages.py dan)"""
        custom = ConfigCache._settings.get("referral_message", "")
        if custom:
            return custom
        # Default (messages.py dan)
        from messages import REFERRAL_MESSAGE
        return REFERRAL_MESSAGE

    @staticmethod
    async def refresh_settings():
        """Qayta yuklash (Admin o'zgartirganda)"""
        await ConfigCache.initialize()
