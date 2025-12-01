import os
from dotenv import load_dotenv

# Завантажуємо .env для локального запуску (на Railway змінні прийдуть з оточення)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_NAME = "users.db"

if not BOT_TOKEN:
    print("BOT_TOKEN не налаштовано! Перевір .env або Variables на Railway.")
    # Не робимо exit тут, щоб Railway не падав безкінечно, але попереджаємо в логах.

# ─── ФІДИ ───────────────────
TOPICS = {
    "Політика": [
        "https://www.holosameryky.com/api/zroyml-vomx-tpeokt_",
        "https://feeds.bbci.co.uk/ukrainian/politics/rss.xml",
    ],
    "Війна": [
        "https://www.holosameryky.com/api/z_ygqil-vomx-tpevrbqp",
        "https://feeds.bbci.co.uk/ukrainian/war/rss.xml",
    ],
    "Наука": [
        "https://www.holosameryky.com/api/ztmvqpl-vomx-tpek-uqp",
        "https://feeds.bbci.co.uk/ukrainian/science/rss.xml",
    ],
    "Спорт": [
        "https://www.holosameryky.com/api/z-oyrl-vomx-tpergtq",
        "https://feeds.bbci.co.uk/ukrainian/sport/rss.xml",
    ],
    "Економіка": [
        "https://www.holosameryky.com/api/z-vmqtl-vomx-tperovqr",
        "https://feeds.bbci.co.uk/ukrainian/business/rss.xml",
    ],
    "Культура": [
        "https://www.holosameryky.com/api/z_kbqvl-vomx-tpevpoov",
        "https://feeds.bbci.co.uk/ukrainian/culture/rss.xml",
    ],
}

RFI_FEEDS = {
    "Міжнародне": "https://www.rfi.fr/fr/monde/rss",
    "Європа": "https://www.rfi.fr/fr/europe/rss",
}

KEYWORDS = {
    "Політика": ["зеленський", "рада"],
    "Війна": ["зсу", "фронт"],
    "Наука": ["дослідження", "ai"],
    "Спорт": ["футбол", "матч"],
    "Економіка": ["ввп", "інфляція"],
    "Культура": ["фільм", "книга"],
    "Міжнародне": ["сша", "європа"],
    "Європа": ["єс", "нато"],
}
