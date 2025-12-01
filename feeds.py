import feedparser
import hashlib
import asyncio
import json

from config import KEYWORDS
from db import is_posted, mark_posted
from translator import translate_fr_to_uk


async def parse_feed(bot, users, url: str, topic: str, translate: bool = False):
    """
    Парсить один RSS-фід, фільтрує за KEYWORDS і розсилає новину користувачам.
    """
    try:
        feed = feedparser.parse(url)
        if not feed.entries:
            return

        # Беремо тільки першу новину (за бажанням можна зробити декілька)
        entry = feed.entries[0]
        title = getattr(entry, "title", "")
        summary = getattr(entry, "summary", "")[:200]
        link = getattr(entry, "link", "")

        if translate:
            title = await translate_fr_to_uk(title)
            summary = await translate_fr_to_uk(summary)

        text = f"{title} {summary}".lower()
        keywords = KEYWORDS.get(topic, [])

        if keywords and not any(w.lower() in text for w in keywords):
            # Якщо є ключові слова і жодне не знайдено – пропускаємо
            return

        # Хеш, щоб не дублювати одну й ту ж новину
        h = hashlib.md5(f"{topic}_{link}".encode()).hexdigest()
        if await is_posted(h):
            return

        msg = f"*{title}*\n\n{summary}...\n\n[Читати →]({link})"
        if translate:
            msg += "\n\n_Перекладено з RFI (Франція)_"

        # Розсилка всім, хто підписаний на тему
        for user_id, topics_json in users:
            user_topics = json.loads(topics_json)
            if topic in user_topics:
                try:
                    await bot.send_message(
                        user_id,
                        msg,
                        parse_mode="Markdown",
                        disable_web_page_preview=True,
                    )
                    await asyncio.sleep(0.5)
                except Exception:
                    # Можна додати логування
                    pass

        await mark_posted(h)

    except Exception as ex:
        print(f"ERROR parsing feed {url}: {ex}")
