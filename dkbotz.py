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

### All Message Start

START_MESSAGE = """<b>👋 Hello {mention},

🚀 Welcome To MX Player Downloader Bot 🎬

<i>⚡️ Use Me To Download MX Player Movies & Shows 🍿

✨ Just Send Me A Valid MX Player Link And See The Magic ✨</i>

💡 Send /help For More Information 📖</b>"""

### All Messages End

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

def full_title_builder(dkbotz_mx_data):
    title = dkbotz_mx_data.get("show_title", "Unknown")
    episode = dkbotz_mx_data.get("seo_title", "")
    season = dkbotz_mx_data.get("season", "")

    full_title = ""

    if title:
        full_title += str(title)

    if season:
        full_title += f" {season}"

    if episode:
        full_title += f" - {episode}"

    return full_title.strip()

def is_mxplayer_url(url):
    return "mxplayer.in" in url or "mxplay.com" in url

@DKBOTZBOT.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(START_MESSAGE.format(mention=message.from_user.mention))

@DKBOTZBOT.on_message(filters.command("help"))
async def help_cmd(client, message):
    await message.reply_text("📖 Advanced Help Guide\n\n🎯 Supported Tasks:\n• MX Player Video Download\n\n⚙️ How It Works:\n1. Send MX Player Video Link\n2. Select Quality\n3. Processing Begins Instantly\n4. Video Delivered Directly To You\n\n🚀 Features:\n• Ultra Fast Download Engine\n• Automatic Link Detection\n• Optimized Upload System\n• Smart Error Handling\n\n⚠️ Note:\n• Only Valid MX Player Links Are Supported\n• Processing Time Depends On File Size And Server Speed")

@DKBOTZBOT.on_message(filters.text & filters.private)
async def dkbotz_handle_link(client, message):
    url = message.text.strip()

    if not (url.startswith("http://") or url.startswith("https://")):
        return

    checking = await message.reply_text("<b>🔍 Checking...</b>")

    if not is_mxplayer_url(url):
        await checking.edit_text("<b>❌ Unsupported Link</b>")
        return

    dkbotz_mx_data = await mx_player_request_api(url)

    if not dkbotz_mx_data:
        await checking.edit_text("<b>⚠️ API Server Issues</b>")
        return

    if not dkbotz_mx_data.get("status"):
        await checking.edit_text(f"<b>❌ {dkbotz_mx_data.get('message', 'Failed To Fetch Data')}</b>")
        return

    m3u8 = dkbotz_mx_data.get("m3u8_url", "")
    mpd = dkbotz_mx_data.get("mpd_url", "")

    if m3u8:
        download_url = m3u8
    elif mpd:
        download_url = mpd
    else:
        await checking.edit_text("<b>❌ Download Link Not Found\n\nTry Another Content Or API Issues\nContact Support</b>")
        return

    full_title = full_title_builder(dkbotz_mx_data)
    description = dkbotz_mx_data.get("description", "")
    thumb = dkbotz_mx_data.get("thumbnail", "")

    text = f"<b>🎬 Full Title:</b> {title}\n\n<b>📝 Description:</b>\n{description[:300]}...\n\n<b>🔗 Download URL:</b>\n{download_url}"

    try:
        if thumb:
            await message.reply_photo(thumb, caption=text)
        else:
            await message.reply_text(text)
        await checking.delete()
    except:
        await checking.edit_text(text)



DKBOTZBOT.run()
