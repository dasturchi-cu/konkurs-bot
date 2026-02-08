"""
Supabase ma'lumotlar bazasi bilan ishlash (aiohttp versiyasi)
"""
import uuid
import aiohttp
import json
from datetime import datetime
from config import SUPABASE_URL, SUPABASE_KEY

class Database:
    """Database bilan ishlash uchun klass (REST API)"""
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    @staticmethod
    async def _request(method: str, endpoint: str, data: dict = None, params: dict = None) -> dict | list | None:
        """HTTP so'rov yuborish yordamchisi"""
        url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method=method,
                    url=url,
                    headers=Database.headers,
                    json=data,
                    params=params
                ) as response:
                    if 200 <= response.status < 300:
                        try:
                            return await response.json()
                        except:
                            return None
                    else:
                        error_text = await response.text()
                        # 409 Conflict (Duplicate Key) xatosini logda ko'rsatmaslik, 
                        # chunki bu create_user funksiyasida qayta tekshiriladi
                        if response.status != 409:
                            print(f"❌ API Xato ({method} {endpoint}): {response.status} - {error_text}")
                        return None
            except Exception as e:
                print(f"❌ So'rov xatosi: {e}")
                return None

    # --- SETTINGS (SOZLAMALAR) ---
    @staticmethod
    async def get_setting(key: str) -> str | None:
        """Sozlamani olish"""
        params = {"key": f"eq.{key}", "select": "value"}
        data = await Database._request("GET", "settings", params=params)
        return data[0]["value"] if data and len(data) > 0 else None

    @staticmethod
    async def update_setting(key: str, value: str) -> bool:
        """Sozlamani yangilash"""
        payload = {"key": key, "value": str(value)}
        headers = Database.headers.copy()
        headers["Prefer"] = "resolution=merge-duplicates,return=representation"
        
        url = f"{SUPABASE_URL}/rest/v1/settings"
        async with aiohttp.ClientSession() as session:
             async with session.post(url, headers=headers, json=payload) as resp:
                 return resp.status < 300

    # --- CHANNELS (KANALLAR) ---
    @staticmethod
    async def get_channels() -> list:
        """Barcha kanallarni olish"""
        params = {"select": "*", "order": "id.asc"}
        data = await Database._request("GET", "channels", params=params)
        return data if data else []

    @staticmethod
    async def add_channel(name: str, url: str, username: str = None) -> bool:
        """Kanal qo'shish"""
        payload = {"name": name, "url": url, "username": username}
        data = await Database._request("POST", "channels", data=payload)
        return bool(data)

    @staticmethod
    async def delete_channel(channel_id: int) -> bool:
        """Kanalni o'chirish"""
        params = {"id": f"eq.{channel_id}"}
        url = f"{SUPABASE_URL}/rest/v1/channels"
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=Database.headers, params=params) as resp:
                return resp.status < 300

    # --- USERS ---
    @staticmethod
    async def get_user(user_id: int) -> dict | None:
        """Foydalanuvchini olish"""
        params = {"user_id": f"eq.{user_id}", "select": "*"}
        data = await Database._request("GET", "users", params=params)
        return data[0] if data and len(data) > 0 else None
    
    @staticmethod
    async def create_user(user_id: int, username: str = None, referrer_id: int = None) -> dict | None:
        """Yangi foydalanuvchi yaratish (agar mavjud bo'lsa, uni qaytaradi)"""
        # Avval tekshirib ko'ramiz, user mavjudmi?
        existing_user = await Database.get_user(user_id)
        if existing_user:
            # Agar user mavjud bo'lsa, faqat username yangilansin (agar o'zgarganda)
            if username and existing_user.get("username") != username:
                params = {"user_id": f"eq.{user_id}"}
                payload = {"username": username}
                await Database._request("PATCH", "users", data=payload, params=params)
                existing_user["username"] = username
            return existing_user
        
        # Yangi user yaratish
        payload = {
            "user_id": user_id,
            "username": username,
            "referrer_id": referrer_id,
            "invited_count": 0,
            "is_completed": False,
            "is_in_closed_group": False,
            "is_referral_counted": False
        }
        
        data = await Database._request("POST", "users", data=payload)
        
        # Agar duplicate key xatosi bo'lsa (parallel requestlar), yana bir bor tekshiramiz
        if not data:
            existing_user = await Database.get_user(user_id)
            if existing_user:
                return existing_user
        
        created_user = data[0] if data and len(data) > 0 else None
        return created_user

    @staticmethod
    async def confirm_referral(user_id: int) -> bool:
        """Referalni tasdiqlsh"""
        user = await Database.get_user(user_id)
        if not user or not user.get("referrer_id") or user.get("is_referral_counted"):
            return False
        referrer_id = user["referrer_id"]
        
        params = {"user_id": f"eq.{user_id}"}
        payload = {"is_referral_counted": True}
        update_res = await Database._request("PATCH", "users", data=payload, params=params)
        
        if update_res:
            await Database.increment_invited_count(referrer_id)
            return True
        return False
    
    @staticmethod
    async def increment_invited_count(user_id: int) -> bool:
        """Taklif qilinganlar sonini oshirish (faqat hisob uchun)"""
        user = await Database.get_user(user_id)
        if not user: return False
        
        new_count = user.get("invited_count", 0) + 1
        params = {"user_id": f"eq.{user_id}"}
        payload = {"invited_count": new_count}
        await Database._request("PATCH", "users", data=payload, params=params)
        return True
    
    @staticmethod
    async def set_completed(user_id: int) -> bool:
        """Userni completed (link olgan) deb belgilash"""
        params = {"user_id": f"eq.{user_id}"}
        payload = {"is_completed": True, "is_in_closed_group": True}
        await Database._request("PATCH", "users", data=payload, params=params)
        return True
    
    @staticmethod
    async def get_referral_count(user_id: int) -> int:
        """Referallarni sanash (aniq usul: is_referral_counted=true)"""
        params = {
            "referrer_id": f"eq.{user_id}",
            "is_referral_counted": "eq.true",
            "select": "id"
        }
        data = await Database._request("GET", "users", params=params)
        return len(data) if data else 0

    @staticmethod
    async def get_stats() -> dict:
        """Umumiy statistika"""
        # Barcha foydalanuvchilar
        resp = await Database._request("GET", "users", params={"select": "id"})
        total = len(resp) if resp else 0
        
        # Referal orqali kelganlar (is_referral_counted=true)
        resp_ref = await Database._request("GET", "users", params={"select": "id", "is_referral_counted": "eq.true"})
        referrals = len(resp_ref) if resp_ref else 0
        
        # Yakunlaganlar (is_completed=true)
        resp_comp = await Database._request("GET", "users", params={"select": "id", "is_completed": "eq.true"})
        completed = len(resp_comp) if resp_comp else 0
        
        return {
            "total_users": total,
            "completed_users": completed,
            "referral_users": referrals,
            "in_closed_group": completed
        }

    # --- WINNERS (G'OLIBLAR) ---
    @staticmethod
    async def get_leaderboard(limit: int = 10) -> list:
        """TOP ishtirokchilarni olish (referal count bo'yicha)"""
        # Barcha userlarni olib, referral count bo'yicha sort qilamiz
        all_users = []
        params = {"select": "user_id,username,invited_count"}
        data = await Database._request("GET", "users", params=params)
        
        if not data:
            return []
        
        # invited_count bo'yicha sort (kamayish tartibida)
        sorted_users = sorted(data, key=lambda x: x.get("invited_count", 0), reverse=True)
        return sorted_users[:limit]

    @staticmethod
    async def set_winner(rank: int, user_id: int, prize: str) -> bool:
        """G'olibni belgilash"""
        # Upsert - agar rank mavjud bo'lsa update, yo'qsa insert
        payload = {"rank": rank, "user_id": user_id, "prize": prize}
        headers = Database.headers.copy()
        headers["Prefer"] = "resolution=merge-duplicates,return=representation"
        
        url = f"{SUPABASE_URL}/rest/v1/winners"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as resp:
                return resp.status < 300

    @staticmethod
    async def upload_proof(rank: int, image_id: str) -> bool:
        """To'lov isbotini yuklash"""
        params = {"rank": f"eq.{rank}"}
        payload = {"proof_image_id": image_id}
        result = await Database._request("PATCH", "winners", data=payload, params=params)
        return bool(result)

    @staticmethod
    async def get_winners() -> list:
        """G'oliblar ro'yxatini olish"""
        params = {"select": "*", "order": "rank.asc"}
        data = await Database._request("GET", "winners", params=params)
        return data if data else []

    @staticmethod
    async def get_all_users() -> list:
        """Barcha foydalanuvchilarni olish (broadcast uchun)"""
        params = {"select": "*"}
        data = await Database._request("GET", "users", params=params)
        return data if data else []


# Test funksiyasi (main.py uchun)
async def test_database():
    """Database ulanishini test qilish"""
    url = f"{SUPABASE_URL}/rest/v1/users"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    params = {"select": "count", "limit": "1"}
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    print("Database ulanishi muvaffaqiyatli")
                    return True
                else:
                    print(f"Database ulanish xatosi: {response.status}")
                    return False
        except Exception as e:
            print(f"Ulanish xatosi: {e}")
            return False
