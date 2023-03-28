from aiogram.dispatcher.filters.state import StatesGroup, State


class Reg(StatesGroup):
    user_name = State()
    user_surname = State()
    user_email = State()
    user_eng_level = State()
    user_utc = State()

class TimeSlot(StatesGroup):
    week_day = State()
    start_time = State()
    # end_time = State() - раскомментить если понадобится

class TS(StatesGroup):
    time_slot = State()



