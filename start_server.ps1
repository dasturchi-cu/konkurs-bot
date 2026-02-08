# Webdock Server Ishga Tushirish - Muammo Hal Qilish
# Play tugmasi ishlamasa, quyidagi usullarni ko'ring

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Webdock Server Ishga Tushirish" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "⚠️  Play tugmasi ishlamayapti? Quyidagi usullarni sinab ko'ring:" -ForegroundColor Yellow
Write-Host ""

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  USUL 1: Dashboard'da Boshqa Tugmalar" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Webdock dashboard'ga kiring: https://app.webdock.io" -ForegroundColor Cyan
Write-Host "2. 'konkurs bot' serverini toping" -ForegroundColor White
Write-Host "3. Server sahifasida quyidagi tugmalarni tekshiring:" -ForegroundColor White
Write-Host "   - ⚙️  Settings tugmasi (sozlamalar)" -ForegroundColor Gray
Write-Host "   - 🔄 Reboot tugmasi (qayta ishga tushirish)" -ForegroundColor Gray
Write-Host "   - 📊 Monitoring bo'limi" -ForegroundColor Gray
Write-Host "4. Settings > Server Actions bo'limida 'Start' tugmasini qidiring" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  USUL 2: Browser Console (F12)" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Webdock dashboard'da F12 tugmasini bosing (Developer Tools)" -ForegroundColor Cyan
Write-Host "2. Console tab'ga o'ting" -ForegroundColor White
Write-Host "3. Quyidagi JavaScript kodini kiriting:" -ForegroundColor White
Write-Host ""
Write-Host '   // Serverni ishga tushirish' -ForegroundColor Gray
Write-Host '   fetch("/api/v1/servers/YOUR_SERVER_ID/actions/start", {' -ForegroundColor Gray
Write-Host '     method: "POST",' -ForegroundColor Gray
Write-Host '     headers: { "Authorization": "Bearer YOUR_TOKEN" }' -ForegroundColor Gray
Write-Host '   })' -ForegroundColor Gray
Write-Host ""
Write-Host "   (YOUR_SERVER_ID va YOUR_TOKEN ni o'z ma'lumotlaringiz bilan almashtiring)" -ForegroundColor Yellow
Write-Host ""

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  USUL 3: Webdock Support" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Webdock dashboard'da Support yoki Help bo'limiga kiring" -ForegroundColor Cyan
Write-Host "2. Support ticket oching" -ForegroundColor White
Write-Host "3. Muammoni tasvirlang:" -ForegroundColor White
Write-Host "   - Server nomi: 'konkurs bot'" -ForegroundColor Gray
Write-Host "   - Muammo: Play tugmasi ishlamayapti" -ForegroundColor Gray
Write-Host "   - Server holati: Stopped" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  USUL 4: API orqali (Agar API Token bor bo'lsa)" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

$useApi = Read-Host "API orqali ishga tushirishni xohlaysizmi? (y/n)"

if ($useApi -eq "y" -or $useApi -eq "Y") {
    Write-Host ""
    Write-Host "API token olish uchun:" -ForegroundColor Cyan
    Write-Host "1. Webdock dashboard > Settings > API Keys" -ForegroundColor White
    Write-Host "2. Yangi API key yarating" -ForegroundColor White
    Write-Host ""
    
    $apiToken = Read-Host "API Token'ni kiriting"
    $serverId = Read-Host "Server ID ni kiriting (dashboard'dan)"
    
    if (-not [string]::IsNullOrWhiteSpace($apiToken) -and -not [string]::IsNullOrWhiteSpace($serverId)) {
        Write-Host ""
        Write-Host "🚀 Serverni ishga tushirish..." -ForegroundColor Yellow
        
        $apiUrl = "https://api.webdock.io/api/v1/servers/$serverId/actions/start"
        $headers = @{
            "Authorization" = "Bearer $apiToken"
            "Content-Type" = "application/json"
        }
        
        try {
            $response = Invoke-RestMethod -Uri $apiUrl -Method Post -Headers $headers -ErrorAction Stop
            Write-Host "✅ Server ishga tushirish so'rovi yuborildi!" -ForegroundColor Green
            Write-Host "   Bir necha daqiqa kutib, server holatini tekshiring." -ForegroundColor Yellow
        } catch {
            Write-Host "❌ Xatolik: $($_.Exception.Message)" -ForegroundColor Red
            if ($_.Exception.Response) {
                $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
                $responseBody = $reader.ReadToEnd()
                Write-Host "   Javob: $responseBody" -ForegroundColor Gray
            }
        }
    } else {
        Write-Host "❌ API token yoki Server ID kiritilmadi!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  MUAMMO HAL QILISH TAVSIYALARI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Browser'ni yangilang (F5 yoki Ctrl+R)" -ForegroundColor White
Write-Host "2. Boshqa browser'dan ochib ko'ring (Chrome, Firefox, Edge)" -ForegroundColor White
Write-Host "3. Browser cache'ni tozalang" -ForegroundColor White
Write-Host "4. Incognito/Private mode'da ochib ko'ring" -ForegroundColor White
Write-Host "5. Webdock dashboard'ni to'liq yuklang (1-2 daqiqa kuting)" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

