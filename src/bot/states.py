from aiogram.fsm.state import State, StatesGroup

class TabelStates(StatesGroup):
    CHS_position = State()
    CHS_person = State()
    Final_proces = State()
