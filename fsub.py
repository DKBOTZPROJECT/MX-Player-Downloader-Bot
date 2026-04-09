from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from Config import *

async def ForceSub(client, message):
    if not FSUB_CHANNEL:
        return True

    try:
        invite_link = await client.create_chat_invite_link(chat_id=(int(FSUB_CHANNEL) if str(FSUB_CHANNEL).startswith("-100") else FSUB_CHANNEL))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        invite_link = await client.create_chat_invite_link(chat_id=(int(FSUB_CHANNEL) if str(FSUB_CHANNEL).startswith("-100") else FSUB_CHANNEL))
    except Exception as err:
        print(f"DKBOTZ FSUB Error: {err}")
        return True

    try:
        user = await client.get_chat_member(chat_id=(int(FSUB_CHANNEL) if str(FSUB_CHANNEL).startswith("-100") else FSUB_CHANNEL), user_id=message.from_user.id)
        if user.status == "kicked":
            await client.send_message(chat_id=message.from_user.id, text="<b>🚫 Sorry Sir, You Are Banned To Use Bot. Contact Support.</b>", disable_web_page_preview=True)
            return False

        return True

    except UserNotParticipant:
        global BOT_USERNAME

        if not BOT_USERNAME:
            me = await client.get_me()
            BOT_USERNAME = me.username

        buttons = [
            [InlineKeyboardButton("🤖 Join DKBOTZ Updates Channel ✔️", url=invite_link.invite_link)],
            [InlineKeyboardButton("🔄 Refresh 🔄", url=f"https://t.me/{BOT_USERNAME}?start=help")]
        ]

        await client.send_message(chat_id=message.from_user.id, text="<b>⚡️ Please Join Our Updates Channel To Use This Bot!\n\n🔥 Only Subscribers Can Use This Bot Due To High Load!</b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
        return False

    except Exception as err:
        print(f"DKBOTZ FSUB Check Error: {err}")
        return True
