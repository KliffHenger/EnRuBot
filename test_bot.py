from config import bot, dp
from aiogram.utils import executor
from utils import registration, menu, time_slot, find_interlocutor, hour_goal, english_level, sending_messages
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from airtable_config import msg_table, table
from datetime import datetime, timedelta
from keyboards.inline_menu import G_MENU


async def every_week():
    all_table = table.all()
    msg_tb = msg_table.get('recBy0uFnTEUzz3U2')
    for index in range(len(all_table)):
        tg_id = all_table[index]['fields']['UserIDTG']
        last = all_table[index]['fields']['LastFindPeer'] # 2023-04-05 16:42:43 но это просто строка
        text_msg = msg_tb['fields']['Text']
        if last == 'None': # сюда попадают все, кто ни разу никого не искал
            try:
                await bot.send_message(int(tg_id), text=text_msg, reply_markup=G_MENU)
            except:
                pass
        else: # сюда попадают те, кто долго не искали собеседника
            silent_week = datetime.now() - timedelta(days=7) # указать то кол-во дней простоя которое нужно (сейчас 7 дней)
            last_time_find = datetime.strptime(last, '%Y-%m-%d %H:%M:%S')
            if last_time_find < silent_week:
                try:
                    await bot.send_message(int(tg_id), text=text_msg, reply_markup=G_MENU)
                except:
                    pass



async def on_startup(_):
    print('The bot is online!')
    print(datetime.now())
    sched = AsyncIOScheduler()
    sched.add_job(every_week, trigger='interval', minutes=5, misfire_grace_time=60) # строчка для тестов
    # sched.add_job(every_week, trigger='cron', day_of_week=0, hour=18, misfire_grace_time=60) # рабочая строчка
    sched.start()
    sched.print_jobs()
 


"""Регистрация всех хэндлеров"""
sending_messages.register_handlers_send_msg(dp)
registration.register_handlers_registration(dp)
time_slot.register_handlers_time_slot(dp)
menu.register_handlers_menu(dp)
find_interlocutor.register_handlers_find_interlocutor(dp)
hour_goal.register_handlers_hour_goal(dp)
english_level.register_handlers_english_level(dp)




if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
