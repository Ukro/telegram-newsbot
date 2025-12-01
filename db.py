import aiosqlite
import json
from config import DB_NAME


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                topics TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS posted (
                hash TEXT PRIMARY KEY
            )
        """)
        await db.commit()


async def get_user_topics(user_id: int) -> list:
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT topics FROM users WHERE user_id=?", (user_id,))
        row = await cursor.fetchone()
        return json.loads(row[0]) if row else []


async def save_user_topics(user_id: int, topics: list):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR REPLACE INTO users(user_id, topics) VALUES (?, ?)",
            (user_id, json.dumps(topics))
        )
        await db.commit()


async def is_posted(hash_code: str) -> bool:
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT 1 FROM posted WHERE hash=?", (hash_code,))
        return await cursor.fetchone() is not None


async def mark_posted(hash_code: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT INTO posted(hash) VALUES (?)", (hash_code,))
        await db.commit()


async def get_all_users():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT user_id, topics FROM users")
        return await cursor.fetchall()
