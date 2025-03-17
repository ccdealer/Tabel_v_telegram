import asyncio  #библиотека ассинхронных процессов

from src.settings.base import bot, dp, logger #импортируем логгер бота и диспетчер
from src.bot.routers import ROUTERS #ветки ботов
import datetime
import time
from src.settings.db_init import beg_and_fin
from apscheduler.schedulers.background import BackgroundScheduler
from aiogram.types import FSInputFile

async def main():
    # dp.include_router(*ROUTERS)
    for router in ROUTERS:  # Подключаем каждый роутер отдельно
        dp.include_router(router)
    scheduler = BackgroundScheduler()
    scheduler.add_job(beg_and_fin, 'cron', day = 1, hour = 0, minute = 0)

    scheduler.start()
    logger.info(msg="Bot started")
    await dp.start_polling(bot)

# def sender()

if __name__ == "__main__":
    asyncio.run(main=main())
