from config import bot, dp
from aiogram.utils import executor
from utils import registration, menu, time_slot, find_interlocutor, hour_goal, english_level
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from airtable_config import msg_table, table
from datetime import datetime


async def every_week():
    all_table = table.all()
    for index in range(len(all_table)):
        tg_id = all_table[index]['fields']['UserIDTG']
        last = all_table[index]['fields']['LastFindPeer']
        time_now = datetime.now()




        if all_table[index]['fields']['DayLife'] == 0:
            tg_id = all_table[index]['fields']['UserTGID']
            record_id = all_table[index]['id']
            quantity_day = int(all_table[index]['fields']['DayLife'])-1
            table.update(record_id=record_id, fields={'DayLife': str(quantity_day)})
            print(tg_id +' -1 день использования сервиса')
        elif int(all_table[index]['fields']['DayLife']) == 0:
            tg_id = all_table[index]['fields']['UserTGID']
            try:
                job_name = all_table[index]['fields']['JobName']
                record_id = all_table[index]['id']
                globals()[job_name].shutdown(wait=False) # отключение планировщика
                table.update(record_id=str(record_id), fields={'JobName': 'None'})
            except:
                pass
            try:
                await bot.send_message(int(tg_id), text=f'Дальнейшее использование нашего сервиса возможно только после уплаты \
абонентской платы в размере - 20 BYN за 30 дней (сумма не окончательна и обсуждению подлежит).\n\
Для уплаты или обсуждения суммы необходимо связаться с автором, перейдя в пункт меню /help', reply_markup=MENU)
            except:
                pass

async def on_startup(_):
    print('The bot is online!')
    print(datetime.now())
 


"""Регистрация всех хэндлеров"""
registration.register_handlers_registration(dp)
time_slot.register_handlers_time_slot(dp)
menu.register_handlers_menu(dp)
find_interlocutor.register_handlers_find_interlocutor(dp)
hour_goal.register_handlers_hour_goal(dp)
english_level.register_handlers_english_level(dp)



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
