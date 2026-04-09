import os
import requests
import asyncio
from pyrogram import Client as DKBOTZ, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Config import *
from fsub import ForceSub

DKBOTZBOT = DKBOTZ(
    "dkbotz_mx_player_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=999,
)

### All Message Start And Button

START_MESSAGE = """<b>👋 Hello {mention},

🚀 Welcome To MX Player Downloader Bot 🎬

<i>⚡️ Use Me To Download MX Player Movies & Shows 🍿

✨ Just Send Me A Valid MX Player Link And See The Magic ✨</i>

💡 Send /help For More Information 📖</b>"""

HELP_MESSAGE = """<b>📖 Advanced Help Guide 📘

🎯 Supported Tasks:
• MX Player Video Download 🎬

⚙️ How It Works:
1️⃣ Send MX Player Video Link 🔗
2️⃣ Select Quality 🎞️
3️⃣ Processing Begins Instantly ⚡
4️⃣ Video Delivered Directly To You 📥

🚀 Features:
• Ultra Fast Download Engine ⚡
• Automatic Link Detection 🔍
• Optimized Upload System 📤
• Smart Error Handling 🛠️

⚠️ Note:
• Only Valid MX Player Links Are Supported ❗
• Processing Time Depends On File Size And Server Speed ⏳</b>"""

ABOUT_MESSAGE = f"""ℹ️ 𝐀𝐛𝐨𝐮𝐭 𝐓𝐡𝐢𝐬 𝐁𝐨𝐭 🤖

📝 𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞: <a href='https://www.python.org'>𝐏𝐲𝐭𝐡𝐨𝐧</a>

🧰 𝐅𝐫𝐚𝐦𝐞𝐖𝐨𝐫𝐤: <a href=https://github.com/Mayuri-Chan/pyrofork'>𝐏𝐲𝐫𝐨𝐟𝐨𝐫𝐤</a>

👨‍💻 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫: <a href='https://t.me/{OWNER_USERNAME}'>𝐀𝐧𝐨𝐧𝐲𝐦𝐨𝐮𝐬</a>

📢 𝐂𝐡𝐚𝐧𝐧𝐞𝐥: <a href='{CHANNEL_URL}'>𝐂𝐡𝐚𝐧𝐧𝐞𝐥</a>"""

DONATE_MESSAGE = f"""<b>💗 Thank You For Showing Interest In Supporting Us</b>

<i>Your Small Contribution Helps Keep This Bot Running Smoothly And Continuously.</i>
━━━━━━━━━━━━━━━━━━
<b>💸 You Can Donate Any Amount:</b>

₹20 • ₹30 • ₹50 • ₹70 • ₹100 • ₹200 😊
━━━━━━━━━━━━━━━━━━
<b>📨 Payment Methods:</b>
• Google Pay
• Paytm
• PhonePe
• UPI 

<b>🆔 UPI ID:</b> <code>{UPI_ID}</code>
━━━━━━━━━━━━━━━━━━
<b>📞 Need More Information?</b>

Contact: <a href='https://t.me/{OWNER_USERNAME}'>𝐀𝐧𝐨𝐧𝐲𝐦𝐨𝐮𝐬</a>

✨ <i>Every Contribution Motivates Us To Improve And Maintain The Service.</i>"""

START_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("❓ Help", callback_data="dkbotzmsg_help"),
        InlineKeyboardButton("ℹ️ About", callback_data="dkbotzmsg_about")
    ],
    [
        InlineKeyboardButton("Join My Update Channel 📢", url=CHANNEL_URL)
    ],
    [
        InlineKeyboardButton("📛 Close", callback_data="dkbotzmsg_close")
    ]
])

HELP_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🏡 Home", callback_data="dkbotzmsg_start"),
        InlineKeyboardButton("💸 Donate", callback_data="dkbotzmsg_donate")
    ],
    [
        InlineKeyboardButton("Join My Update Channel 📢", url=CHANNEL_URL)
    ],
    [
        InlineKeyboardButton("📛 Close", callback_data="dkbotzmsg_close")
    ]
])

### All Messages End And Button

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
    if not await ForceSub(client, message):
        return

    await message.reply_text(START_MESSAGE.format(mention=message.from_user.mention), reply_markup=HELP_BUTTONS, disable_web_page_preview=True)

@DKBOTZBOT.on_message(filters.command("help"))
async def help_cmd(client, message):
    if not await ForceSub(client, message):
        return

    await message.reply_text(HELP_MESSAGE, reply_markup=HELP_BUTTONS, disable_web_page_preview=True)

@DKBOTZBOT.on_message(filters.command("about"))
async def about_cmd(client, message):
    if not await ForceSub(client, message):
        return

    await message.reply_text(ABOUT_MESSAGE, reply_markup=HELP_BUTTONS, disable_web_page_preview=True)

@DKBOTZBOT.on_message(filters.command("donate"))
async def donate_cmd(client, message):
    if not await ForceSub(client, message):
        return

    await message.reply_text(DONATE_MESSAGE, reply_markup=START_BUTTONS, disable_web_page_preview=True)

@DKBOTZBOT.on_callback_query(filters.regex("^dkbotzmsg_"))
async def callback_handler(client, query):
    data = query.data

    if data == "dkbotzmsg_start":
        await query.message.edit_text(START_MESSAGE.format(mention=query.from_user.mention), reply_markup=START_BUTTONS, disable_web_page_preview=True)

    elif data == "dkbotzmsg_help":
        await query.message.edit_text(HELP_MESSAGE, reply_markup=HELP_BUTTONS, disable_web_page_preview=True)

    elif data == "dkbotzmsg_about":
        await query.message.edit_text(ABOUT_MESSAGE, reply_markup=HELP_BUTTONS, disable_web_page_preview=True)

    elif data == "dkbotzmsg_donate":
        await query.message.edit_text(DONATE_MESSAGE, reply_markup=START_BUTTONS, disable_web_page_preview=True)

    elif data == "dkbotzmsg_close":
        await query.message.delete()


@DKBOTZBOT.on_message(filters.text & filters.private)
async def dkbotz_handle_link(client, message):
    url = message.text.strip()

    if not (url.startswith("http://") or url.startswith("https://")):
        return

    if not await ForceSub(client, message):
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

    text = f"<b>🎬 Full Title:</b> {full_title}\n\n<b>📝 Description:</b>\n{description[:300]}...\n\n<b>🔗 Download URL:</b>\n{download_url}"

    try:
        if thumb:
            await message.reply_photo(thumb, caption=text)
        else:
            await message.reply_text(text)
        await checking.delete()
    except:
        await checking.edit_text(text)



DKBOTZBOT.run()
