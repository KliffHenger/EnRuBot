from config import dp #, scheduler
from aiogram.utils import executor
from utils import registration, menu, time_slot, find_interlocutor, hour_goal, statistics





async def on_startup(_):
    print('The bot is online!')
    # scheduler.start()                   # эта штука хранит задачи


"""Регистрация всех хэндлеров"""
registration.register_handlers_registration(dp)
time_slot.register_handlers_time_slot(dp)
menu.register_handlers_menu(dp)
find_interlocutor.register_handlers_find_interlocutor(dp)
hour_goal.register_handlers_hour_goal(dp)
# statistics.register_handlers_statistics(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
