from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOPICS, RFI_FEEDS


def topics_keyboard(selected=None) -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для вибору тем.
    """
    if selected is None:
        selected = []

    all_topics = {**TOPICS, **RFI_FEEDS}
    kb = []

    for t in all_topics:
        emoji = "✅" if t in selected else "⬜"
        kb.append([
            InlineKeyboardButton(
                text=f"{emoji} {t}",
                callback_data=f"toggle_{t}"
            )
        ])

    kb.append([
        InlineKeyboardButton(text="Готово ✅", callback_data="done")
    ])

    return InlineKeyboardMarkup(inline_keyboard=kb)
