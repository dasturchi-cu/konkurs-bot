📌 LOYIHA: Telegram konkurs / referral bot (MVP, Supabase bilan)

🎯 MAQSAD
Telegram orqali foydalanuvchilarni kanalga obuna qildirish va referal orqali do‘st taklif qilish tizimi bilan ishlaydigan konkurs bot yaratish.
Ma’lumotlar bazasi Supabase’da saqlanadi.
Admin panel Telegram guruh orqali boshqariladi.

---

🧠 TEXNOLOGIYA STACK

— Backend: Python 3.10+
— Framework: aiogram 3.x
— Database: Supabase (PostgreSQL)
— Supabase API: REST
— Admin panel: Telegram guruh
— Hosting: VPS (Ubuntu 20.04+)

---

🔑 KONFIGURATSIYA (config.py / .env)

Supabase ma’lumotlari alohida config faylda saqlanadi:
. envda bor hammasi 


⚠️ Bu ma’lumotlar:
— kod ichida yozilmaydi
— GitHub’ga yuklanmaydi
— faqat serverda saqlanadi

---

👤 FOYDALANUVCHI FUNKSIONALI (MVP)

1️⃣ /start bosganda:

— user_id olinadi
— username saqlanadi
— referal bo‘lsa → referrer_id yoziladi
— foydalanuvchi ID ko‘rsatiladi

2️⃣ Majburiy obuna tekshirish:

— belgilangan kanalga obuna tekshiriladi
— obuna bo‘lmasa → tugma chiqadi
— obuna bo‘lgach → davom etadi

3️⃣ Referal tizim:

— har foydalanuvchi uchun link:
[https://t.me/bot?start=USER_ID](https://t.me/bot?start=USER_ID)

— referal orqali kirganlar:
→ referrer_id yoziladi
→ invited_count +1

4️⃣ Referal limiti:

— talab: 10 ta do‘st
— 10 ga yetganda:
→ is_completed = true
→ 1 martalik token link beriladi

---

🗄️ SUPABASE MA’LUMOTLAR BAZASI (JADVALLAR)

📁 users jadvali:

* id (uuid, pk)
* user_id (bigint, unique)
* username (text)
* referrer_id (bigint, nullable)
* invited_count (int, default 0)
* is_completed (boolean, default false)
* created_at (timestamp)

📁 invite_links jadvali:

* id (uuid, pk)
* user_id (bigint)
* token (text, unique)
* is_used (boolean, default false)
* created_at (timestamp)

---

👥 ADMIN PANEL (TELEGRAM GURUH)

Alohida guruh:
— bot qo‘shiladi
— faqat adminlar bo‘ladi

Admin buyruqlar:

/admin — menyu
/stat — statistika
/users — foydalanuvchilar
/completed — yakunlaganlar
/broadcast — xabar yuborish

---

🔒 XAVFSIZLIK

— user faqat 1 marta yoziladi
— o‘z-o‘ziga referal yo‘q
— referal 1 marta hisoblanadi
— 1 martalik link bloklanadi
— admin buyruqlar faqat admin_id

---

🔗 SUPABASE BILAN ISHLASH

Python orqali Supabase REST ishlatiladi:

— foydalanuvchi qo‘shish
— invited_count yangilash
— completed belgilash
— token yaratish va tekshirish

---

📅 ISH BOSQICHLARI

1. Supabase ulash + jadval yaratish
2. /start + user saqlash
3. obuna tekshiruv
4. referal tizim
5. admin panel
6. 1 martalik link
7. test + deploy

---

✅ MVP NATIJA

✔️ Supabase’da barcha user saqlanadi
✔️ referal tizim ishlaydi
✔️ admin guruhdan boshqaradi
✔️ konkurs to‘liq yuradi

---

📌 STATUS: Supabase bilan MVP tayyor texnik topshiriq
📌 LOYIHA: Telegram Konkurs / Referral Bot (MVP – yopiq guruh + sovrin tizimi)

🎯 MAQSAD
Telegram orqali foydalanuvchilarni bir nechta kanal va guruhlarga majburiy obuna qildirish,
referal tizim orqali do‘st taklif qilish va ma’lum miqdorga yetganda yopiq guruhga kirish huquqi berish.

Asosiy “fishka” — **yopiq guruhga faqat 10 ta do‘st taklif qilganlar kiradi**.
Konkurslar va sovrinlar yopiq guruh ichida o‘tkaziladi.

---

🧠 TEXNOLOGIYA STACK

— Backend: Python 3.10+
— Framework: aiogram 3.x
— Database: Supabase (PostgreSQL)
— Admin panel: Telegram ichidagi maxsus admin guruh
— Hosting: VPS (Linux)

---

👤 ADMIN MA’LUMOTI

Admin Telegram ID:
👉 **7458702074**

Admin huquqlari:
— statistika ko‘rish
— foydalanuvchilar ro‘yxati
— completed userlar
— broadcast
— yopiq guruhga qo‘shish

---

📌 MAJBURIY OBUNA KANALLAR / GURUHLAR

Foydalanuvchi /start qilganda quyidagilarga majburiy obuna tekshiriladi:

1️⃣ Kanal:
[https://t.me/matematikatestquiz](https://t.me/matematikatestquiz)

2️⃣ Yopiq guruh (hozircha tekshiruv, kirish keyin):
[https://t.me/matematikatestquiz_guruh](https://t.me/matematikatestquiz_guruh)

3️⃣ Kanal:
[https://t.me/freelanser_uzbek](https://t.me/freelanser_uzbek)

4️⃣ Asosiy loyiha kanali (keyin qo‘shiladi)

Agar hammasiga obuna bo‘lmasa:
→ “Obuna bo‘ling” tugmasi chiqadi
→ qayta tekshirish tugmasi

---

👤 FOYDALANUVCHI OQIMI (TO‘LIQ LOGIKA)

### 1️⃣ /start bosganda:

— user_id olinadi
— username saqlanadi
— referal bo‘lsa → referrer_id yoziladi
— foydalanuvchi ID ko‘rsatiladi

Agar referal link bilan kirgan bo‘lsa:
→ referrer invited_count +1

---

### 2️⃣ Asosiy matn va taklif posti:

Bot quyidagi matnni yuboradi:

👋 Assalomu alaykum!

Pedagoglar uchun maxsus yopiq kanalda
50+ ta PDF kitoblar jamlanmasi BEPUL tarqatilyapti 🎁

Ishtirok etish uchun:

1️⃣ Taklif havolangizni oling
2️⃣ 10 nafar ustozga ulashing
3️⃣ 10 nafar ustoz havola orqali botga kirib, kanallarga a’zo bo‘lsa —
siz yopiq guruhga kirish huquqini olasiz 🔒

👇 Tugmani bosing va havolani oling

---

### 3️⃣ Referal tizim:

Har foydalanuvchiga maxsus link beriladi:

[https://t.me/BOT_USERNAME?start=USER_ID](https://t.me/BOT_USERNAME?start=USER_ID)

Referal orqali kirganlar:
— referrer_id yoziladi
— invited_count +1

Cheklovlar:
— user o‘ziga referal bo‘la olmaydi
— bitta user faqat 1 marta hisoblanadi

---

### 4️⃣ Referal limiti:

Talab: **10 ta do‘st**

invited_count == 10 bo‘lganda:

— is_completed = true
— foydalanuvchiga yopiq guruh uchun **1 martalik maxsus link** beriladi
— bot yozadi:

“Tabriklaymiz 🎉
Siz 10 ta do‘st taklif qildingiz.
Mana yopiq guruhga kirish havolasi 🔒”

---

### 5️⃣ Yopiq guruh logikasi:

— guruh linki faqat token orqali beriladi
— link 1 marta ishlaydi
— ishlatilgach → is_used = true
— boshqa foydalanuvchi foydalana olmaydi

---

👥 ADMIN PANEL (TELEGRAM GURUH ORQALI)

Alohida admin guruhi ochiladi.
Bot shu guruhda ishlaydi.

Admin buyruqlar:

/admin — bosh menyu
/stat — umumiy statistika
/users — foydalanuvchilar soni
/completed — 10 taga yetganlar
/broadcast — hammaga xabar yuborish

Statistika:
— jami user
— faol user
— referal bilan kelganlar
— yopiq guruhga kirganlar

---

🗄️ SUPABASE MA’LUMOTLAR BAZASI (SQL)

### 📁 users jadvali

```sql
create table users (
    id uuid primary key default gen_random_uuid(),
    user_id bigint unique not null,
    username text,
    referrer_id bigint,
    invited_count integer default 0,
    is_completed boolean default false,
    created_at timestamp default now()
);
```

---

### 📁 invite_links jadvali (yopiq guruh uchun token)

```sql
create table invite_links (
    id uuid primary key default gen_random_uuid(),
    user_id bigint not null,
    token text unique not null,
    is_used boolean default false,
    created_at timestamp default now()
);
```

---

🧠 QO‘SHIMCHA QOIDALAR

— har bir user faqat 1 marta ro‘yxatdan o‘tadi
— referal faqat 1 marta sanaladi
— admin_id = 7458702074
— admin bo‘lmagan buyruqlar ishlamaydi
— 10 ga yetgandan keyin referal hisoblanmaydi

---

📅 MVP ISH REJASI

1-bosqich:
— bot skeleton
— /start + Supabase ulash
— user saqlash

2-bosqich:
— majburiy obuna tekshirish
— referal tizim

3-bosqich:
— invited_count + limit
— yopiq guruh token

4-bosqich:
— admin panel
— statistika
— broadcast

---

✅ NATIJA

Oxirida bot:

✔️ user saqlaydi
✔️ 3–4 kanalga obuna tekshiradi
✔️ referal orqali +1 sanaydi
✔️ 10 taga yetganda yopiq guruhga kirgizadi
✔️ admin guruhdan boshqariladi

---

📌 STATUS: To‘liq MVP texnik topshiriq tayyor
🔒 YOPIQ GURUH KIRISH NAZORATI (MUHIM QO‘SHIMCHA LOGIKA)

🎯 MAQSAD
Foydalanuvchi 10 ta do‘st taklif qilgach yopiq guruhga kiradi.
Agar keyinchalik majburiy kanallardan chiqib ketsa —
bot avtomatik tekshiradi va qayta obuna bo‘lishga majbur qiladi.

---

👤 1️⃣ 10 TA DO‘ST TO‘LGANDA NIMA BO‘LADI

invited_count == 10 bo‘lganda:

— is_completed = true
— yopiq guruh uchun 1 martalik token link yaratiladi
— foydalanuvchiga quyidagi xabar yuboriladi:

“🎉 Tabriklaymiz!
Siz 10 ta do‘st taklif qildingiz va yopiq guruhga qo‘shildingiz 🔒

Mana kirish havolasi:
👉 [Yopiq guruh linki]”

— foydalanuvchi yopiq guruhga kiradi

---

👁️ 2️⃣ DOIMIY TEKSHIRUV (ENG MUHIM FISHKA)

Bot HAR SAFAR foydalanuvchi botga yozganda yoki tugma bossanda:

Quyidagilarni tekshiradi:

✅ matematikatestquiz kanalida bormi
✅ freelanser_uzbek kanalida bormi
✅ asosiy kanal (keyin qo‘shiladi)

Agar shulardan bittasidan ham chiqib ketgan bo‘lsa:

— foydalanuvchiga yoziladi:

“⚠️ Siz majburiy kanallardan chiqib ketgansiz.
Yopiq guruhda qolish uchun qayta obuna bo‘ling.”

— “Qayta obuna bo‘lish” tugmasi chiqadi
— qayta tekshirilmaguncha:
❌ yopiq guruh linki berilmaydi
❌ bot funksiyalari yopiladi

---

🔄 3️⃣ YOPIQ GURUHDA HAM NAZORAT

Agar foydalanuvchi yopiq guruhga kirib,
keyin majburiy kanallardan chiqib ketsa:

— bot tekshiruv paytida buni aniqlaydi
— foydalanuvchiga yozadi:

“⚠️ Siz majburiy kanallardan chiqib ketdingiz.
Yopiq guruhda qolish uchun qayta obuna bo‘ling.”

— agar ma’lum vaqt ichida obuna bo‘lmasa:
→ admin ogohlantiriladi
→ foydalanuvchi yopiq guruhdan chiqariladi (kick)

---

🗄️ 4️⃣ SUPABASE’GA QO‘SHIMCHA MAYDONLAR

users jadvaliga qo‘shimcha ustunlar:

```sql
alter table users
add column is_in_closed_group boolean default false,
add column last_check timestamp default now();
```

Ma’nosi:
— is_in_closed_group → yopiq guruhga kirganmi
— last_check → oxirgi tekshiruv vaqti

---

🤖 5️⃣ BOT LOGIKASI (ISH TARTIBI)

Har bir muhim joyda chaqiriladi:

— /start bosganda
— har bir tugma bosilganda
— yopiq guruh link berilishidan oldin

Funksiya:

check_subscriptions(user_id):

— barcha majburiy kanallarni tekshiradi
— agar bittasi yo‘q bo‘lsa → False
— hammasi joyida bo‘lsa → True

Agar False bo‘lsa:
— foydalanuvchi bloklanadi
— “qayta obuna bo‘ling” chiqadi

---

👮‍♂️ 6️⃣ ADMIN UCHUN NAZORAT

Admin buyruq:

/check USER_ID

— user hozir qaysi kanallarda bor
— yopiq guruhda bormi
— chiqib ketgan bo‘lsa → chiqarish mumkin

---

⚠️ 7️⃣ MUHIM QOIDALAR

— foydalanuvchi yopiq guruhga kirib olib keyin chiqib ketib ketolmaydi
— majburiy obuna doimiy majburiyat
— chiqib ketganlar avtomatik cheklanadi
— yopiq guruh “haqiqiy filter” bo‘lib ishlaydi

---

📌 STATUS: Yopiq guruh + doimiy nazorat logikasi qo‘shildi

Project Overview
A Telegram bot for a referral-based competition system that requires users to subscribe to channels and invite friends to gain access to a closed premium group.
Technology Stack

Backend: Python 3.10+
Framework: aiogram 3.x
Database: Supabase (PostgreSQL)
Admin Interface: Telegram group
Hosting: VPS (Ubuntu 20.04+)

Admin Configuration

Admin Telegram ID: 7458702074
Admin Permissions: Statistics, user management, broadcast, group access control

Mandatory Subscription Channels
Users must subscribe to ALL channels before proceeding:

https://t.me/matematikatestquiz
https://t.me/matematikatestquiz_guruh (closed group - access after completion)
https://t.me/freelanser_uzbek
Main project channel (to be added later)

User Flow
1. /start Command

Extract and save user_id and username
Check for referral code in start parameter
If referral exists: save referrer_id and increment referrer's invited_count
Display user ID to user

2. Subscription Verification

Check subscription status for all mandatory channels
If not subscribed: show "Subscribe" buttons
If subscribed: allow to proceed
CRITICAL: Re-check subscriptions on every bot interaction

3. Welcome Message (after subscription verification)
👋 Assalomu alaykum!

Pedagoglar uchun maxsus yopiq kanalda
50+ ta PDF kitoblar jamlanmasi BEPUL tarqatilyapti 🎁

Ishtirok etish uchun:

1️⃣ Taklif havolangizni oling
2️⃣ 10 nafar ustozga ulashing
3️⃣ 10 nafar ustoz havola orqali botga kirib, kanallarga a'zo bo'lsa —
siz yopiq guruhga kirish huquqini olasiz 🔒

👇 Tugmani bosing va havolani oling
4. Referral System

Each user gets unique link: https://t.me/BOT_USERNAME?start=USER_ID
When someone joins via referral link:

Save referrer_id in new user's record
Increment referrer's invited_count by 1


Restrictions:

Users cannot refer themselves
Each user counted only once per referrer
Referrals not counted after user reaches 10



5. Completion Logic (10 Referrals)
When invited_count reaches 10:

Set is_completed = true
Generate one-time access token
Send message:

🎉 Tabriklaymiz!
Siz 10 ta do'st taklif qildingiz va yopiq guruhga qo'shildingiz 🔒

Mana kirish havolasi:
👉 [One-time group link]
6. Continuous Subscription Monitoring
CRITICAL FEATURE: Before any bot action, check if user is still subscribed to ALL mandatory channels.
If user unsubscribed from any channel:

Block all bot functions
Show warning message:

⚠️ Siz majburiy kanallardan chiqib ketgansiz.
Yopiq guruhda qolish uchun qayta obuna bo'ling.

Display "Re-subscribe" button
If user is in closed group and doesn't re-subscribe within timeframe:

Notify admin
Remove user from closed group (kick)



Database Schema (Supabase)
users table
sqlCREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id BIGINT UNIQUE NOT NULL,
    username TEXT,
    referrer_id BIGINT,
    invited_count INTEGER DEFAULT 0,
    is_completed BOOLEAN DEFAULT false,
    is_in_closed_group BOOLEAN DEFAULT false,
    last_check TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);
invite_links table
sqlCREATE TABLE invite_links (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id BIGINT NOT NULL,
    token TEXT UNIQUE NOT NULL,
    is_used BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Admin Panel (Telegram Group Commands)

Available commands in admin group:
- `/admin` - Show admin menu
- `/stat` - Display statistics (total users, active users, referrals, completed users)
- `/users` - List all users
- `/completed` - List users who reached 10 referrals
- `/broadcast` - Send message to all users
- `/check USER_ID` - Check specific user's subscription status

## Security Rules
1. Each user registered only once
2. Referrals counted only once per user
3. Users cannot refer themselves
4. One-time invite links become invalid after use
5. Admin commands only work for `admin_id = 7458702074`
6. Continuous subscription verification required

## Implementation Phases

### Phase 1: Core Setup
- Bot skeleton with aiogram 3.x
- Supabase connection
- User registration on /start

### Phase 2: Subscription & Referral
- Mandatory subscription checker
- Referral link generation
- Referral tracking system

### Phase 3: Completion Logic
- Invited count tracking
- One-time token generation
- Closed group access link

### Phase 4: Admin & Monitoring
- Admin panel in Telegram group
- Statistics dashboard
- Broadcast functionality
- Continuous subscription monitoring

# Configuration (.env)
.envda bor tokenalr
ADMIN_ID=7458702074
SECURITY: Never commit .env file to Git
Expected Outcomes
✅ Users saved to Supabase
✅ Multi-channel subscription verification
✅ Referral system tracking
✅ Automatic closed group access after 10 referrals
✅ Continuous subscription monitoring
✅ Admin control via Telegram group
✅ One-time access tokens for closed group