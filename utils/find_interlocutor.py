from aiogram import types, Dispatcher
from airtable_config import table
from .meeting import createMeeting
from config import bot, dp, week_dict, WEEKDAYS, scheduler
from .menu import menu
from keyboards.inline_menu import G_MENU

from datetime import datetime, timedelta
import asyncio



first_user_record_id = ''
second_user_record_id = ''
first_user_tg_id = ''
second_user_tg_id = ''






@dp.callback_query_handler(text='find_interlocutor')
async def callback_find_companion(message: types.Message):
    find_table = table.all()
    global first_user_record_id
    global second_user_record_id
    global second_user_tg_id
    first_user_record_id, first_user_eng_level, first_user_time_slot, second_user_record_id, second_user_tg_id = '', '', '', '', ''
    global first_user_tg_id
    first_user_tg_id = str(message.from_user.id)
    is_found = False
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            first_user_eng_level = find_table[index]['fields']['UserEngLevel']
            first_user_time_slot = find_table[index]['fields']['UserTimeSlot']
            first_user_fname = find_table[index]['fields']['UserName']
            week = first_user_time_slot[0]+first_user_time_slot[1]
            start_time = first_user_time_slot[2]+first_user_time_slot[3]
            week_for_message = week_dict.get(week)
            first_user_record_id = find_table[index]['id']
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] != str(message.from_user.id) \
                and find_table[index]['fields']['UserEngLevel'] == first_user_eng_level \
                and find_table[index]['fields']['UserTimeSlot'] == first_user_time_slot \
                and find_table[index]['fields']['IsPared'] == 'False':
            second_user_tg_id = str(find_table[index]['fields']['UserIDTG'])
            second_user_fname = find_table[index]['fields']['UserName']
            second_user_record_id = find_table[index]['id']
            is_found = True
    if is_found:
        is_pared_id = first_user_tg_id+second_user_tg_id
        table.update(record_id=str(first_user_record_id), fields={'IsPared': "True"})
        table.update(record_id=str(second_user_record_id), fields={'IsPared': "True"})
        table.update(record_id=str(first_user_record_id), fields={'IsParedID': is_pared_id})
        table.update(record_id=str(second_user_record_id), fields={'IsParedID': is_pared_id})
        await bot.send_message(message.from_user.id, text=f'Для Вас есть собеседник на время {week_for_message}, {start_time}-00.')
        await bot.send_message(message.from_user.id, text=f'Ваш собеседник - {second_user_fname}.', reply_markup=G_MENU)
        await bot.send_message(chat_id=int(second_user_tg_id), text=f'Для Вас есть собеседник на время {week_for_message}, {start_time}-00.')
        await bot.send_message(chat_id=int(second_user_tg_id), text=f'Ваш собеседник - {first_user_fname}.', reply_markup=G_MENU)
        if week_for_message:    # этот кусок кода отвечет за отсрочку выдачи всех последующих сообщений
            search_day = WEEKDAYS.index(week_for_message.lower())  
            time_now = datetime.now()
            date_now = datetime.date(time_now)
            day_now = time_now.weekday()
            different_days = search_day - day_now if day_now < search_day else 7 - day_now + search_day
            date_meet = date_now + timedelta(days=different_days)
            datetime_meet = str(date_meet)+","+str(start_time)+",00,00"
            dt_meet = datetime.strptime(datetime_meet, "%Y-%m-%d,%H,%M,%S")
        
        # scheduler.add_job(send_message_cron, trigger='cron', hour=datetime.now().hour, 
            # minute=datetime.now().minute + 1, start_date=datetime.now(), kwargs={'message': message})
        scheduler.add_job(send_message_cron30, trigger='cron', hour=dt_meet.hour - 1, 
            minute=30, start_date=dt_meet, kwargs={'message': message})
        scheduler.add_job(send_message_cron15, trigger='cron', hour=dt_meet.hour - 1, 
            minute=45, start_date=dt_meet, kwargs={'message': message})
        scheduler.add_job(send_message_cron5, trigger='cron', hour=dt_meet.hour - 1, 
            minute=55, start_date=dt_meet, kwargs={'message': message})
        scheduler.add_job(send_message_cron, trigger='cron', hour=dt_meet.hour, 
            minute=00, start_date=dt_meet, kwargs={'message': message})
        scheduler.add_job(update_cron, trigger='cron', hour=dt_meet.hour, 
            minute=40, start_date=dt_meet, kwargs={'message': message})
    else:
        await bot.send_message(message.from_user.id, text='Извините, мы никого не смогли найти....', reply_markup=G_MENU)
    

async def send_message_cron30(message: types.Message):
    await bot.send_message(chat_id=int(first_user_tg_id), text='Встреча начнется через 30 минут')
    await bot.send_message(chat_id=int(second_user_tg_id), text='Встреча начнется через 30 минут')

async def send_message_cron15(message: types.Message):                                                                  
    await bot.send_message(chat_id=int(first_user_tg_id), text='Встреча начнется через 15 минут')
    await bot.send_message(chat_id=int(second_user_tg_id), text='Встреча начнется через 15 минут')

async def send_message_cron5(message: types.Message):
    await bot.send_message(chat_id=int(first_user_tg_id), text='Встреча начнется через 5 минут')
    await bot.send_message(chat_id=int(second_user_tg_id), text='Встреча начнется через 5 минут')

async def send_message_cron(message: types.Message):
    meeting_link, join_password = createMeeting()
    await bot.send_message(chat_id=int(first_user_tg_id), text=f'Join new meeting: {meeting_link}')
    await bot.send_message(chat_id=int(second_user_tg_id), text=f'Hi! You can join new meeting: {meeting_link}')

async def update_cron(message: types.Message):
    find_table = table.all()
    table.update(record_id=str(first_user_record_id), fields={'IsPared': "False"})
    table.update(record_id=str(second_user_record_id), fields={'IsPared': "False"})
        


async def find_companion(message: types.Message):
    """
    Функция поиска собеседника. Наша цель на данном этапе: найти человека с подходящими
    параметрами. На первом шаге мы ищем двоих пользователей в базе для получения данных.
    После данной операции нам необзодимо провести операцию сравнения. Если параметры языка и времени у
    пользователей совпадают, то они образуют пару. Если нет - бот выводит: 'Извините, мы никого не смогли найти....'.
    Ровно в этот момент их значения поля 'IsPared' в базе становится True.
    По истечению 40 минут (в данной функции пока что одна минута) их значение 'IsPared'
    снова снанет False.
    """
    find_table = table.all()
    first_user_record_id, first_user_eng_level, first_user_time_slot, second_user_record_id, second_user_tg_id = '', '', '', '', ''
    is_found = False
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            first_user_eng_level = find_table[index]['fields']['UserEngLevel']
            first_user_time_slot = find_table[index]['fields']['UserTimeSlot']
            first_user_record_id = find_table[index]['id']
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] != str(message.from_user.id) \
                and find_table[index]['fields']['UserEngLevel'] == first_user_eng_level \
                and find_table[index]['fields']['UserTimeSlot'] == first_user_time_slot \
                and find_table[index]['fields']['IsPared'] == 'False':
            second_user_tg_id = str(find_table[index]['fields']['UserIDTG'])
            second_user_record_id = find_table[index]['id']
            is_found = True
    if is_found:
        meeting_link, join_password = createMeeting()
        table.update(record_id=str(first_user_record_id), fields={'IsPared': "True"})
        table.update(record_id=str(second_user_record_id), fields={'IsPared': "True"})
        await message.answer(text=f"Join new meeting: {meeting_link}")
        await bot.send_message(chat_id=int(second_user_tg_id), text=f"Hi! You can join new meeting: {meeting_link}")
        await asyncio.sleep(60)
        table.update(record_id=str(first_user_record_id), fields={'IsPared': "False"})
        table.update(record_id=str(second_user_record_id), fields={'IsPared': "False"})
    else:
        await message.answer(text='Извините, мы никого не смогли найти....')
        await menu(message)



def register_handlers_find_interlocutor(dp: Dispatcher):
    dp.register_message_handler(find_companion, commands=['find_interlocutor'])
    dp.register_message_handler(send_message_cron30)
    dp.register_message_handler(send_message_cron15)
    dp.register_message_handler(send_message_cron5)
    dp.register_message_handler(send_message_cron)
    dp.register_message_handler(update_cron)

    
