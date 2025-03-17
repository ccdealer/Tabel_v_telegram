import logging
from logging.config import dictConfig

from aiogram import Bot, Dispatcher

from dotenv import dotenv_values

config = dotenv_values()
BOT_TOKEN:str = config.get("BOT_TOKEN")  #Забираем значение токена бота 

bot: Bot = Bot(token=BOT_TOKEN) #Инициализируем бота с токеном БОТ_ТОКЕН
dp: Dispatcher = Dispatcher() #Пока хз что это и как работает но штука нужная

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "detailed",
        },
    },
    "formatters": {
        "detailed": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
} 
#Собственно сам логгер

dictConfig(LOGGING) #Что и зачем разобраться надо
logger = logging.getLogger(__name__)
