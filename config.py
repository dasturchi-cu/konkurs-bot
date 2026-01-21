"""
Bot konfiguratsiya fayli
Barcha muhit o'zgaruvchilari va konstantalar
"""
import os
from dotenv import load_dotenv

# .env faylni yuklash
load_dotenv()

# Bot sozlamalari
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")

# Admin sozlamalari
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
ADMIN_GROUP_ID = int(os.getenv("ADMIN_GROUP_ID", 0))

# Supabase sozlamalari
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

# Yopiq guruh
CLOSED_GROUP_LINK = os.getenv("CLOSED_GROUP_LINK")
CLOSED_GROUP_ID = os.getenv("CLOSED_GROUP_ID") # Yopiq guruh ID si (invite link yaratish uchun)
# Video ID (default qiymat: test_video.py orqali olingan)
# Video ID (default qiymat: test_video.py orqali olingan)
PROMO_VIDEO_ID = os.getenv("PROMO_VIDEO_ID")
if not PROMO_VIDEO_ID:
    PROMO_VIDEO_ID = "BAACAgIAAxkDAAOraXC63ARkRUfIdmofaupM9H7GQq0AAsaXAAJ3KolLsOK4BzHXF684BA"

REAL_VIDEO_ID = "BAACAgIAAxkDAAPVaXC-b3ET4eKq3VscBAUeT_UEZl0AAgqYAAJ3KolLnD9ZI2w87Eo4BA"

# Majburiy kanallar ro'yxati
REQUIRED_CHANNELS = [
    {
        "name": "Matematika Test Quiz",
        "username": "matematikatestquiz",
        "url": "https://t.me/matematikatestquiz"
    },
    {
        "name": "Freelancer Uzbek",
        "username": "freelanser_uzbek",
        "url": "https://t.me/freelanser_uzbek"
    },
    {
        "name": "Matematika Test Quiz Guruhi",
        "username": "matematikatestquiz_guruh",
        "url": "https://t.me/matematikatestquiz_guruh"
    }
]

# Referal limiti
REFERRAL_LIMIT = 10

# Validatsiya
def validate_config():
    """Konfiguratsiya to'g'riligini tekshirish"""
    required = {
        "BOT_TOKEN": BOT_TOKEN,
        "BOT_USERNAME": BOT_USERNAME,
        "ADMIN_ID": ADMIN_ID,
        "SUPABASE_URL": SUPABASE_URL,
        "SUPABASE_KEY": SUPABASE_KEY,
        "CLOSED_GROUP_LINK": CLOSED_GROUP_LINK
    }
    
    missing = [key for key, value in required.items() if not value]
    
    if missing:
        raise ValueError(f"Quyidagi konfiguratsiya parametrlari topilmadi: {', '.join(missing)}")
    
    print("Konfiguratsiya to'g'ri yuklandi")
