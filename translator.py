import httpx
import asyncio


async def translate_fr_to_uk(text: str) -> str:
    """
    Переклад тексту з FR → UK через LibreTranslate з до 3 спробами.
    Якщо сервіс недоступний – повертаємо оригінал.
    """
    if not text:
        return text

    for _ in range(3):
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(
                    "https://libretranslate.de/translate",
                    json={
                        "q": text,
                        "source": "fr",
                        "target": "uk",
                        "format": "text",
                    },
                )
                data = resp.json()
                return data.get("translatedText", text)
        except Exception:
            await asyncio.sleep(1)

    return text
