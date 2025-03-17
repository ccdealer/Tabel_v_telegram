from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message , InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from src.bot.states import TabelStates
from src.settings.base import  logger


master_router = Router()

@master_router.message(CommandStart()) #бот реагирует на /start
async def start_comand(message: Message, state: FSMContext):
    start = InlineKeyboardButton(text="Начало смены", callback_data="beg")
    finish = InlineKeyboardButton(text="Конец смены", callback_data="fin")
    markup = InlineKeyboardMarkup(inline_keyboard = [[start],[finish]])
    await state.set_state(state=TabelStates.CHS_position)
    await message.answer(text="Выберите", reply_markup=markup)