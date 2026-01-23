import asyncio
from database import Database

async def main():
    print("Checking settings...")
    msg = await Database.get_setting("referral_message")
    with open("debug_output.txt", "w", encoding="utf-8") as f:
        f.write(str(msg))
    print("Written to debug_output.txt")

if __name__ == "__main__":
    asyncio.run(main())
