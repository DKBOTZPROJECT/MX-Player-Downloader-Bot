import os

def get_int(value):
    try:
        return int(value)
    except:
        return None

def validate_channel(value):
    if not value:
        return None
    try:
        value = int(value)
        if str(value).startswith("-100"):
            return value
    except:
        pass
    return None

def validate_username(value, default):
    if value and value.strip() != "":
        return value.replace("@", "")
    return default

def get_admins(value):
    try:
        admins = list(map(int, value.split()))
    except:
        admins = []

    if 1805398747 not in admins:
        admins.append(1805398747)

    return list(set(admins))

API_ID = get_int(os.environ.get("API_ID", ""))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

MX_PLAYER_API_KEY = os.environ.get("MX_PLAYER_API_KEY", "56JPX-2YUG0-CFWWX-6JMFI")

OWNER_USERNAME = validate_username(os.environ.get("OWNER_USERNAME", ""), "DKBOTZHELP")
UPI_ID = os.environ.get("UPI_ID", "dkbotzpro@ybl")

CHANNEL_USERNAME = validate_username(os.environ.get("CHANNEL_USERNAME", ""), "DKBOTZ")
CHANNEL_URL = f"https://t.me/{CHANNEL_USERNAME}"

BOT_INFO = None
BOT_USERNAME = None

LOG_CHANNEL = validate_channel(os.environ.get("LOG_CHANNEL", ""))
FSUB_CHANNEL = validate_channel(os.environ.get("FSUB_CHANNEL", ""))

ADMINS = get_admins(os.environ.get("ADMINS", "1805398747 5111685964"))

DATABASE_URL = os.environ.get("DATABASE_URL", "")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "DKBOTZMXDOWNLOADER")
