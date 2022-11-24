from config import dp
from aiogram import executor
from utils import registration, menu, time_slot

# TODO:
#   1. Setting English level
#   2. Setting users' timeslots


async def on_startup(_):
    print('The bot is online!')


if __name__ == '__main__':
    registration.register_handlers_registration(dp)
    time_slot.register_handlers_time_slot(dp)
    menu.register_handlers_menu(dp)
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
