import os
import re
import time
import random
import string
import math
import glob
import shutil
import requests
import asyncio
import yt_dlp
import aiohttp
from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyrogram import Client as DKBOTZ, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from Config import *
from fsub import ForceSub

USER_DATA = {}

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

def humanbytes(size):
    """Convert bytes to human readable format"""
    if not size:
        return "0 B"
    power = 2**10
    n = 0
    units = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"

async def fix_thumb(thumb):
    width = 0
    height = 0

    try:
        if not thumb:
            return 0, 0, None

        thumb = str(thumb).strip()

        if thumb.startswith(("http://", "https://")):
            os.makedirs("DKBOTZ", exist_ok=True)

            name = "".join(random.choices(string.ascii_letters + string.digits, k=12))
            ext = os.path.splitext(thumb.split("?")[0])[1].lower()
            if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
                ext = ".jpg"

            file_path = os.path.join("DKBOTZ", f"{name}{ext}")

            timeout = aiohttp.ClientTimeout(total=30)
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0"}

            async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
                async with session.get(thumb) as resp:
                    if resp.status != 200:
                        return 0, 0, None

                    with open(file_path, "wb") as f:
                        while True:
                            chunk = await resp.content.read(1024 * 32)
                            if not chunk:
                                break
                            f.write(chunk)

            thumb = file_path

        if not os.path.exists(thumb):
            return 0, 0, None

        img = Image.open(thumb).convert("RGB")
        ow, oh = img.size

        if ow <= 0 or oh <= 0:
            return 0, 0, None

        new_width = 320
        new_height = int((oh / ow) * new_width)

        img = img.resize((new_width, new_height))
        img.save(thumb, "JPEG", quality=95)

        width = new_width
        height = new_height

        try:
            metadata = extractMetadata(createParser(thumb))
            if metadata:
                if metadata.has("width"):
                    width = metadata.get("width")
                if metadata.has("height"):
                    height = metadata.get("height")
        except:
            pass

        return width, height, thumb

    except Exception as e:
        return 0, 0, None

def TimeFormatter(milliseconds: int) -> str:
    """Format time from milliseconds to readable format"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

async def get_video_metadata(file_path):
    """Extract video duration, width, and height"""
    duration = 0
    width = 0
    height = 0

    try:
        metadata = extractMetadata(createParser(file_path))
        if metadata is not None:
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")
    except Exception as e:
        print(f"Metadata extraction error: {e}")

    return duration, width, height

async def progress_for_pyrogram(current, total, ud_type, message, start):
    """Display download/upload progress"""
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🚫 Cancel", callback_data="closeme")]])

    now = time.time()
    diff = now - start

    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round(
            (total - current) / speed) * 1000 if speed > 0 else 0
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \n<b>📊 Percentage:</b> {2}%\n".format(
            ''.join(["■" for i in range(math.floor(percentage / 5))]),
            ''.join(["□" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))

        tmp = progress + "<b>✅ Completed:</b> {0}\n<b>📁 Total Size:</b> {1}\n<b>🚀 Speed:</b> {2}/s\n<b>⌚️ ETA:</b> {3}\n".format(
            humanbytes(current), humanbytes(total), humanbytes(speed),
            estimated_total_time if estimated_total_time != '' else "0 s")

        try:
            await message.edit(text="{}\n{}".format(ud_type, tmp),
                               reply_markup=reply_markup)
        except:
            pass

async def remove_file(file_path):
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        return True
    except Exception as e:
        return False

async def remove_folder(folder_path):
    try:
        if not folder_path or not os.path.exists(folder_path):
            return True

        try:
            shutil.rmtree(folder_path, ignore_errors=True)
        except:
            pass

        if os.path.exists(folder_path):
            try:
                os.rmdir(folder_path)
            except:
                pass

        return not os.path.exists(folder_path)

    except Exception as e:
        return False

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

def is_mxplayer_url(url):
    return "mxplayer.in" in url or "mxplay.com" in url

@DKBOTZBOT.on_message(filters.command("start"))
async def start_cmd(client, message):
    user = message.from_user
    if DB_ENABLED:
        join = await add_user(user)
        if join and LOG_CHANNEL:
            await client.send_message(LOG_CHANNEL, f"🚀 <b>New User Started The Bot</b>\n👤 <b>Name :</b> {user.first_name or 'Unknown'} {user.last_name or ''}\n🆔 <b>User ID :</b> <code>{user.id}</code>\n🔗 <b>Username :</b> {'@' + user.username if user.username else 'Not Set'}\n🌍 <b>Language :</b> {user.language_code or 'Unknown'}\n🤖 <b>Bot :</b> {'Yes' if user.is_bot else 'No'}\n⏰ <b>Time :</b> <code>{datetime.now().strftime('%d %B %Y %I:%M:%S %p')}</code>")
        if await is_banned(user.id):
            return await message.reply_text("<b>🚫 Sorry, You Are Banned From Using This Bot.</b>")

    if not await ForceSub(client, message):
        return

    await message.reply_text(START_MESSAGE.format(mention=message.from_user.mention), reply_markup=HELP_BUTTONS, disable_web_page_preview=True)

@DKBOTZBOT.on_message(filters.command("help"))
async def help_cmd(client, message):
    user = message.from_user
    if DB_ENABLED:
        join = await add_user(user)
        if join and LOG_CHANNEL:
            await client.send_message(LOG_CHANNEL, f"🚀 <b>New User Started The Bot</b>\n👤 <b>Name :</b> {user.first_name or 'Unknown'} {user.last_name or ''}\n🆔 <b>User ID :</b> <code>{user.id}</code>\n🔗 <b>Username :</b> {'@' + user.username if user.username else 'Not Set'}\n🌍 <b>Language :</b> {user.language_code or 'Unknown'}\n🤖 <b>Bot :</b> {'Yes' if user.is_bot else 'No'}\n⏰ <b>Time :</b> <code>{datetime.now().strftime('%d %B %Y %I:%M:%S %p')}</code>")
        if await is_banned(user.id):
            return await message.reply_text("<b>🚫 Sorry, You Are Banned From Using This Bot.</b>")

    if not await ForceSub(client, message):
        return

    await message.reply_text(HELP_MESSAGE, reply_markup=HELP_BUTTONS, disable_web_page_preview=True)

@DKBOTZBOT.on_message(filters.command("about"))
async def about_cmd(client, message):
    user = message.from_user
    if DB_ENABLED:
        join = await add_user(user)
        if join and LOG_CHANNEL:
            await client.send_message(LOG_CHANNEL, f"🚀 <b>New User Started The Bot</b>\n👤 <b>Name :</b> {user.first_name or 'Unknown'} {user.last_name or ''}\n🆔 <b>User ID :</b> <code>{user.id}</code>\n🔗 <b>Username :</b> {'@' + user.username if user.username else 'Not Set'}\n🌍 <b>Language :</b> {user.language_code or 'Unknown'}\n🤖 <b>Bot :</b> {'Yes' if user.is_bot else 'No'}\n⏰ <b>Time :</b> <code>{datetime.now().strftime('%d %B %Y %I:%M:%S %p')}</code>")
        if await is_banned(user.id):
            return await message.reply_text("<b>🚫 Sorry, You Are Banned From Using This Bot.</b>")

    if not await ForceSub(client, message):
        return

    await message.reply_text(ABOUT_MESSAGE, reply_markup=HELP_BUTTONS, disable_web_page_preview=True)

@DKBOTZBOT.on_message(filters.command("donate"))
async def donate_cmd(client, message):
    user = message.from_user
    if DB_ENABLED:
        join = await add_user(user)
        if join and LOG_CHANNEL:
            await client.send_message(LOG_CHANNEL, f"🚀 <b>New User Started The Bot</b>\n👤 <b>Name :</b> {user.first_name or 'Unknown'} {user.last_name or ''}\n🆔 <b>User ID :</b> <code>{user.id}</code>\n🔗 <b>Username :</b> {'@' + user.username if user.username else 'Not Set'}\n🌍 <b>Language :</b> {user.language_code or 'Unknown'}\n🤖 <b>Bot :</b> {'Yes' if user.is_bot else 'No'}\n⏰ <b>Time :</b> <code>{datetime.now().strftime('%d %B %Y %I:%M:%S %p')}</code>")
        if await is_banned(user.id):
            return await message.reply_text("<b>🚫 Sorry, You Are Banned From Using This Bot.</b>")

    if not await ForceSub(client, message):
        return

    await message.reply_text(DONATE_MESSAGE, reply_markup=START_BUTTONS, disable_web_page_preview=True)

@DKBOTZBOT.on_message(filters.command("profile") & filters.private)
async def dkbotz_profile_cmd(client, message):
    if not DB_ENABLED:
        return await message.reply_text("<b>⚠️ Database Not Enabled.</b>")

    user = message.from_user
    data = users_col.find_one({"user_id": user.id}) or {}

    await message.reply_text(f"<b>👤 Your Profile</b>\n\n🆔 <b>User ID :</b> <code>{user.id}</code>\n👤 <b>Name :</b> {user.first_name or 'Unknown'} {user.last_name or ''}\n🔗 <b>Username :</b> {'@' + user.username if user.username else 'Not Set'}\n🌍 <b>Language :</b> {user.language_code.upper() if user.language_code else 'Unknown'}\n📦 <b>Total Downloads :</b> <code>{data.get('downloads', 0)}</code>\n🚫 <b>Banned :</b> {'Yes' if data.get('is_banned') else 'No'}")

@DKBOTZBOT.on_message(filters.command("ban"))
async def dkbotz_ban_cmd(client, message):
    if message.from_user.id not in ADMINS:
        return await message.reply_text("<b>❌ Access Denied</b>")
    if not DB_ENABLED:
        return await message.reply_text("<b>⚠️ Database Not Enabled.</b>")

    args = message.text.split()

    if len(args) < 2 or not args[1].isdigit():
        return await message.reply_text("<b>Usage :</b> <code>/ban user_id</code>")

    uid = int(args[1])

    if await ban_user(uid):
        await message.reply_text(f"<b>✅ User Banned Successfully</b>\n🆔 <code>{uid}</code>")

        if LOG_CHANNEL:
            try:
                await client.send_message(LOG_CHANNEL, f"🚫 <b>User Banned</b>\n🆔 <b>User ID :</b> <code>{uid}</code>\n👮 <b>Banned By :</b> {message.from_user.mention}")
            except Exception:
                pass

    else:
        await message.reply_text(f"<b>⚠️ Unable To Ban User</b>\n🆔 <code>{uid}</code>")


@DKBOTZBOT.on_message(filters.command("unban"))
async def dkbotz_unban_cmd(client, message):
    if message.from_user.id not in ADMINS:
        return await message.reply_text("<b>❌ Access Denied</b>")
    if not DB_ENABLED:
        return await message.reply_text("<b>⚠️ Database Not Enabled.</b>")

    args = message.text.split()

    if len(args) < 2 or not args[1].isdigit():
        return await message.reply_text("<b>Usage :</b> <code>/unban user_id</code>")

    uid = int(args[1])

    if await unban_user(uid):
        await message.reply_text(f"<b>✅ User Unbanned Successfully</b>\n🆔 <code>{uid}</code>")

        if LOG_CHANNEL:
            try:
                await client.send_message(LOG_CHANNEL, f"✅ <b>User Unbanned</b>\n🆔 <b>User ID :</b> <code>{uid}</code>\n👮 <b>Unbanned By :</b> {message.from_user.mention}")
            except Exception:
                pass

    else:
        await message.reply_text(f"<b>⚠️ User Already Unbanned Or Not Found</b>\n🆔 <code>{uid}</code>")


@DKBOTZBOT.on_message(filters.command("broadcast"))
async def dkbotz_broadcast_cmd(client, message):
    if message.from_user.id not in ADMINS:
        return await message.reply_text("<b>❌ Access Denied</b>")
    if not DB_ENABLED:
        return await message.reply_text("<b>⚠️ Database Not Enabled.</b>")

    bc_msg = message.reply_to_message

    if not bc_msg:
        return await message.reply_text("<b>📢 Reply To A Message To Broadcast.</b>")

    users = await get_all_users()
    total = len(users)

    if not total:
        return await message.reply_text("<b>⚠️ No Users Found.</b>")

    status = await message.reply_text(f"<b>📢 Broadcasting Message To {total} Users...</b>")

    success = 0
    failed = 0

    for uid in users:
        try:
            await bc_msg.copy(uid)
            success += 1

        except FloodWait as e:
            await asyncio.sleep(e.value)

            try:
                await bc_msg.copy(uid)
                success += 1
            except Exception:
                failed += 1

        except Exception:
            failed += 1

        await asyncio.sleep(1)

    await status.edit_text(f"<b>📢 Broadcast Completed</b>\n\n✅ <b>Success :</b> <code>{success}</code>\n❌ <b>Failed :</b> <code>{failed}</code>\n👥 <b>Total Users :</b> <code>{total}</code>")


@DKBOTZBOT.on_message(filters.command("stats"))
async def dkbotz_stats_cmd(client, message):
    if message.from_user.id not in ADMINS:
        return await message.reply_text("<b>❌ Access Denied</b>")
    if not DB_ENABLED:
        return await message.reply_text("<b>⚠️ Database Not Enabled.</b>")

    s = await get_stats()

    if not s:
        return await message.reply_text("<b>⚠️ Unable To Fetch Statistics.</b>")

    await message.reply_text(f"<b>📊 DKBOTZBOT Statistics</b>\n\n👥 <b>Total Users :</b> <code>{s.get('total_users', 0)}</code>\n✅ <b>Active Users :</b> <code>{s.get('active_users', 0)}</code>\n🚫 <b>Banned Users :</b> <code>{s.get('banned_users', 0)}</code>\n🆕 <b>New Users Today :</b> <code>{s.get('new_today', 0)}</code>\n📦 <b>Total Downloads :</b> <code>{s.get('total_downloads', 0)}</code>")


@DKBOTZBOT.on_message(filters.command("users"))
async def dkbotz_users_cmd(client, message):
    if message.from_user.id not in ADMINS:
        return await message.reply_text("<b>❌ Access Denied</b>")
    if not DB_ENABLED:
        return await message.reply_text("<b>⚠️ Database Not Enabled.</b>")

    s = await get_stats()

    await message.reply_text(f"<b>👥 DKBOTZBOT User Summary</b>\n\n👤 <b>Total Users :</b> <code>{s.get('total_users', 0)}</code>\n✅ <b>Active Users :</b> <code>{s.get('active_users', 0)}</code>\n🚫 <b>Banned Users :</b> <code>{s.get('banned_users', 0)}</code>\n🆕 <b>Joined Today :</b> <code>{s.get('new_today', 0)}</code>")


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

async def start_download(client, query, saved):
    user_id = query.from_user.id
    msg_id = query.message.id
    url = saved["download_url"]
    thumbnail = saved["thumb"]
    title = saved["title"]
    v = saved["selected_video"]
    a = saved["selected_audio"]

    folder = os.path.join("DKBOTZ", str(user_id), str(msg_id))
    os.makedirs(folder, exist_ok=True)

    if not isinstance(a, list):
        a = [a] if a else []

    a = [str(i).strip() for i in a if str(i).strip()]

    if len(a) > 1:
        audio_fmt = "+".join(a)
    elif len(a) == 1:
        audio_fmt = a[0]
    else:
        audio_fmt = ""

    if v and audio_fmt:
        fmt = f"{v}+{audio_fmt}"
    elif v:
        fmt = v
    elif audio_fmt:
        fmt = audio_fmt
    else:
        fmt = "best"

    safe_title = "".join(x for x in title if x not in '\\/:*?"<>|').strip()
    output = os.path.join(folder, f"{safe_title}.%(ext)s")

    cmd = [
        "yt-dlp",
        "-f", fmt,
        "-o", output,
        "--newline",
        "--progress",
        "--no-warnings",
        "--restrict-filenames",
        url
    ]
    if len(a) > 1:
        cmd.extend(["--audio-multistreams"])

    async def safe_edit(text):
        try:
            await query.message.edit_text(text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await query.message.edit_text(text)
            except:
                pass
        except:
            pass

    async def safe_reply(text):
        try:
            await query.message.reply_text(text)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await query.message.reply_text(text)
            except:
                pass
        except:
            pass

    async def safe_delete():
        try:
            await query.message.delete()
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                await query.message.delete()
            except:
                pass
        except:
            pass

    async def run_download():
        try:
            audio_text = ", ".join(a) if a else "None"
            await safe_edit(
                f"<b>🚀 Preparing Download...</b>\n\n"
                f"<b>🎥 Video:</b> <code>{v if v else 'None'}</code>\n"
                f"<b>🎵 Audio:</b> <code>{audio_text}</code>"
            )

            process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)

            last_update = 0
            last_text = ""
            frag_mode = False
            frag_current = 0
            frag_total = 0

            while True:
                line = await process.stdout.readline()
                if not line:
                    break

                text = line.decode(errors="ignore").strip()

                if "ERROR:" in text:
                    return await safe_edit(f"<b>❌ Error</b>\n<code>{text[:350]}</code>")

                if "[download]" not in text:
                    continue

                frag = re.search(r'frag\s+(\d+)/(\d+)', text)
                if frag:
                    frag_mode = True
                    frag_current = int(frag.group(1))
                    frag_total = int(frag.group(2))

                percent = re.search(r'(\d+\.\d+)%', text)
                total = re.search(r'of\s+~?\s*([^\s]+)', text)
                speed = re.search(r'at\s+([^\s]+)', text)
                eta = re.search(r'ETA\s+([^\s]+)', text)

                raw_percent = float(percent.group(1)) if percent else 0.0
                total_size = total.group(1) if total else "Unknown"
                speed_val = speed.group(1) if speed else "0B/s"
                eta_val = eta.group(1) if eta else "Calculating"

                if frag_mode and frag_total > 0:
                    overall = ((frag_current - 1) + (raw_percent / 100)) / frag_total * 100
                    show_percent = min(overall, 99.9)
                else:
                    show_percent = raw_percent

                if "100%" in text and frag_mode and frag_current < frag_total:
                    continue

                if frag_mode and frag_current >= frag_total and raw_percent >= 100:
                    show_percent = 100.0

                bar_count = int(show_percent / 10)
                bar = "▓" * bar_count + "░" * (10 - bar_count)

                frag_text = f"\n<b>🧩 Parts:</b> <code>{frag_current}/{frag_total}</code>" if frag_mode else ""
                audio_line = f"\n<b>🎵 Tracks:</b> <code>{len(a)}</code>" if a else ""

                show = (
                    f"<b>📥 Downloading...</b>\n\n"
                    f"<code>[{bar}] {show_percent:.1f}%</code>\n\n"
                    f"<b>📦 Size:</b> <code>{total_size}</code>\n"
                    f"<b>⚡ Speed:</b> <code>{speed_val}</code>\n"
                    f"<b>⏳ ETA:</b> <code>{eta_val}</code>"
                    f"{audio_line}"
                    f"{frag_text}"
                )

                now = time.time()
                if show != last_text and now - last_update >= 2:
                    await safe_edit(show)
                    last_text = show
                    last_update = now

            code = await process.wait()

            if code != 0:
                return await safe_edit("<b>❌ Download Failed</b>")

            files = glob.glob(os.path.join(folder, "*"))
            files = [x for x in files if os.path.isfile(x)]

            if not files:
                return await safe_edit("<b>❌ File Not Found</b>")

            await safe_edit(f"<b>✅ Download Completed</b>\n\n<b>📁 Total Files:</b> <code>{len(files)}</code>\n<b>🎵 Audio Tracks:</b> <code>{len(a)}</code>\n\n<b>🚀 Uploading Starting...</b>")
            for file_path in files:
                try:
                    size = os.path.getsize(file_path)
                    file_name = os.path.basename(file_path)
                    file_size = humanbytes(size)
                    await safe_edit(f"<b>📤 Uploading File...</b>\n\n<b>📁 Name:</b> <code>{file_name}</code>\n<b>📦 Size:</b> <code>{file_size}</code>")
                    duration, width, height = await get_video_metadata(file_path)
                    if thumbnail:
                        width, height, dkthumbs = await fix_thumb(thumbnail)

                    start_time = time.time()
                    caption = f"<b>📁 Name:</b> <code><b>{file_name}</code>\n\n<b>📦 Size:</b> <code>{file_size}</code>"
                    dkcopy = await client.send_video(chat_id=query.message.chat.id, video=file_path, caption=caption, duration=duration if duration > 0 else None, width=width if width > 0 else None, height=height if height > 0 else None, thumb=dkthumbs if dkthumbs else None, progress=progress_for_pyrogram, progress_args=("📤 <b>Uploading Video...</b>", query.message, start_time))
                    await increment_downloads(query.from_user.id)
                    
                    if LOG_CHANNEL:
                        user = query.from_user
                        log_msg=f"📥 <b>New Video Uploaded</b>\n👤 <b>User:</b> {user.mention if user else 'Unknown'}\n🆔 <b>ID:</b> <code>{user.id if user else 0}</code>\n📛 <b>Username:</b> {'@'+user.username if user and user.username else 'No Username'}"
                        try:
                            log = await dkcopy.copy(LOG_CHANNEL)
                            await log.reply(log_msg)
                        except Exception as e:
                            pass

                    await safe_edit(f"<b>📤 Uploading Done...</b>\n\n<b>📁 Name:</b> <code>{file_name}</code>\n<b>📦 Size:</b> <code>{file_size}</code>")
                    await asyncio.sleep(2)
                    await remove_file(file_path)
                    if thumbnail:
                        await remove_file(dkthumbs)

                except Exception as e:
                    await safe_reply(f"<b>❌ Upload Failed</b>\n\n<b>📁 File:</b> <code>{os.path.basename(file_path)}</code>\n<b>⚠️ Error:</b> <code>{str(e)}</code>")
                    await remove_file(file_path)
                    if thumbnail:
                        await remove_file(dkthumbs)

            await safe_delete()
            await remove_folder(folder)

        except FileNotFoundError:
            await safe_edit("<b>❌ yt-dlp Not Installed</b>")

        except Exception as e:
            await safe_edit(f"<b>❌ Failed</b>\n<code>{str(e)[:350]}</code>")

    asyncio.create_task(run_download())


@DKBOTZBOT.on_callback_query(filters.regex("^select"))
async def all_select_callbacks(client, query):
    try:
        parts = query.data.split("_")
        user_id = query.from_user.id
        action = parts[1]
        msg_id = int(parts[2])
        saved = USER_DATA.get(user_id, {}).get(msg_id)

        if not saved:
            return await query.answer("Expired", True)

        def build_audio_buttons(msg_id, audios, selected_ids):
            rows = []
            for item in audios[:25]:
                if len(item) == 3:
                    afid, q, lang = item
                else:
                    afid, q = item

                mark = "✅" if afid in selected_ids else "☑️"
                rows.append([InlineKeyboardButton(f"{mark} 🎵 {q}", callback_data=f"select_audio_{msg_id}_{afid}")])

            rows.append([
                InlineKeyboardButton("⏭ Skip Audio", callback_data=f"select_skip_{msg_id}"),
                InlineKeyboardButton("🚀 Download", callback_data=f"select_done_{msg_id}")
            ])
            return InlineKeyboardMarkup(rows)

        if action == "video":
            fid = "_".join(parts[3:])
            saved["selected_video"] = fid
            audios = saved.get("audios", [])

            if not audios:
                saved["selected_audio"] = []
                return await start_download(client, query, saved)

            if "selected_audio" not in saved or not isinstance(saved["selected_audio"], list):
                first_audio = audios[0][0] if audios else None
                saved["selected_audio"] = [first_audio] if first_audio else []

            if len(audios) == 1:
                return await start_download(client, query, saved)

            return await query.message.edit_reply_markup(build_audio_buttons(msg_id, audios, saved["selected_audio"]))

        elif action == "audio":
            fid = "_".join(parts[3:])

            if "selected_audio" not in saved or not isinstance(saved["selected_audio"], list):
                saved["selected_audio"] = []

            if fid in saved["selected_audio"]:
                saved["selected_audio"].remove(fid)
            else:
                saved["selected_audio"].append(fid)

            return await query.message.edit_reply_markup(build_audio_buttons(msg_id, saved.get("audios", []), saved["selected_audio"]))

        elif action == "skip":
            saved["selected_audio"] = []
            return await start_download(client, query, saved)

        elif action == "done":
            if "selected_audio" not in saved or not isinstance(saved["selected_audio"], list):
                saved["selected_audio"] = []

            return await start_download(client, query, saved)

        else:
            return await query.answer("Unknown Action", True)

    except Exception as e:
        return await query.answer(str(e), True)

@DKBOTZBOT.on_message(filters.text & filters.private)
async def dkbotz_handle_link(client, message):
    user = message.from_user
    if DB_ENABLED:
        join = await add_user(user)
        if join and LOG_CHANNEL:
            await client.send_message(LOG_CHANNEL, f"🚀 <b>New User Started The Bot</b>\n👤 <b>Name :</b> {user.first_name or 'Unknown'} {user.last_name or ''}\n🆔 <b>User ID :</b> <code>{user.id}</code>\n🔗 <b>Username :</b> {'@' + user.username if user.username else 'Not Set'}\n🌍 <b>Language :</b> {user.language_code or 'Unknown'}\n🤖 <b>Bot :</b> {'Yes' if user.is_bot else 'No'}\n⏰ <b>Time :</b> <code>{datetime.now().strftime('%d %B %Y %I:%M:%S %p')}</code>")
        if await is_banned(user.id):
            return await message.reply_text("<b>🚫 Sorry, You Are Banned From Using This Bot.</b>")

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

    full_title = dkbotz_mx_data.get("full_title", "Video")
    description = dkbotz_mx_data.get("description", "")
    thumb = dkbotz_mx_data.get("thumbnail", "")

    try:
        with yt_dlp.YoutubeDL({"quiet": True, "nocheckcertificate": True}) as ydl:
            info = ydl.extract_info(download_url, download=False)

        fmts = info.get("formats", [])
        videos = []
        audios = []

        for f in fmts:
            fid = str(f.get("format_id"))
            vcodec = f.get("vcodec")
            acodec = f.get("acodec")
            h = f.get("height")
            ext = f.get("ext", "mp4")
            abr = f.get("abr")

            if vcodec != "none":
                q = f"{h}p" if h else ext.upper()
                videos.append((fid, q))

            if vcodec == "none" and acodec != "none":
                lang = f.get("language") or f.get("language_preference") or "Unknown"
                q = f"{int(abr)}kbps [{lang}]" if abr else f"{ext.upper()} [{lang}]"
                audios.append((fid, q))

        videos = list(dict.fromkeys(videos))
        audios = list(dict.fromkeys(audios))

    except:
        return await checking.edit_text("<b>❌ Failed To Read Formats</b>")

    USER_DATA.setdefault(message.from_user.id, {})
    USER_DATA[message.from_user.id][message.id] = {"url": url, "download_url": download_url, "title": full_title, "thumb": thumb, "videos": videos, "audios": audios, "selected_video": None, "selected_audio": audios[0][0] if audios else None}

    btn = []
    for fid, q in videos[:25]:
        btn.append([InlineKeyboardButton(f"🎥 {q}", callback_data=f"select_video_{message.id}_{fid}")])

    text = f"<b>🎬 Full Title:</b> {full_title}\n\n<b>📝 Description:</b>\n{description[:300]}..."

    if thumb:
        await message.reply_photo(thumb, caption=text, reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply_text(text, reply_markup=InlineKeyboardMarkup(btn))

    await checking.delete()



DKBOTZBOT.run()
