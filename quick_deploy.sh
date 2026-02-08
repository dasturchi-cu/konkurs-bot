#!/bin/bash

# Tezkor deploy (build qilmasdan, faqat restart)

echo "🔄 Botni tezkor restart qilish..."

# 1. Container'ni restart qilish
docker-compose restart

# 2. Loglarni ko'rsatish
echo "📋 Bot loglari:"
docker-compose logs -f --tail=30 bot

