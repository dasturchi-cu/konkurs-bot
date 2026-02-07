#!/bin/bash

# Botni qayta deploy qilish skripti (24/7 ishlashi uchun)

echo "🔄 Botni qayta deploy qilish boshlandi..."

# 1. Git'dan yangi kodlarni olish (agar Git ishlatilsa)
if [ -d ".git" ]; then
    echo "📥 Git'dan yangi kodlar olinmoqda..."
    git pull origin main || git pull origin master
fi

# 2. Eski containerni to'xtatish va o'chirish
echo "⏹️  Eski container to'xtatilmoqda..."
docker-compose down

# 3. Yangi image build qilish
echo "🔨 Yangi image build qilinmoqda..."
docker-compose build --no-cache

# 4. Eski imagelarni tozalash (ixtiyoriy)
echo "🧹 Eski imagelarni tozalash..."
docker image prune -f

# 5. Yangi containerni ishga tushirish
echo "🚀 Yangi container ishga tushirilmoqda..."
docker-compose up -d

# 6. Bir oz kutish (container ishga tushishi uchun)
sleep 3

# 7. Container holatini tekshirish
echo "📊 Container holati:"
docker ps | grep konkurs_bot

# 8. Loglarni ko'rsatish
echo ""
echo "📋 Bot loglari (oxirgi 50 qator):"
docker-compose logs --tail=50 bot

echo ""
echo "✅ Deploy muvaffaqiyatli yakunlandi!"
echo "💡 To'liq loglarni ko'rish uchun: docker-compose logs -f bot"

