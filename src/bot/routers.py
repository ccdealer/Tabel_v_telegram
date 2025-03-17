
from src.bot.handlers.master import master_router
from src.bot.handlers.tabel_router import tabel_router

ROUTERS = [
    master_router,
    tabel_router
] #сюда через запятую грузим ветки диалогов