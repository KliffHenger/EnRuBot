from aiogram.dispatcher.filters.state import StatesGroup, State


class Reg(StatesGroup):
    user_name = State()
    user_surname = State()
    user_email = State()
    user_eng_level = State()
