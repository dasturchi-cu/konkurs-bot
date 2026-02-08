# Remote serverga deploy qilish skripti
# SSH: Dasturchi@konkursbot.vps.webdock.cloud
# Parol: muhammad9085

$ErrorActionPreference = "Stop"

Write-Host "🔄 Botni remote serverga deploy qilish boshlandi..." -ForegroundColor Cyan

$SSH_HOST = "Dasturchi@konkursbot.vps.webdock.cloud"
$SSH_PASSWORD = "muhammad9085"
$REMOTE_DIR = "~/konkurs_bot"

# SSH va SCP uchun kerakli dasturlarni tekshirish
Write-Host "📋 Kerakli dasturlarni tekshirish..." -ForegroundColor Yellow

# SSH orqali serverga ulanish va deploy qilish
Write-Host "🔌 Serverga ulanish..." -ForegroundColor Yellow

# PowerShell'da SSH parol bilan ishlash uchun sshpass yoki plink kerak
# Yoki SSH key ishlatish kerak, lekin hozir parol bilan ishlaymiz

# Windows uchun SSH parol bilan ishlash - plink yoki sshpass kerak
# Agar sshpass yoki plink bo'lmasa, manual ravishda parol kiritish kerak

# Variant 1: sshpass ishlatish (agar o'rnatilgan bo'lsa)
# sshpass -p "$SSH_PASSWORD" ssh -o StrictHostKeyChecking=no $SSH_HOST "cd $REMOTE_DIR && bash deploy.sh"

# Variant 2: Manual parol kiritish (interactive)
Write-Host "⚠️  SSH parol kiritish kerak: muhammad9085" -ForegroundColor Yellow
Write-Host "📤 Serverga fayllarni yuklash..." -ForegroundColor Yellow

# Fayllarni yuklash (scp yoki rsync)
# scp -r . $SSH_HOST:$REMOTE_DIR/

# Eng oson usul: SSH orqali remote komandalarni bajarish
Write-Host "🚀 Remote serverda deploy qilish..." -ForegroundColor Yellow

# SSH orqali deploy.sh ni ishga tushirish
$deployCommand = @"
cd $REMOTE_DIR || { echo 'Papka topilmadi, yaratilmoqda...'; mkdir -p $REMOTE_DIR; cd $REMOTE_DIR; }
if [ -f deploy.sh ]; then
    chmod +x deploy.sh
    bash deploy.sh
else
    echo 'deploy.sh topilmadi, docker-compose orqali deploy qilinmoqda...'
    docker-compose down
    docker-compose build --no-cache
    docker-compose up -d
    docker-compose logs --tail=50 bot
fi
"@

Write-Host ""
Write-Host "📝 Quyidagi komandani bajarish kerak:" -ForegroundColor Cyan
Write-Host "ssh $SSH_HOST" -ForegroundColor White
Write-Host "Parol: muhammad9085" -ForegroundColor White
Write-Host ""
Write-Host "Keyin serverda quyidagi komandalarni bajaring:" -ForegroundColor Cyan
Write-Host "cd ~/konkurs_bot" -ForegroundColor White
Write-Host "bash deploy.sh" -ForegroundColor White
Write-Host ""

# Agar sshpass yoki plink bo'lsa, avtomatik bajarish
if (Get-Command sshpass -ErrorAction SilentlyContinue) {
    Write-Host "✅ sshpass topildi, avtomatik deploy boshlandi..." -ForegroundColor Green
    sshpass -p "$SSH_PASSWORD" ssh -o StrictHostKeyChecking=no $SSH_HOST $deployCommand
} elseif (Get-Command plink -ErrorAction SilentlyContinue) {
    Write-Host "✅ plink topildi, avtomatik deploy boshlandi..." -ForegroundColor Green
    echo y | plink -ssh -pw $SSH_PASSWORD $SSH_HOST $deployCommand
} else {
    Write-Host "⚠️  sshpass yoki plink topilmadi." -ForegroundColor Yellow
    Write-Host "📋 Quyidagi qadamlarni bajarish kerak:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. SSH orqali serverga ulaning:" -ForegroundColor Cyan
    Write-Host "   ssh $SSH_HOST" -ForegroundColor White
    Write-Host ""
    Write-Host "2. Parolni kiriting: muhammad9085" -ForegroundColor White
    Write-Host ""
    Write-Host "3. Serverda quyidagi komandalarni bajaring:" -ForegroundColor Cyan
    Write-Host "   cd ~/konkurs_bot" -ForegroundColor White
    Write-Host "   git pull  # agar Git ishlatilsa" -ForegroundColor White
    Write-Host "   bash deploy.sh" -ForegroundColor White
    Write-Host ""
    Write-Host "Yoki agar fayllar serverda bo'lmasa:" -ForegroundColor Yellow
    Write-Host "   mkdir -p ~/konkurs_bot" -ForegroundColor White
    Write-Host "   cd ~/konkurs_bot" -ForegroundColor White
    Write-Host "   # Fayllarni yuklash kerak (scp yoki git clone)" -ForegroundColor White
}

Write-Host ""
Write-Host "✅ Ko'rsatmalar tayyor!" -ForegroundColor Green

