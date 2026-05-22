import logging
from datetime import datetime, timezone
from pymongo import MongoClient
from Config import DATABASE_URL, DATABASE_NAME

logger = logging.getLogger(__name__)

DB_ENABLED = False

if DATABASE_URL and DATABASE_URL.startswith("mongodb"):
    try:
        client = MongoClient(DATABASE_URL)
        db = client[DATABASE_NAME]

        users_col = db.users
        stats_col = db.bot_stats

        users_col.create_index("user_id", unique=True)

        DB_ENABLED = True
        logger.info("Database Connected")

    except Exception as e:
        logger.error(f"Database Error : {e}")

else:
    logger.warning("DATABASE_URL Missing")


async def add_user(user):
    if not DB_ENABLED:
        return False

    try:
        if users_col.find_one({"user_id": user.id}):
            return False

        users_col.insert_one({
            "user_id": user.id,
            "joined_at": datetime.now(timezone.utc),
            "is_banned": False,
            "downloads": 0
        })

        return True

    except Exception as e:
        logger.error(f"Add User Error : {e}")
        return False


async def is_banned(user_id):
    if not DB_ENABLED:
        return False

    try:
        data = users_col.find_one({"user_id": user_id}, {"is_banned": 1})
        return bool(data and data.get("is_banned"))

    except Exception as e:
        logger.error(f"Is Banned Error : {e}")
        return False


async def ban_user(user_id):
    if not DB_ENABLED:
        return False

    try:
        result = users_col.update_one({"user_id": user_id}, {"$set": {"is_banned": True}})
        return result.modified_count > 0

    except Exception as e:
        logger.error(f"Ban User Error : {e}")
        return False


async def unban_user(user_id):
    if not DB_ENABLED:
        return False

    try:
        result = users_col.update_one({"user_id": user_id}, {"$set": {"is_banned": False}})
        return result.modified_count > 0

    except Exception as e:
        logger.error(f"Unban User Error : {e}")
        return False


async def increment_downloads(user_id):
    if not DB_ENABLED:
        return

    try:
        users_col.update_one({"user_id": user_id}, {"$inc": {"downloads": 1}}, upsert=True)
        stats_col.update_one({"_id": "global"}, {"$inc": {"total_downloads": 1}}, upsert=True)

    except Exception as e:
        logger.error(f"Increment Downloads Error : {e}")


async def get_stats():
    if not DB_ENABLED:
        return {}

    try:
        total_users = users_col.count_documents({})
        banned_users = users_col.count_documents({"is_banned": True})

        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

        new_today = users_col.count_documents({"joined_at": {"$gte": today}})

        stats = stats_col.find_one({"_id": "global"}) or {}

        return {
            "total_users": total_users,
            "active_users": total_users - banned_users,
            "banned_users": banned_users,
            "new_today": new_today,
            "total_downloads": stats.get("total_downloads", 0)
        }

    except Exception as e:
        logger.error(f"Get Stats Error : {e}")
        return {}


async def get_all_users():
    if not DB_ENABLED:
        return []

    try:
        return [i["user_id"] for i in users_col.find({"is_banned": False}, {"user_id": 1})]

    except Exception as e:
        logger.error(f"Get Users Error : {e}")
        return []
