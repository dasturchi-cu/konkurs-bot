"""
Yordamchi funksiyalar
"""
from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from config import BOT_USERNAME, ADMIN_ID, ADMIN_GROUP_ID
from services import ConfigCache


async def check_subscriptions(bot: Bot, user_id: int) -> tuple[bool, list]:
    """
    Majburiy kanallar obunasini tekshirish
    ConfigCache dan dinamik kanallarni oladi
    """
    missing_channels = []
    channels = ConfigCache.get_channels()
    
    for channel in channels:
        try:
            # Kanal usernameni olish (@ belgisiz)
            # Agar kanalda 'url' bo'lsa-yu, 'username' bo'lmasa, url_dan olishga harakat qilamiz
            channel_username = channel.get("username")
            if not channel_username and channel.get("url"):
                channel_username = channel["url"].split("/")[-1]
            
            if channel_username and channel_username.startswith("@"):
                channel_username = channel_username[1:]
            
            # Agar username bo'lmasa, tekshirib bo'lmaydi (Private kanal bo'lishi mumkin)
            # Bunday holda botning o'zi o'sha kanal a'zosi bo'lishi kerak yoki get_chat_member link bilan ishlamaydi.
            # Bizning holatda hammasi public kanallar deb hisoblaymiz.
            if not channel_username:
                continue

            # Foydalanuvchi obunasini tekshirish
            member = await bot.get_chat_member(
                chat_id=f"@{channel_username}",
                user_id=user_id
            )
            
            # Obuna tekshirish
            if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
                missing_channels.append(channel)
        
        except Exception as e:
            # Username noto'g'ri yoki bot admin emas.
            # Agar jiddiy xato bo'lsa logga yozamiz
            # print(f"❌ Kanalga obuna tekshirishda xato ({channel.get('name')}): {e}")
            missing_channels.append(channel)
    
    is_subscribed = len(missing_channels) == 0
    return is_subscribed, missing_channels


def generate_referral_link(user_id: int) -> str:
    """Referal havola yaratish"""
    return f"https://t.me/{BOT_USERNAME}?start={user_id}"


def is_admin(user_id: int) -> bool:
    """Foydalanuvchi admin ekanligini tekshirish"""
    return user_id == ADMIN_ID


async def is_admin_group(chat_id: int) -> bool:
    """Chat admin guruhi ekanligini tekshirish"""
    return chat_id == ADMIN_GROUP_ID


def format_user_info(user: dict) -> str:
    """Foydalanuvchi ma'lumotlarini formatlash"""
    username = f"@{user.get('username')}" if user.get('username') else "❌"
    invited = user.get('invited_count', 0)
    completed = "✅" if user.get('is_completed') else "❌"
    in_group = "✅" if user.get('is_in_closed_group') else "❌"
    
    LIMIT = ConfigCache.get_limit()

    return (
        f"👤 <b>ID:</b> <code>{user['user_id']}</code>\n"
        f"📝 <b>Username:</b> {username}\n"
        f"👥 <b>Taklif qildi:</b> {invited}/{LIMIT}\n"
        f"✅ <b>Yakunlagan:</b> {completed}\n"
        f"🔒 <b>Yopiq guruhda:</b> {in_group}"
    )
