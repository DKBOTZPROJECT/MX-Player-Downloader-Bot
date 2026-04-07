import os
import requests
import asyncio
from pyrogram import Client as DKBOTZ, filters

API_ID = int(os.environ.get("API_ID", ""))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

DKBOTZBOT = DKBOTZ(
    "dkbotz_mx_player_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=999,
)

async def mx_player_request_api(url):
    api_url = f"https://ott.dkbotzpro.in/mxplayer?url={url}"
    for _ in range(3):
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        await asyncio.sleep(1)
    return False

@DKBOTZBOT.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text("🚀 Welcome To MX Player Downloader Bot\n\n🔥 Experience Lightning Fast Video Extraction From MX Player\n\n📥 Simply Send A Valid MX Player Link And Let The Bot Handle Everything Automatically\n\n💡 Type /help To Explore Features")

@DKBOTZBOT.on_message(filters.command("help"))
async def help_cmd(client, message):
    await message.reply_text("📖 Advanced Help Guide\n\n🎯 Supported Tasks:\n• MX Player Video Download\n\n⚙️ How It Works:\n1. Send MX Player Video Link\n2. Select Quality\n3. Processing Begins Instantly\n4. Video Delivered Directly To You\n\n🚀 Features:\n• Ultra Fast Download Engine\n• Automatic Link Detection\n• Optimized Upload System\n• Smart Error Handling\n\n⚠️ Note:\n• Only Valid MX Player Links Are Supported\n• Processing Time Depends On File Size And Server Speed")



DKBOTZBOT.run()
