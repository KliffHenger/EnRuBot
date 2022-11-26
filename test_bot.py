from config import dp
from aiogram.utils import executor
from utils import registration, menu, time_slot, find_interlocutor


# TODO:
#   1. Setting English level
#   2. Setting users' timeslots

async def on_startup(_):
    print('The bot is online!')

registration.register_handlers_registration(dp)
time_slot.register_handlers_time_slot(dp)
menu.register_handlers_menu(dp)
find_interlocutor.register_handlers_find_interlocutor(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
