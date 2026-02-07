# Serverda Botni Qayta Deploy Qilish

## Tezkor Deploy (Linux/Mac):

```bash
# 1. Serverga ulaning
ssh user@your-server

# 2. Bot papkasiga kiring
cd /path/to/konkurs_bot

# 3. Deploy skriptini ishga tushiring
bash deploy.sh
```

## Yoki Qo'lda:

```bash
# 1. Eski containerni to'xtatish
docker-compose down

# 2. Yangi image build qilish
docker-compose build --no-cache

# 3. Yangi containerni ishga tushirish
docker-compose up -d

# 4. Loglarni tekshirish
docker-compose logs -f bot
```

## Windows Server uchun:

```cmd
deploy.bat
```

## Muhim Eslatmalar:

1. **`.env` fayli** to'g'ri sozlangan bo'lishi kerak
2. **Docker** va **docker-compose** o'rnatilgan bo'lishi kerak
3. Deploy qilishdan oldin **backup** oling
4. Loglarni tekshirib, bot to'g'ri ishlayotganini tasdiqlang

## Tekshirish:

```bash
# Container holatini ko'rish
docker ps

# Bot loglarini ko'rish
docker-compose logs -f bot

# Container ichiga kirish (kerak bo'lsa)
docker exec -it konkurs_bot bash
```

