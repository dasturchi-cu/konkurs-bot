#!/bin/bash

# Botni qayta deploy qilish skripti

echo "🔄 Botni qayta deploy qilish boshlandi..."

# 1. Eski containerni to'xtatish va o'chirish
echo "⏹️  Eski container to'xtatilmoqda..."
docker-compose down

# 2. Yangi image build qilish
echo "🔨 Yangi image build qilinmoqda..."
docker-compose build --no-cache

# 3. Yangi containerni ishga tushirish
echo "🚀 Yangi container ishga tushirilmoqda..."
docker-compose up -d

# 4. Loglarni ko'rsatish
echo "📋 Bot loglari:"
docker-compose logs -f --tail=50 bot

echo "✅ Deploy muvaffaqiyatli yakunlandi!"

