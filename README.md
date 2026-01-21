# 🤖 Telegram Konkurs Bot - To'liq Texnik Hujjat

## 📋 Umumiy Ma'lumot

Bu bot - **referal tizimi** va **konkurs natijalari** bilan ishlaydigan professional Telegram bot. Foydalanuvchilar 10 ta do'st taklif qilishsa, yopiq guruhga kirishlari mumkin. Admin esa konkurs natijalarini boshqaradi va g'oliblarni e'lon qiladi.

---

## 🛠 Ishlatilgan Texnologiyalar

### 1. **Python 3.10+**
Asosiy dasturlash tili

### 2. **aiogram 3.x**
Telegram Bot API uchun zamonaviy asinxron framework
- Polling rejimi (VPS/Local uchun)
- Middleware tizimi (Obuna tekshiruvi)
- Handler routing (Har bir funksiya uchun alohida handler)

### 3. **Supabase (PostgreSQL)**
Ma'lumotlar bazasi (Cloud-hosted)
- REST API orqali ulanish (`aiohttp`)
- Users jadvali (Foydalanuvchilar)
- Winners jadvali (G'oliblar)
- Settings jadvali (Sozlamalar)
- Channels jadvali (Majburiy kanallar)

### 4. **aiohttp**
HTTP requestlar uchun async library (Supabase bilan aloqa)

### 5. **python-dotenv**
Environment variables (`.env` fayldan)

---

## 📁 Loyiha Strukturasi

```
konkurs_bot/
│
├── main.py                    # Botni ishga tushirish (Entry point)
├── config.py                  # Konfiguratsiya va env o'zgaruvchilar
├── database.py                # Supabase bilan ishlash (REST API)
├── services.py                # ConfigCache (Dinamik sozlamalar)
├── messages.py                # Barcha bot xabarlari (O'zbek tilida)
├── keyboards.py               # Inline va Reply klaviaturalar
├── utils.py                   # Yordamchi funksiyalar
├── middlewares.py             # Obuna tekshiruvi (Middleware)
│
├── handlers/                  # Handler modullari
│   ├── __init__.py           # Handlerlarni export qilish
│   ├── start.py              # /start va yangi foydalanuvchilar
│   ├── subscription.py       # Obuna tekshiruvi
│   ├── referral.py           # Referal tizimi
│   ├── admin.py              # Admin panel (Boshqaruv)
│   └── results.py            # Natijalar (TOP 10, G'oliblar)
│
├── .env                       # Sirli konfiguratsiya (TOKEN, DB)
├── .gitignore                # Git ignore (sensitiv fayllar)
├── requirements.txt          # Python dependencies
├── update_schema.sql         # Database schema (Settings, Channels)
├── winners_schema.sql        # G'oliblar jadvali schema
└── README.md                 # Bu fayl
```

---

## 🗄 Database Strukturasi

### **1. users** (Foydalanuvchilar)

| Ustun | Turi | Tavsif |
|-------|------|--------|
| `id` | BIGINT | Auto-increment ID |
| `user_id` | BIGINT | Telegram User ID (Unique) |
| `username` | TEXT | @username |
| `referrer_id` | BIGINT | Kim taklif qilgan (NULL bo'lishi mumkin) |
| `invited_count` | INTEGER | Nechta odam taklif qilgan (Hisob uchun) |
| `is_referral_counted` | BOOLEAN | Obuna bo'lganmi? (Referal hisoblangan) |
| `is_completed` | BOOLEAN | 10 ta to'plaganmi? (Link olganmi) |
| `is_in_closed_group` | BOOLEAN | Yopiq guruhda a'zomi? |
| `created_at` | TIMESTAMP | Ro'yxatdan o'tgan vaqt |

### **2. winners** (G'oliblar)

| Ustun | Turi | Tavsif |
|-------|------|--------|
| `id` | BIGINT | Auto ID |
| `rank` | INTEGER | O'rin (1, 2, 3...) Unique |
| `user_id` | BIGINT | G'olib User ID |
| `prize` | TEXT | Sovrin nomi ("100,000 so'm") |
| `proof_image_id` | TEXT | To'lov isboti (Telegram file_id) |
| `announced_at` | TIMESTAMP | E'lon qilingan vaqt |

### **3. settings** (Sozlamalar)

| Ustun | Turi | Tavsif |
|-------|------|--------|
| `key` | TEXT | Sozlama nomi (Primary Key) |
| `value` | TEXT | Sozlama qiymati |

**Misol:**
- `referral_limit` → `"10"`
- `closed_group_link` → `"https://t.me/..."`
- `promo_video_id` → `"BAACAgI..."`
- `referral_message` → `"Custom matn..."`

### **4. channels** (Majburiy Kanallar)

| Ustun | Turi | Tavsif |
|-------|------|--------|
| `id` | BIGINT | Auto ID |
| `name` | TEXT | Kanal nomi |
| `url` | TEXT | Kanal linki |
| `username` | TEXT | @username |
| `created_at` | TIMESTAMP | Qo'shilgan vaqt |

---

## ⚙️ Asosiy Funksiyalar va Ularning Ishi

### **1. Start Handler (`handlers/start.py`)**

**Vazifa:** Yangi foydalanuvchilarni ro'yxatdan o'tkazish

```python
/start                    # Oddiy kirish
/start 7458702074        # Referal link orqali
```

**Jarayon:**
1. User ID ni tekshirish (Database.get_user)
2. Agar yangi bo'lsa:
   - Referer ID ni olish (agar bor bo'lsa)
   - Yangi user yaratish (Database.create_user)
3. Obuna tekshiruviga yo'naltirish (Middleware)

---

### **2. Subscription Middleware (`middlewares.py`)**

**Vazifa:** Har bir harakatdan oldin obuna tekshiruvi

**Jarayon:**
1. User barcha majburiy kanallarga a'zomi? (`utils.check_subscriptions`)
2. Agar YO'Q → Obuna klaviaturasi chiqadi
3. Agar HA → Keyingi handlerga o'tadi

**Texnik:**
- `bot.get_chat_member()` API orqali tekshirish
- ChatMemberStatus.LEFT yoki KICKED bo'lsa → A'zo emas

---

### **3. Referal System (`handlers/referral.py`)**

**Asosiy funksiyalar:**

#### `show_referral_link()`
- Foydalanuvchiga referal havolasini ko'rsatish
- Video yuborish (ConfigCache.get_video_id())
- Statistika (Invited: X/10)
- Agar 10 ta bo'lsa → Yopiq guruh havolasi (60s da o'chadi)

#### `send_temp_invite()`
- Yopiq guruh havolasini yuborish
- 60 soniya kutish (`asyncio.sleep(60)`)
- Xabarni o'chirish (`.delete()`)

#### `refresh_stats()` (Callback)
- "Yangilash" tugmasi bosilganda
- Eski xabarni o'chirish
- Yangi statistika yuborish

**Muhim Logika:**
```python
if invited >= LIMIT and not user['is_completed']:
    # Birinchi marta link yuborish
    send_temp_invite()
    Database.set_completed(user_id)
else:
    # Link allaqachon berilgan, shu sababli yuborilmaydi
    pass
```

---

### **4. Admin Panel (`handlers/admin.py`)**

#### **Statistika Komandalari:**
- `/admin` → Yordam
- `/stats` → Bot statistikasi
- `/leaderboard` → TOP 10 ishtirokchilar

#### **Sozlamalar:**
- `/set_limit 15` → Referal limiti
- `/set_link https://...` → Yopiq guruh linki
- `/set_message MATN` → Referal matni
- `/set_video FILE_ID` → Video ID

#### **Kanallar:**
- `/channels` → Ro'yxat
- `/add_channel Nom|URL` → Qo'shish
- `/del_channel ID` → O'chirish

#### **G'oliblar:**
- `/set_winner 1 USER_ID "100,000 so'm"` → G'olibni belgilash
- `/proof 1` → To'lov isbotini yuklash (rasm captionida yoki reply)

#### **Broadcast:**
- `/send` → Admin guruhidan reply qilingan xabarni hammaga yuborish

---

### **5. Results Handler (`handlers/results.py`)**

**Vazifa:** Natijalarni ko'rsatish

#### `show_results()`
1. **Leaderboard** (TOP 10) chiqarish
   - `Database.get_leaderboard(10)` orqali
   - `invited_count` bo'yicha sort
2. **G'oliblar** e'loni
   - `Database.get_winners()` orqali
   - Sovrin va o'rinlar
3. **To'lov isboti** rasmlarini yuborish
   - `answer_photo(proof_image_id)`

---

## 🔄 ConfigCache Tizimi (`services.py`)

**Vazifa:** Sozlamalarni xotirada saqlash (har doim DB ga murojaat qilmaslik)

### Qanday ishlaydi?

1. **Bot ishga tushganda:**
   ```python
   await ConfigCache.initialize()
   ```
   - Supabase dan barcha sozlamalarni yuklab oladi
   - Xotirada saqlaydi (`_settings` dict)

2. **Admin sozlama o'zgartirganda:**
   ```python
   await Database.update_setting("referral_limit", "15")
   await ConfigCache.refresh_settings()
   ```
   - Bazaga yozadi
   - Cache ni yangilaydi

3. **Handlerlar ishlatganda:**
   ```python
   limit = ConfigCache.get_limit()
   link = ConfigCache.get_closed_link()
   message = ConfigCache.get_message()
   ```

**Foyda:** Tez (RAM dan o'qish) va dinamik (DB dan olinadi).

---

## 📊 Database Metodlari (`database.py`)

### **User metodlari:**
- `get_user(user_id)` → Userni olish
- `create_user(user_id, username, referrer_id)` → Yangi user yaratish
- `confirm_referral(user_id)` → Referal tasdiqqa (obuna bo'lgandan keyin)
- `increment_invited_count(user_id)` → Invited count oshirish
- `set_completed(user_id)` → Link olgan deb belgilash
- `get_referral_count(user_id)` → Aniq referal soni (`is_referral_counted=TRUE`)

### **Winners metodlari:**
- `get_leaderboard(limit)` → TOP ishtirokchilar
- `set_winner(rank, user_id, prize)` → G'olibni belgilash
- `upload_proof(rank, image_id)` → To'lov isbotini yuklash
- `get_winners()` → G'oliblar ro'yxati

### **Settings metodlari:**
- `get_setting(key)` → Sozlamani olish
- `update_setting(key, value)` → Sozlamani yangilash (Upsert)

### **Channels metodlari:**
- `get_channels()` → Kanallar ro'yxati
- `add_channel(name, url, username)` → Kanal qo'shish
- `delete_channel(id)` → Kanalni o'chirish

---

## 🎯 Asosiy User Jarayoni (Flow)

### **1. Yangi foydalanuvchi:**
```
/start 123456 → Database.create_user(referrer_id=123456)
              → Middleware: Obuna tekshiruvi
              → Majburiy kanallarga obuna bo'lishi kerak
              → "Obuna bo'ldim ✅" → Database.confirm_referral()
              → Referrer ning countiga +1
              → Asosiy menyu
```

### **2. Referal to'plash:**
```
"🔗 Referal havolam" → Video + Matn + Link
                      → Do'stlarga ulashish
                      → Har bir do'st obuna bo'lganda +1
                      → 10 ta to'psa → Yopiq guruh havolasi (60s)
```

### **3. Natijalarni ko'rish:**
```
"🏆 Natijalar" → TOP 10 Leaderboard
               → G'oliblar ro'yxati
               → To'lov isboti rasmlari
```

---

## 👨‍💼 Admin Jarayoni (Flow)

### **1. Konkurs tugagach:**
```
/leaderboard                             # TOP 10 ni ko'rish
/set_winner 1 7458702074 "100,000 so'm"  # 1-o'rinni belgilash
/set_winner 2 123456 "50,000 so'm"       # 2-o'rin
/set_winner 3 654321 "25,000 so'm"       # 3-o'rin
```

### **2. To'lov isbotlarini yuklash:**
```
# Usul 1: Rasm + Caption
[Rasm yuboring]
Caption: /proof 1

# Usul 2: Reply
[Rasm yuboring]
Reply qilib: /proof 1
```

### **3. Broadcast:**
```
Admin guruhda:
[Xabar yozing/rasmni yuboring]
Reply qilib: /send
→ Barcha foydalanuvchilarga yuboriladi
```

### **4. Sozlamalarni o'zgartirish:**
```
/set_limit 20                    # Limitni 20 ga ko'tarish
/set_message YANGI_MATN          # Referal matnini o'zgartirish
/add_channel Sponsor|https://... # Yangi kanal qo'shish
```

---

## 🚀 Qanday Ishlaydi? (Texnik Detals)

### **1. Polling vs Webhook**
Bot hozir **Polling** rejimida:
```python
await dp.start_polling(bot)
```
- Har 1-2 soniyada Telegram serverga so'rov yuboradi
- Yangi xabarlar bormi deb tekshiradi
- VPS/Local uchun ideal

**Webhook** (Kelajakda):
- Telegram serverdan HTTP POST request keladi
- FastAPI/Flask kerak
- Production uchun yaxshi (tezroq)

### **2. Asinxron (Async/Await)**
Barcha funksiyalar `async`:
```python
async def show_referral_link(message: Message):
    user = await Database.get_user(user_id)  # Kutamiz
    await message.answer("...")              # Kutamiz
```

**Sabab:**
- Bir vaqtning o'zida ko'p foydalanuvchilarga javob berish
- Blocking operatsiyalar yo'q (tez)

### **3. Middleware Pattern**
```python
dp.message.middleware(SubscriptionMiddleware())
```
- Har bir message/callback dan **oldin** ishga tushadi
- Obuna tekshiradi
- Agar OK bo'lsa → Keyingi handlerga o'tkazadi
- Agar NO → Obuna klaviaturasi

### **4. Router Pattern**
Har bir modul o'zining `router`iga ega:
```python
# handlers/admin.py
router = Router()

@router.message(Command("stats"))
async def show_stats(message: Message):
    ...
```

Main.py da:
```python
dp.include_router(admin.router)
dp.include_router(referral.router)
# ...
```

**Foyda:** Kodning tartibli bo'lishi, debug qilish oson.

---

## 🔐 Xavfsizlik va Best Practices

### **1. Environment Variables**
Sirli ma'lumotlar `.env` faylida:
```env
BOT_TOKEN=123456:ABC...
SUPABASE_URL=https://...
SUPABASE_ANON_KEY=eyJ...
ADMIN_ID=7458702074
```

`.gitignore` da:
```
.env
__pycache__/
venv/
```

### **2. Admin Tekshiruvi**
Har qanday admin komanda:
```python
if not is_admin(message.from_user.id):
    return
```

### **3. Input Validatsiya**
```python
try:
    rank = int(message.text.split()[1])
    # ...
except:
    await message.answer("Xato!")
```

### **4. Database Injection Protection**
Supabase REST API parametrlari:
```python
params = {"user_id": f"eq.{user_id}"}  # Safe
```

---

## 📦 Dependencies (`requirements.txt`)

```
aiogram==3.4.1           # Telegram Bot framework
aiohttp==3.9.1           # HTTP client
python-dotenv==1.0.0     # .env support
```

**O'rnatish:**
```bash
pip install -r requirements.txt
```

---

## 🎛 Botni Ishga Tushirish

### **Local (Test):**
```bash
python main.py
```

### **VPS (24/7):**
```bash
# PM2 bilan (Node.js kerak)
pm2 start "python main.py" --name konkurs_bot
pm2 save
pm2 startup

# yoki screen bilan
screen -S bot
python main.py
# Ctrl+A, D (Detach)
```

---

## 📝 Xulosa

### **Bot nimalarni qila oladi?**

**Foydalanuvchilar uchun:**
✅ Referal orqali do'st taklif qilish
✅ 10 ta to'plasa yopiq guruhga kirish
✅ Statistikani ko'rish
✅ Konkurs natijalarini ko'rish
✅ Video bilan chiroyli taklifnoma olish

**Admin uchun:**
✅ Limitni dynamic o'zgartirish
✅ Referal matnini o'zgartirish
✅ Kanallarni qo'shish/o'chirish
✅ G'oliblarni belgilash
✅ To'lov isbotlarini yuklash
✅ TOP 10 ni ko'rish
✅ Broadcast yuborish

### **Texnologiyalar:**
- Python + aiogram 3.x
- Supabase (PostgreSQL)
- Async/Await pattern
- ConfigCache (Dynamic settings)
- Middleware (Auto-check)
- Modular architecture

### **Code Quality:**
- ✅ Har bir fayl o'z vazifasiga javobgar
- ✅ Asinxron (tez)
- ✅ Xavfsiz (env variables, admin check)
- ✅ Scalable (Yangi funksiyalar qo'shish oson)

**Bot tayyor va professional darajada!** 🚀
