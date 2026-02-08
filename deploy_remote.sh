#!/bin/bash

# Remote serverga deploy qilish skripti
# SSH: Dasturchi@konkursbot.vps.webdock.cloud
# Parol: muhammad9085

set -e

echo "🔄 Botni remote serverga deploy qilish boshlandi..."

SSH_HOST="Dasturchi@konkursbot.vps.webdock.cloud"
SSH_PASSWORD="muhammad9085"
REMOTE_DIR="~/konkurs_bot"

# SSH orqali serverga ulanish va deploy qilish
echo "🔌 Serverga ulanish..."

# sshpass o'rnatilganligini tekshirish
if command -v sshpass &> /dev/null; then
    echo "✅ sshpass topildi, avtomatik deploy boshlandi..."
    
    # Remote serverda deploy qilish
    sshpass -p "$SSH_PASSWORD" ssh -o StrictHostKeyChecking=no $SSH_HOST << 'ENDSSH'
        cd ~/konkurs_bot || { echo "Papka topilmadi, yaratilmoqda..."; mkdir -p ~/konkurs_bot; cd ~/konkurs_bot; }
        
        if [ -f deploy.sh ]; then
            echo "📋 deploy.sh topildi, ishga tushirilmoqda..."
            chmod +x deploy.sh
            bash deploy.sh
        else
            echo "⚠️  deploy.sh topilmadi, docker-compose orqali deploy qilinmoqda..."
            docker-compose down || true
            docker-compose build --no-cache
            docker-compose up -d
            sleep 3
            docker-compose logs --tail=50 bot
        fi
        
        echo ""
        echo "📊 Container holati:"
        docker ps | grep konkurs_bot || docker ps -a | grep konkurs_bot
        
        echo ""
        echo "✅ Deploy muvaffaqiyatli yakunlandi!"
ENDSSH

else
    echo "⚠️  sshpass topilmadi."
    echo "📋 Quyidagi qadamlarni bajarish kerak:"
    echo ""
    echo "1. sshpass o'rnating:"
    echo "   Ubuntu/Debian: sudo apt-get install sshpass"
    echo "   macOS: brew install hudochenko/tap/sshpass"
    echo ""
    echo "2. Yoki manual ravishda:"
    echo "   ssh $SSH_HOST"
    echo "   Parol: $SSH_PASSWORD"
    echo "   cd ~/konkurs_bot"
    echo "   bash deploy.sh"
    echo ""
    exit 1
fi

echo ""
echo "✅ Remote deploy muvaffaqiyatli yakunlandi!"

