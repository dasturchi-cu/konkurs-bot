# Serverni ishga tushirish va deploy qilish skripti
# Avval Webdock dashboard'da serverni ishga tushiring!

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Server Deploy Skripti" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$SSH_HOST = "Dasturchi@konkursbot.vps.webdock.cloud"
$SSH_PASSWORD = "muhammad9085"

Write-Host "⚠️  MUHIM: Avval Webdock dashboard'da serverni ishga tushiring!" -ForegroundColor Yellow
Write-Host "   Dashboard: https://app.webdock.io" -ForegroundColor Yellow
Write-Host "   Server: konkurs bot" -ForegroundColor Yellow
Write-Host "   Play (▶️) tugmasini bosing va 1-2 daqiqa kuting" -ForegroundColor Yellow
Write-Host ""

$continue = Read-Host "Serverni ishga tushirdingizmi? (y/n)"
if ($continue -ne "y" -and $continue -ne "Y") {
    Write-Host "❌ Serverni ishga tushiring va keyin qayta urinib ko'ring!" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "🔌 Serverni tekshiryapman..." -ForegroundColor Yellow

# Serverni tekshirish (ping yoki SSH)
$maxRetries = 10
$retryCount = 0
$connected = $false

while ($retryCount -lt $maxRetries -and -not $connected) {
    Write-Host "   Urinish $($retryCount + 1)/$maxRetries..." -ForegroundColor Gray
    
    try {
        $result = Test-NetConnection -ComputerName konkursbot.vps.webdock.cloud -Port 22 -WarningAction SilentlyContinue -ErrorAction SilentlyContinue
        if ($result.TcpTestSucceeded) {
            $connected = $true
            Write-Host "✅ Server ishga tushdi!" -ForegroundColor Green
            break
        }
    } catch {
        # Ignore
    }
    
    if (-not $connected) {
        $retryCount++
        if ($retryCount -lt $maxRetries) {
            Write-Host "   Kutish... (5 soniya)" -ForegroundColor Gray
            Start-Sleep -Seconds 5
        }
    }
}

if (-not $connected) {
    Write-Host ""
    Write-Host "❌ Server hali ishga tushmagan yoki tarmoq muammosi bor!" -ForegroundColor Red
    Write-Host "   Webdock dashboard'da server holatini tekshiring." -ForegroundColor Yellow
    Write-Host ""
    exit
}

Write-Host ""
Write-Host "🚀 Deploy qilish boshlandi..." -ForegroundColor Cyan
Write-Host ""

# SSH orqali deploy qilish
Write-Host "📤 Serverga ulanish va deploy qilish..." -ForegroundColor Yellow
Write-Host "   SSH: $SSH_HOST" -ForegroundColor Gray
Write-Host "   Parol: $SSH_PASSWORD" -ForegroundColor Gray
Write-Host ""

# SSH komandasi
$deployCommands = @"
cd ~/konkurs_bot || { echo 'Papka topilmadi, yaratilmoqda...'; mkdir -p ~/konkurs_bot; cd ~/konkurs_bot; }
echo '📥 Git pull...'
git pull origin main || git pull origin master
echo '🔨 Deploy...'
if [ -f deploy.sh ]; then
    chmod +x deploy.sh
    bash deploy.sh
else
    echo 'deploy.sh topilmadi, docker-compose orqali...'
    docker-compose down
    docker-compose build --no-cache
    docker-compose up -d
    sleep 3
    docker-compose logs --tail=50 bot
fi
echo ''
echo '📊 Container holati:'
docker ps | grep konkurs_bot || docker ps -a | grep konkurs_bot
"@

Write-Host "⚠️  SSH orqali ulanish kerak. Quyidagi komandani bajaring:" -ForegroundColor Yellow
Write-Host ""
Write-Host "ssh $SSH_HOST" -ForegroundColor White
Write-Host "Parol: $SSH_PASSWORD" -ForegroundColor White
Write-Host ""
Write-Host "Keyin serverda:" -ForegroundColor Yellow
Write-Host "cd ~/konkurs_bot" -ForegroundColor White
Write-Host "git pull" -ForegroundColor White
Write-Host "bash deploy.sh" -ForegroundColor White
Write-Host ""

# Agar sshpass yoki plink bo'lsa, avtomatik qilish
if (Get-Command sshpass -ErrorAction SilentlyContinue) {
    Write-Host "✅ sshpass topildi, avtomatik deploy..." -ForegroundColor Green
    sshpass -p "$SSH_PASSWORD" ssh -o StrictHostKeyChecking=no $SSH_HOST $deployCommands
} elseif (Get-Command plink -ErrorAction SilentlyContinue) {
    Write-Host "✅ plink topildi, avtomatik deploy..." -ForegroundColor Green
    echo y | plink -ssh -pw $SSH_PASSWORD $SSH_HOST $deployCommands
} else {
    Write-Host "ℹ️  sshpass yoki plink topilmadi. Yuqoridagi qadamlarni manual bajaring." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ Deploy jarayoni yakunlandi!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

