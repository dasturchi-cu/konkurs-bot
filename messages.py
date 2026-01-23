"""
Bot xabarlari (O'zbek tilida)
"""

# Start xabari
WELCOME_MESSAGE = """👋 <b>Xush kelibsiz!</b>

Bu bot — yopiq guruhlarda o‘tkaziladigan sovrinli, pullik matematika testlariga kirish uchun yaratilgan.
Hurmat bilan Admin Ixtiyor @Ixtiyor_Math_05

📌 <b>Bot orqali siz:</b>

🔒 Maxsus yopiq guruhlarga qo‘shilasiz
💰 Pullik va sovrinli testlarda ishtirok etasiz
🏆 Eng yuqori ball to‘plagan ishtirokchilar taqdirlanadi
📊 Natijalar asosida reyting shakllanadi

👇 Ishtirok shartlari va yopiq guruhlarga kirish uchun menyuni oching."""

# Obuna bo'lish xabari
SUBSCRIPTION_REQUIRED = """⚠️ <b>Majburiy obuna</b>

Botdan foydalanish uchun quyidagi kanallarga obuna bo'lishingiz shart:

{channels}

👇 Obuna bo'lgach, "Obuna bo'ldim ✅" tugmasini bosing"""

# Obuna tekshirish muvaffaqiyatli
SUBSCRIPTION_SUCCESS = """✅ <b>Ajoyib!</b>

Siz barcha kanallarga obuna bo'ldingiz.

Endi referal havolangizni oling va {limit} ta do'st taklif qiling! 👇"""

# Referal statistika / Taklif qilish xabari
REFERRAL_MESSAGE = """🧠 <b>MATEMATIKA TEST QUIZ — bilim orqali yutuq!</b>

• Matematika test va rasmli quizlar orqali bilimingizni sinang va rivojlantiring.

📅 Har oy 2 marta yutuqli test-quizlar
🏆 Yuqori natija egalariga sovg‘alar va bonuslar

🔒 <b>Yopiq guruhga qo‘shilish sharti:</b>
➡️ {limit} nafar do‘stingizni taklif qilishingiz kerak bo‘ladi.

🔥 Tasodif yo‘q — faqat bilim baholanadi.
Do‘stlaringizni taklif qiling va birga yutuqqa erishing!

👇 <b>Havola ustiga bosib, taklif qilishni boshlang!</b>

{link}"""

REFERRAL_STATS = """📊 <b>Sizning statistikangiz:</b> {count}/{limit}

{message}"""

# 10 ta do'st to'lganda
CONGRATULATIONS = """🎉 <b>TABRIKLAYMIZ!</b>

Siz {limit} ta do'st taklif qildingiz va yopiq guruhga qo'shildingiz! 🎊

🔒 <b>Yopiq guruhga kirish:</b>
👉 {link}

✅ Yopiq guruhda 50+ ta PDF kitoblar va boshqa qimmatli materiallar sizni kutmoqda!

⚠️ <b>MUHIM:</b> Majburiy kanallardan chiqib ketsangiz, yopiq guruh huquqingiz block qilinadi!"""

# Kanallardan chiqib ketgan
UNSUBSCRIBED_WARNING = """⚠️ <b>OGOHLANTIRISH!</b>

Siz majburiy kanallardan chiqib ketgansiz.

Yopiq guruhda qolish va botdan foydalanish uchun qayta obuna bo'ling! 👇

{channels}"""

# Admin panel xabarlari
ADMIN_MENU = """👨‍💼 <b>ADMIN PANEL</b>

/stat - Umumiy statistika
/users - Barcha foydalanuvchilar
/completed - Yakunlaganlar ro'yxati
/broadcast [xabar] - Hammaga xabar yuborish
/check [USER_ID] - Foydalanuvchini tekshirish"""

ADMIN_STATS = """📊 <b>UMUMIY STATISTIKA</b>

👥 Jami foydalanuvchilar: <b>{total}</b>
✅ Yakunlaganlar: <b>{completed}</b>
🔗 Referal orqali kelganlar: <b>{referrals}</b>
🔒 Yopiq guruhdagilar: <b>{in_group}</b>"""

BROADCAST_SENT = """✅ Xabar yuborildi!

📤 Yuborildi: {sent} ta foydalanuvchiga
❌ Xato: {failed} ta"""

# Xato xabarlari
ERROR_MESSAGE = "❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring."
NOT_ADMIN = "⛔️ Bu buyruq faqat adminlar uchun!"
USER_NOT_FOUND = "❌ Foydalanuvchi topilmadi."
