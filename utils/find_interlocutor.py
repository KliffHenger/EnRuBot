from aiogram import types, Dispatcher
from airtable_config import table
from .meeting import createMeeting
from config import bot, dp, week_dict, WEEKDAYS
from .menu import menu
from keyboards.inline_menu import G_MENU, U_STAT
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

import asyncio






@dp.callback_query_handler(text='find_interlocutor')
async def callback_find_companion(message: types.Message):
    meeting_link, join_password = createMeeting()
    find_table = table.all()
    global first_user_record_id
    global second_user_record_id
    global second_user_tg_id
    global first_user_tg_id
    first_user_record_id, first_user_eng_level, first_user_time_slot, second_user_record_id, second_user_tg_id = '', '', '', '', ''
    first_user_tg_id = str(message.from_user.id)
    more_found = False
    is_found = False
    for index in range(len(find_table)): # начало цикла подбора, вытягивание инициатора из БД
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            first_user_eng_level = find_table[index]['fields']['UserEngLevel']
            first_user_time_slot = find_table[index]['fields']['UserTimeSlot']
            first_user_fname = find_table[index]['fields']['UserName']
            week = first_user_time_slot[0]+first_user_time_slot[1]
            start_time = first_user_time_slot[2]+first_user_time_slot[3]
            week_for_message = week_dict.get(week)
            first_user_record_id = find_table[index]['id']
    for index in range(len(find_table)):  # вытягивание собеседника из БД
        if find_table[index]['fields']['UserIDTG'] != str(message.from_user.id) \
                and find_table[index]['fields']['UserEngLevel'] == first_user_eng_level \
                and find_table[index]['fields']['UserTimeSlot'] == first_user_time_slot \
                and find_table[index]['fields']['IsPared'] == 'False':
            second_user_tg_id = str(find_table[index]['fields']['UserIDTG'])
            second_user_fname = find_table[index]['fields']['UserName']
            second_user_record_id = find_table[index]['id']
            is_found = True
            more_found = False
    if is_found == True and more_found == False:
        '''начинаем обновлять данные в БД и тут же получаем кое что обратно'''
        table.update(record_id=str(first_user_record_id), fields={'IsPared': "True"})
        table.update(record_id=str(second_user_record_id), fields={'IsPared': "True"})
        table.update(record_id=str(first_user_record_id), fields={'IsParedID': second_user_tg_id})
        table.update(record_id=str(second_user_record_id), fields={'IsParedID': first_user_tg_id})
        
        f_dict = table.get(first_user_record_id)
        
        first_tg_id = f_dict['fields']['UserIDTG']
        second_tg_id = f_dict['fields']['IsParedID']

        first_record_id = first_user_record_id 
        second_record_id = second_user_record_id
        
        '''тут мы пытаемся каждому пользователю выдать по планировщику'''
        name_sched = 'sched'+first_tg_id
        globals()[name_sched] = AsyncIOScheduler(timezone="Europe/Minsk")
        globals()[name_sched].start()
        
        '''тут у нас выдача сообщений про успешный метчинг'''
        await bot.send_message(message.from_user.id, text=f'There is an peer for you for the time of {week_for_message}, {start_time}-00.')
        await bot.send_message(message.from_user.id, text=f'Your peer is - {second_user_fname}.', reply_markup=G_MENU)
        await bot.send_message(chat_id=int(second_tg_id), text=f'There is an peer for you for the time of {week_for_message}, {start_time}-00.')
        await bot.send_message(chat_id=int(second_tg_id), text=f'Your peer is - {first_user_fname}.', reply_markup=G_MENU)
        if week_for_message:    # этот кусок кода отвечет за формирование необходимых дат для отсрочки сообщений
            search_day = WEEKDAYS.index(week_for_message.lower())  
            time_now = datetime.now()
            date_now = datetime.date(time_now)
            day_now = time_now.weekday()
            different_days = search_day - day_now if day_now <= search_day else 7 - day_now + search_day
            date_meet = date_now + timedelta(days=different_days)
            datetime_meet = str(date_meet)+","+str(start_time)+",00,00"
            dt_meet = datetime.strptime(datetime_meet, "%Y-%m-%d,%H,%M,%S")
            start_alert = dt_meet - timedelta(minutes=30)

        '''тут мы собираем квардс для передачи в планировщик'''
        mess = {'first_tg_id': first_tg_id, 'second_tg_id': second_tg_id}
        bd = {'first_record_id':first_record_id, 'second_record_id':second_record_id}
        mess_bd = {'first_tg_id': first_tg_id, 'second_tg_id': second_tg_id, 
                'first_record_id':first_record_id, 'second_record_id':second_record_id}

        '''быстрые задания для тестов'''
        # globals()[name_sched].add_job(send_message_cron30, trigger='cron', day_of_week=time_now.weekday(), hour=time_now.hour, 
        #     minute=int(time_now.minute)+1,second=10 , kwargs={'mess': mess}, misfire_grace_time=3)
        # globals()[name_sched].add_job(send_message_cron15, trigger='cron', day_of_week=time_now.weekday(), hour=time_now.hour, 
        #     minute=int(time_now.minute)+1,second=15 , kwargs={'mess': mess}, misfire_grace_time=3)
        # globals()[name_sched].add_job(send_message_cron5, trigger='cron', day_of_week=time_now.weekday(), hour=time_now.hour, 
        #     minute=int(time_now.minute)+1,second=20 , kwargs={'mess': mess}, misfire_grace_time=3)
        # globals()[name_sched].add_job(send_message_cron, trigger='cron', day_of_week=time_now.weekday(), hour=time_now.hour,
        #     minute=int(time_now.minute)+1,second=25 , kwargs={'mess': mess}, misfire_grace_time=3)
        # globals()[name_sched].add_job(send_message_postmeet, trigger='cron', day_of_week=time_now.weekday(), hour=time_now.hour,
        #     minute=int(time_now.minute)+1,second=30 , kwargs={'mess_bd': mess_bd}, misfire_grace_time=3)
        # globals()[name_sched].add_job(update_cron, trigger='cron', day_of_week=time_now.weekday(), hour=time_now.hour,
        #     minute=int(time_now.minute)+1,second=30 , kwargs={'bd': bd}, misfire_grace_time=3)
        # globals()[name_sched].print_jobs()

        """непосредственно добавление заданий в обработчик"""
        globals()[name_sched].add_job(send_message_cron30, trigger='cron', day_of_week=start_alert.weekday(), hour=int(start_alert.strftime('%H')), 
            minute=30, kwargs={'mess': mess}, misfire_grace_time=3)
        globals()[name_sched].add_job(send_message_cron15, trigger='cron', day_of_week=start_alert.weekday(), hour=int(start_alert.strftime('%H')), 
            minute=45, kwargs={'mess': mess}, misfire_grace_time=3)
        globals()[name_sched].add_job(send_message_cron5, trigger='cron', day_of_week=start_alert.weekday(), hour=int(start_alert.strftime('%H')), 
            minute=55, kwargs={'mess': mess}, misfire_grace_time=3)
        globals()[name_sched].add_job(send_message_cron, trigger='cron', day_of_week=search_day, hour=int(dt_meet.strftime('%H')),
            minute=0, kwargs={'mess': mess}, misfire_grace_time=3)
        globals()[name_sched].add_job(send_message_postmeet, trigger='cron', day_of_week=search_day, hour=int(dt_meet.strftime('%H')),
            minute=40, kwargs={'mess': mess}, misfire_grace_time=3)
        globals()[name_sched].add_job(update_cron, trigger='cron', day_of_week=search_day, hour=int(dt_meet.strftime('%H')),
            minute=40, kwargs={'bd': bd}, misfire_grace_time=3)
        globals()[name_sched].print_jobs()
    else: # отработка цикла для тех кому пары не нашлось
        list_TS = []
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserIDTG'] != str(message.from_user.id) \
                    and find_table[index]['fields']['UserEngLevel'] == first_user_eng_level \
                    and find_table[index]['fields']['UserTimeSlot'] != first_user_time_slot \
                    and find_table[index]['fields']['IsPared'] == 'False':
                more_time_slot = find_table[index]['fields']['UserTimeSlot']
                list_TS.append(more_time_slot)
                is_found = False
                more_found = True
        if is_found == False and more_found == True: # уровень языка совпадает хоть с кем нибудь, смените ТаймСлот
            list_time_slot = ' '.join([str(elem) for elem in list_TS])
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f'There are no coincidences for your Time-Slot, but there is at {list_time_slot}')).message_id
            print(msg_id)
            await menu(message)
        else: # уровень языка не совпадает вообще ни с кем 
            msg_id = (await bot.send_message(message.from_user.id, 
                text='Sorry, but there is no one with your level of knowledge of the language. Try to change it.')).message_id
            print(msg_id)
            await menu(message)
        
"""непосредственно наши сообщения которые будут приходить перед началом + работа с БД"""
async def send_message_cron30(mess):
    first_tg_id = mess['first_tg_id']
    second_tg_id = mess['second_tg_id']
    await bot.send_message(chat_id=int(first_tg_id), text='The meeting will begin after 30 minutes.')
    await bot.send_message(chat_id=int(second_tg_id), text='The meeting will begin after 30 minutes.')
async def send_message_cron15(mess):
    first_tg_id = mess['first_tg_id']
    second_tg_id = mess['second_tg_id']
    await bot.send_message(chat_id=int(first_tg_id), text='The meeting will begin after 15 minutes.')
    await bot.send_message(chat_id=int(second_tg_id), text='The meeting will begin after 15 minutes.')
async def send_message_cron5(mess):
    first_tg_id = mess['first_tg_id']
    second_tg_id = mess['second_tg_id']
    await bot.send_message(chat_id=int(first_tg_id), text='The meeting will begin after 5 minutes.')
    await bot.send_message(chat_id=int(second_tg_id), text='The meeting will begin after 5 minutes.')
async def send_message_cron(mess):
    first_tg_id = mess['first_tg_id']
    second_tg_id = mess['second_tg_id']
    meeting_link, join_password = createMeeting()
    await bot.send_message(chat_id=int(first_tg_id), text=f'Join new meeting: {meeting_link}', reply_markup=G_MENU)
    await bot.send_message(chat_id=int(second_tg_id), text=f'Join new meeting: {meeting_link}', reply_markup=G_MENU)
async def send_message_postmeet(mess_bd):
    first_tg_id = mess_bd['first_tg_id']
    second_tg_id = mess_bd['second_tg_id']
    first_record_id = mess_bd['first_record_id']
    second_record_id = mess_bd['second_record_id']
    msg_id1 = (await bot.send_message(int(first_tg_id), text='Выберите в роли кого вы были на встрече.', reply_markup=U_STAT)).message_id
    msg_id2 = (await bot.send_message(int(second_tg_id), text='Выберите в роли кого вы были на встрече.', reply_markup=U_STAT)).message_id
    table.update(record_id=str(first_record_id), fields={'msgIDforDEL': str(msg_id1)})
    table.update(record_id=str(second_record_id), fields={'msgIDforDEL': str(msg_id2)})
async def update_cron(bd):
    first_record_id = bd['first_record_id']
    second_record_id = bd['second_record_id']
    table.update(record_id=str(first_record_id), fields={'IsPared': "False"})
    table.update(record_id=str(second_record_id), fields={'IsPared': "False"})



async def find_companion(message: types.Message):
    """
    Функция поиска собеседника. Наша цель на данном этапе: найти человека с подходящими
    параметрами. На первом шаге мы ищем двоих пользователей в базе для получения данных.
    После данной операции нам необзодимо провести операцию сравнения. Если параметры языка и времени у
    пользователей совпадают, то они образуют пару. Если нет - бот выводит: 'Извините, мы никого не смогли найти....'.
    Ровно в этот момент их значения поля 'IsPared' в базе становится True.
    По истечению 40 минут их значение 'IsPared' снова снанет False.
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
    dp.register_message_handler(send_message_postmeet)
    dp.register_message_handler(update_cron)
    