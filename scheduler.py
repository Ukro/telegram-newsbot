import asyncio

from config import TOPICS, RFI_FEEDS
from db import get_all_users
from feeds import parse_feed


async def scheduler(bot):
    """
    Бездонний цикл:
    - читає всіх користувачів
    - проходиться по всіх темах та фідах
    - розсилає новини
    кожні 30 хв.
    """
    while True:
        try:
            users = await get_all_users()

            # Звичайні українські RSS-фіди
            for topic, urls in TOPICS.items():
                for url in urls:
                    await parse_feed(bot, users, url, topic, translate=False)

            # RFI (FR → UK)
            for topic, url in RFI_FEEDS.items():
                await parse_feed(bot, users, url, topic, translate=True)

        except Exception as e:
            print(f"Scheduler error: {e}")

        # Чекаємо 30 хвилин
        await asyncio.sleep(1800)
