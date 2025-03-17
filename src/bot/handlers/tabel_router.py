import json
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message , CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from src.bot.states import TabelStates
import aiofiles
import datetime as dt
from src.bot.handlers.master import start_comand
from src.settings.db_init import add_to_monthly_db
tabel_router = Router()

start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Старт", callback_data="start")]
])

@tabel_router.callback_query(TabelStates.CHS_position, F.data == "beg")
async def choose_position_beg( callback: CallbackQuery, state:FSMContext):
    day24 = InlineKeyboardButton(text="Суточная горничная", callback_data="sut")
    day8 = InlineKeyboardButton(text="Дневная горничная", callback_data="dne")
    laundress = InlineKeyboardButton(text="Прачка", callback_data="lau")
    teh_pers = InlineKeyboardButton(text="Тех персонал", callback_data="teh")
    admin = InlineKeyboardButton(text="Администратор гостиницы", callback_data="adg")
    sauna = InlineKeyboardButton(text = "Администратор сауны",callback_data="ads" )
    slesar = InlineKeyboardButton(text="Техник", callback_data="sle")
    markup = InlineKeyboardMarkup(inline_keyboard=[[day24],[day8],[laundress], [teh_pers], [admin], [sauna], [slesar]])
    await state.set_state(state=TabelStates.CHS_person)
    await state.update_data(data = {"begining": dt.datetime.now().strftime("%H:%M:%S") })
    await callback.message.answer(text="Выберите должность", reply_markup=markup)

@tabel_router.callback_query(TabelStates.CHS_position, F.data == "fin")
async def choose_position_fin( callback: CallbackQuery, state:FSMContext):
    day24 = InlineKeyboardButton(text="Суточная горничная", callback_data="sut")
    day8 = InlineKeyboardButton(text="Дневная горничная", callback_data="dne")
    laundress = InlineKeyboardButton(text="Прачка", callback_data="lau")
    teh_pers = InlineKeyboardButton(text="Тех персонал", callback_data="teh")
    admin = InlineKeyboardButton(text="Администратор гостиницы", callback_data="adg")
    sauna = InlineKeyboardButton(text = "Администратор сауны",callback_data="ads" )
    slesar = InlineKeyboardButton(text="Техник", callback_data="sle")
    markup = InlineKeyboardMarkup(inline_keyboard=[[day24],[day8],[laundress], [teh_pers], [admin], [sauna], [slesar]])
    await state.set_state(state=TabelStates.CHS_person)
    await state.update_data(data = {"finish": dt.datetime.now().strftime("%H:%M:%S") })
    await callback.message.answer(text="Выберите должность", reply_markup=markup)


@tabel_router.callback_query(TabelStates.CHS_person)
async def choose_pers_start(callback:CallbackQuery, state: FSMContext):
    await state.update_data(data={"type":callback.data})
    temp = []
    with open("personal.txt", "r", encoding="UTF-8") as p:
        lines = p.readlines()  # Читаем все строки в список
        for line in lines:
            line = line.strip()  # Убираем лишние пробелы и \n
            button = InlineKeyboardButton(text=line, callback_data=line)  # ✅ Создаём кнопку
            temp.append([button])
    markup = InlineKeyboardMarkup(inline_keyboard=temp)
    await state.set_state(state=TabelStates.Final_proces)
    await state.update_data(data={"position" : f"{callback.data}" })
    await callback.message.answer(text= "Выберите своё имя", reply_markup=markup)

@tabel_router.callback_query(TabelStates.Final_proces)
async def final(callback:CallbackQuery, state: FSMContext):
    await state.update_data(data={"person": callback.data})
    data = await state.get_data()
    post = data.get("type")
    pers = data.get("person")
    tip = data.get("begining")
    if tip != None:
        # await add_to_monthly_db(post=post,name= pers, zakr= "False", begining=tip )
        text = await add_to_monthly_db(post=post,name= pers, zakr= "False", begining=tip )
    elif tip == None:
        tip = data.get("finish")
        # await add_to_monthly_db(post=post, name=pers,finish= tip, zakr="True")
        text = await add_to_monthly_db(post=post, name=pers,finish= tip, zakr="True")
    await callback.message.answer(text=text)
    await state.clear()  # Очищаем состояние (начинаем заново)
    await start_comand(callback.message, state)
