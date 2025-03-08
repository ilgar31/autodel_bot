from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
import logging
from config import TOKEN, ADMINS
from handlers import router  # Импортируем роутер из handlers/__init__.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import get_non_working_hours_requests, delete_non_working_hours_requests

logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Подключаем роутеры
dp.include_router(router)

# Создаем планировщик
scheduler = AsyncIOScheduler()

async def notify_admins_about_non_working_hours_requests():
    requests = get_non_working_hours_requests()
    if requests:
        for admin_id in ADMINS:
            await bot.send_message(
                admin_id,
                "Пользователи, которые хотели связаться в нерабочее время:\n" +
                "\n".join([f"@{username}" for user_id, username in requests])
            )
        delete_non_working_hours_requests()

async def on_startup():
    # Запускаем планировщик
    scheduler.add_job(
        notify_admins_about_non_working_hours_requests,
        "cron",
        hour=8,
        minute=0,
        timezone="Europe/Moscow"  # Укажите вашу временную зону
    )
    scheduler.start()

async def on_shutdown():
    # Останавливаем планировщик при завершении работы бота
    scheduler.shutdown()

if __name__ == "__main__":
    import asyncio

    # Запускаем бота и планировщик
    loop = asyncio.get_event_loop()
    loop.run_until_complete(on_startup())  # Запускаем планировщик
    try:
        loop.run_until_complete(dp.start_polling(bot))  # Запускаем бота
    finally:
        loop.run_until_complete(on_shutdown())  # Останавливаем планировщик