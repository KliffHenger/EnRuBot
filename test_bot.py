from config import dp
from aiogram import executor
from utils import registration, menu


async def on_startup(_):
    print('The bot is online!')


if __name__ == '__main__':
    registration.register_handlers_registration(dp)
    menu.register_handlers_menu(dp)
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
