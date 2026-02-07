"""
Klaviaturalar (Inline va Reply)
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def get_subscription_keyboard(channels: list) -> InlineKeyboardMarkup:
    """Majburiy obuna uchun klaviatura"""
    buttons = []
    
    # Har bir kanal uchun tugma
    for channel in channels:
        buttons.append([
            InlineKeyboardButton(
                text=f"📢 {channel['name']}",
                url=channel['url']
            )
        ])
    
    # Tekshirish tugmasi
    buttons.append([
        InlineKeyboardButton(
            text="✅ Obuna bo'ldim",
            callback_data="check_subscription"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Asosiy menyu klaviaturasi"""
    keyboard = [
        [KeyboardButton(text="🔗 Referal havolam")],
        [KeyboardButton(text="📊 Statistikam")],
        [KeyboardButton(text="💸 Sovrindorlar 🏆")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_referral_keyboard(referral_link: str, closed_group_link: str = None) -> InlineKeyboardMarkup:
    """Referal uchun klaviatura"""
    # Taklif matnini tayyorlash
    share_text = "🧠 MATEMATIKA TEST QUIZ — bilim orqali yutuq!\n\nBotga kiring: " + referral_link
    
    buttons = [
        [InlineKeyboardButton(text="↗️ Do'stlarga ulashish", switch_inline_query=share_text)],
        [InlineKeyboardButton(text="🔄 Yangilash", callback_data="refresh_stats")]
    ]
    
    # Agar guruh linki bo'lsa, tugma qo'shish
    if closed_group_link:
        buttons.insert(0, [InlineKeyboardButton(text="🔒 Yopiq guruhga kirish", url=closed_group_link)])
        
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_admin_keyboard() -> InlineKeyboardMarkup:
    """Admin panel klaviaturasi"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats")],
        [InlineKeyboardButton(text="👥 Foydalanuvchilar", callback_data="admin_users")],
        [InlineKeyboardButton(text="✅ Yakunlaganlar", callback_data="admin_completed")]
    ])
