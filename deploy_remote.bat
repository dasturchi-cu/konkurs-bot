@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   Botni Remote Serverga Deploy Qilish
echo ========================================
echo.
echo SSH Host: Dasturchi@konkursbot.vps.webdock.cloud
echo Parol: muhammad9085
echo.
echo ========================================
echo.

echo [1/3] SSH orqali serverga ulanish...
echo.
echo ⚠️  Quyidagi qadamlarni bajarish kerak:
echo.
echo 1. SSH orqali serverga ulaning:
echo    ssh Dasturchi@konkursbot.vps.webdock.cloud
echo.
echo 2. Parolni kiriting: muhammad9085
echo.
echo 3. Serverda quyidagi komandalarni bajaring:
echo    cd ~/konkurs_bot
echo    git pull
echo    bash deploy.sh
echo.
echo Yoki agar fayllar serverda bo'lmasa:
echo    mkdir -p ~/konkurs_bot
echo    cd ~/konkurs_bot
echo    # Fayllarni yuklash kerak
echo.
echo ========================================
echo.
echo [2/3] Agar sshpass o'rnatilgan bo'lsa, avtomatik deploy...
echo.

REM sshpass tekshirish (agar Git Bash yoki WSL ishlatilsa)
where sshpass >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo ✅ sshpass topildi!
    echo.
    echo [3/3] Avtomatik deploy boshlandi...
    echo.
    sshpass -p "muhammad9085" ssh -o StrictHostKeyChecking=no Dasturchi@konkursbot.vps.webdock.cloud "cd ~/konkurs_bot && bash deploy.sh"
    echo.
    echo ✅ Deploy yakunlandi!
) else (
    echo ⚠️  sshpass topilmadi.
    echo.
    echo Manual deploy qilish uchun yuqoridagi qadamlarni bajaring.
    echo.
    echo Yoki sshpass o'rnating:
    echo - Git Bash: choco install sshpass
    echo - WSL: sudo apt-get install sshpass
)

echo.
echo 
echo.
pause

