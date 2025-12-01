import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from config import BOT_TOKEN
from db import init_db, get_user_topics, save_user_topics
from utils import topics_keyboard
from scheduler import scheduler


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    topics = await get_user_topics(user_id)
    await message.answer(
        "Обери теми новин (можна змінити в будь-який момент):",
        reply_markup=topics_keyboard(topics),
    )


@dp.callback_query(lambda c: c.data and c.data.startswith("toggle_"))
async def toggle_topic(cb: types.CallbackQuery):
    user_id = cb.from_user.id
    topic = cb.data.split("_", 1)[1]

    topics = await get_user_topics(user_id)

    if topic in topics:
        topics.remove(topic)
    else:
        topics.append(topic)

    await save_user_topics(user_id, topics)

    await cb.message.edit_reply_markup(
        reply_markup=topics_keyboard(topics)
    )
    await cb.answer()


@dp.callback_query(lambda c: c.data == "done")
async def done(cb: types.CallbackQuery):
    await cb.message.edit_text("Готово! Новини надходитимуть кожні 30 хв.")
    await cb.answer()


async def main():
    await init_db()
    # Запускаємо планувальник в бекграунді
    asyncio.create_task(scheduler(bot))

    print("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
