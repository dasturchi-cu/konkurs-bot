# Telegram Konkurs / Referral Bot

10 ta do'st taklif qilib yopiq guruhga kirish tizimi.

## Xususiyatlar

- ✅ Majburiy kanallar obunasi tekshiruvi
- ✅ Referal tizimi (10 ta do'st limiti)
- ✅ Yopiq guruhga avtomatik kirish
- ✅ Doimiy obuna nazorati
- ✅ Admin panel Telegram guruh orqali
- ✅ Supabase PostgreSQL database

## Texnologiyalar

- Python 3.10+
- aiogram 3.15.0
- Supabase (PostgreSQL)

## O'rnatish

1. Virtual environment yaratish:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Dependencylarni o'rnatish:
```bash
pip install -r requirements.txt
```

3. `.env` faylini sozlash (allaqachon tayyor)

4. Supabase'da jadvallar yaratish:
   - Supabase Dashboard'ga kirish
   - SQL Editor'da `setup_database.sql` scriptni ishga tushirish

## Ishga tushirish

```bash
python main.py
```

## Admin Buyruqlari

Admin guruhida ishlatish uchun:

- `/admin` - Admin menyu
- `/stat` - Umumiy statistika
- `/users` - Barcha foydalanuvchilar
- `/completed` - Yakunlaganlar ro'yxati
- `/broadcast [xabar]` - Hammaga xabar yuborish
- `/check [USER_ID]` - Foydalanuvchini tekshirish

## Loyiha Strukturasi

```
konkurs_bot/
├── handlers/
│   ├── __init__.py
│   ├── start.py          # /start buyrug'i
│   ├── subscription.py   # Obuna tekshiruvi
│   ├── referral.py       # Referal tizimi
│   └── admin.py          # Admin panel
├── config.py             # Konfiguratsiya
├── database.py           # Supabase database
├── utils.py              # Yordamchi funksiyalar
├── messages.py           # Bot xabarlari
├── keyboards.py          # Klaviaturalar
├── middlewares.py        # Middleware
├── main.py               # Entry point
├── requirements.txt      # Dependencies
└── .env                  # Muhit o'zgaruvchilari
```

## Muallif

Admin: [@matematikatestquizbot](https://t.me/matematikatestquizbot)
