# Remote Serverga Deploy Qilish Ko'rsatmasi

## Server Ma'lumotlari
- **SSH Host:** Dasturchi@konkursbot.vps.webdock.cloud
- **Parol:** muhammad9085
- **Remote Papka:** ~/konkurs_bot

## Deploy Qilish Usullari

### Usul 1: Avtomatik (sshpass bilan)

#### Linux/Mac uchun:
```bash
# sshpass o'rnating (agar yo'q bo'lsa)
sudo apt-get install sshpass  # Ubuntu/Debian
# yoki
brew install hudochenko/tap/sshpass  # macOS

# Deploy skriptini ishga tushiring
bash deploy_remote.sh
```

#### Windows uchun:
```powershell
# PowerShell'da
.\deploy_remote.ps1
```

### Usul 2: Manual (SSH orqali)

1. **SSH orqali serverga ulaning:**
```bash
ssh Dasturchi@konkursbot.vps.webdock.cloud
```
Parol: `muhammad9085`

2. **Serverda bot papkasiga kiring:**
```bash
cd ~/konkurs_bot
```

3. **Agar Git ishlatilsa, yangi kodlarni oling:**
```bash
git pull origin main
# yoki
git pull origin master
```

4. **Deploy skriptini ishga tushiring:**
```bash
chmod +x deploy.sh
bash deploy.sh
```

5. **Yoki agar deploy.sh bo'lmasa, Docker orqali:**
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
docker-compose logs -f bot
```

### Usul 3: Fayllarni Yuklash (Agar serverda yo'q bo'lsa)

#### Linux/Mac uchun (scp bilan):
```bash
# Butun loyihani yuklash
scp -r . Dasturchi@konkursbot.vps.webdock.cloud:~/konkurs_bot/

# Keyin SSH orqali deploy qilish
ssh Dasturchi@konkursbot.vps.webdock.cloud
cd ~/konkurs_bot
bash deploy.sh
```

#### Windows uchun (WinSCP yoki PowerShell):
```powershell
# PowerShell'da
scp -r . Dasturchi@konkursbot.vps.webdock.cloud:~/konkurs_bot/
```

## Tekshirish

Deploy qilgandan keyin bot ishlayotganini tekshiring:

```bash
ssh Dasturchi@konkursbot.vps.webdock.cloud
docker ps | grep konkurs_bot
docker-compose logs -f bot
```

## 24/7 Ishlashi

Bot Docker'da `restart: unless-stopped` sozlamasi bilan ishlaydi, shuning uchun:
- Server qayta ishga tushganda bot avtomatik ishga tushadi
- Bot xatolik yuz berganda avtomatik qayta ishga tushadi
- Faqat `docker-compose down` yoki `docker stop` bilan to'xtatiladi

## Muammo Hal Qilish

### Container ishlamayapti:
```bash
docker-compose logs bot
docker ps -a
docker-compose restart
```

### Yangi kodlar yuklanmadi:
```bash
git pull
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### .env fayli sozlanmagan:
```bash
nano ~/konkurs_bot/.env
# Kerakli o'zgaruvchilarni kiriting
docker-compose restart
```

