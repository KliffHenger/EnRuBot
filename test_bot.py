from config import bot, dp, sched
from aiogram.utils import executor
from utils import registration, menu, time_slot, english_level, sending_messages, restart_active_jobs, connect
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

async def every_hour():
    all_table = table.all()
    for index in range(len(all_table)):
        s_TS = all_table[index]['fields']['ServerTimeSlot']
        record_id = all_table[index]['id']
        time_now = datetime.now()
        if s_TS != 'None':
            server_user_time = datetime.strptime(s_TS, '%Y-%m-%d %H:%M:%S')
            if time_now >= server_user_time:
                table.update(record_id, {'ServerTimeSlot': 'None'})
                table.update(record_id, {'UserTimeSlot': 'None'})




async def on_startup(_):
    print('The bot is online!')
    print(datetime.now())
    sched_regular = AsyncIOScheduler()
    sched_regular.start()
    sched.start()
    # sched.add_job(every_week, trigger='interval', minutes=5, misfire_grace_time=60) # строчка для тестов
    sched_regular.add_job(every_week, trigger='cron', day_of_week=0, hour=18, misfire_grace_time=60) # рабочая строчка
    sched_regular.add_job(every_hour, trigger='interval', minutes=60, misfire_grace_time=60)
    sched_regular.print_jobs()
    await restart_active_jobs.for_rest()
    await restart_active_jobs.restart_jobs()
 


"""Регистрация всех хэндлеров"""
sending_messages.register_handlers_send_msg(dp)                 # функция рассылки сообщений
registration.register_handlers_registration(dp)                 # функция регистрации новых пользователей
time_slot.register_handlers_time_slot(dp)                       # функция установки ТаймСлота
menu.register_handlers_menu(dp)                                 # функция Главного Меню
english_level.register_handlers_english_level(dp)               # функция выбора уровня языка
restart_active_jobs.register_handlers_restart_active_jobs(dp)   # функция перезапуска активных задач планировщиков
connect.register_handlers_connect(dp)                           # функция подбора пары




if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
