# Docker'da Botni Ishga Tushirish

## Talablar:
- Docker Desktop o'rnatilgan bo'lishi kerak
- `.env` fayli to'g'ri sozlangan bo'lishi kerak

## Qadamlar:

### 1. Docker Desktop'ni ishga tushiring

### 2. Docker'da build qiling:
```bash
docker-compose build
```

### 3. Botni ishga tushiring:
```bash
docker-compose up -d
```

### 4. Bot loglarini ko'rish:
```bash
docker-compose logs -f bot
```

### 5. Botni to'xtatish:
```bash
docker-compose down
```

### 6. Botni qayta ishga tushirish:
```bash
docker-compose restart
```

## Eslatma:
- Bot avtomatik restart qilinadi (unless-stopped)
- Loglar `./logs` papkasida saqlanadi
- `.env` fayl Docker container'ga avtomatik yuklanadi

