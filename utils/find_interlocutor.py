from aiogram import types, Dispatcher
from airtable_config import table
from .meeting import createMeeting
from config import bot, dp, week_dict, WEEKDAYS
from .menu import menu
from keyboards.inline_menu import G_MENU, U_STAT, C_MEET_MENU, GO_FIND, CONF_MEET
from keyboards.inline_free_timeslot import genmarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from user_states import TS
from aiogram.dispatcher import FSMContext
import re
import asyncio





'''
Мегафункция подбора собеседника.
Надо было бы её делать более сегментированной, но структура осталась от Бета-версии.
'''
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
        table.update(record_id=str(first_user_record_id), fields={'JobName': name_sched})
        table.update(record_id=str(second_user_record_id), fields={'JobName': name_sched})
        
        '''тут у нас выдача сообщений про успешный метчинг'''
        await bot.send_message(message.from_user.id, 
            text=f'We have found a match for you.\nYour meeting starts on \U0001F5D3 {week_for_message}, {start_time}:00 \U0001F5D3')
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                try:
                    msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                except:
                    pass
                try:
                    await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                except:
                    pass
                msg_id1 = (await bot.send_message(message.from_user.id, 
                    text=f'You will have a meeting with - \U0001F464 {second_user_fname} \U0001F464 \nWe would like to send a reminder half an hour prior to the call.', 
                    reply_markup=C_MEET_MENU)).message_id
                table.update(record_id=str(first_record_id), fields={"msgIDforDEL": str(msg_id1)})  #запись msg_id в БД

        await bot.send_message(chat_id=int(second_tg_id), 
            text=f'We have found a match for you.\nYour meeting starts on \U0001F5D3 {week_for_message}, {start_time}:00 \U0001F5D3')
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserIDTG'] == second_tg_id:
                try:
                    msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                except:
                    pass
                try:
                    await bot.delete_message(int(second_tg_id), message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                except:
                    pass
                msg_id2 = (await bot.send_message(chat_id=int(second_tg_id), 
                    text=f'You will have a meeting with - \U0001F464 {first_user_fname} \U0001F464 \nWe would like to send a reminder half an hour prior to the call.', 
                    reply_markup=C_MEET_MENU)).message_id
                table.update(record_id=str(second_record_id), fields={"msgIDforDEL": str(msg_id2)})  #запись msg_id в БД

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
        # globals()[name_sched].add_job(send_message_cron30, trigger='cron', day_of_week=time_now.weekday(), hour=int(time_now.hour),
        #     minute=int(time_now.minute)+1,second=10 , kwargs={'mess': mess}, misfire_grace_time=3)
        # globals()[name_sched].add_job(send_message_cron15, trigger='cron', day_of_week=time_now.weekday(), hour=int(time_now.hour),
        #     minute=int(time_now.minute)+1,second=15 , kwargs={'mess': mess}, misfire_grace_time=3)
        # globals()[name_sched].add_job(send_message_cron5, trigger='cron', day_of_week=time_now.weekday(), hour=int(time_now.hour),
        #     minute=int(time_now.minute)+1,second=20 , kwargs={'mess': mess}, misfire_grace_time=3)
        # globals()[name_sched].add_job(send_message_cron, trigger='cron', day_of_week=time_now.weekday(), hour=int(time_now.hour),
        #     minute=int(time_now.minute)+1,second=25 , kwargs={'mess': mess}, misfire_grace_time=3)
        # globals()[name_sched].add_job(send_message_postmeet, trigger='cron', day_of_week=time_now.weekday(), hour=int(time_now.hour),
        #     minute=int(time_now.minute)+1,second=30 , kwargs={'mess_bd': mess_bd}, misfire_grace_time=3)
        # globals()[name_sched].add_job(update_cron, trigger='cron', day_of_week=time_now.weekday(), hour=int(time_now.hour),
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
            minute=40, kwargs={'mess_bd': mess_bd}, misfire_grace_time=3)
        globals()[name_sched].add_job(update_cron, trigger='cron', day_of_week=search_day, hour=int(dt_meet.strftime('%H')),
            minute=40, kwargs={'bd': bd}, misfire_grace_time=3)
        globals()[name_sched].print_jobs()
    else: # отработка цикла для тех кому пары не нашлось
        list_TS = []
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserIDTG'] != str(message.from_user.id) \
                    and find_table[index]['fields']['UserEngLevel'] == first_user_eng_level \
                    and find_table[index]['fields']['UserTimeSlot'] != first_user_time_slot \
                    and find_table[index]['fields']['UserTimeSlot'] != 'None' \
                    and find_table[index]['fields']['IsPared'] == 'False':
                more_time_slot = find_table[index]['fields']['UserTimeSlot']
                list_TS.append(more_time_slot)
                is_found = False
                more_found = True
                
        if is_found == False and more_found == True: # уровень языка совпадает хоть с кем нибудь, смените ТаймСлот
            find_table = table.all()
            for index in range(len(find_table)):
                if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                    record_id = find_table[index]['id']  # достает record_id из БД
                    try:
                        msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                    except:
                        pass
                    try:
                        await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                    except:
                        pass
                    msg_id = (await bot.send_message(message.from_user.id, 
                        text=f'There are no available peer matches for a given slot.\n\
We saved your choice and would like to send a notification once we find a peer.\n\
There is an opportunity to chat at this time:',
                        reply_markup=genmarkup(list_TS))).message_id
                    # await bot.send_message(message.from_user.id, reply_markup=G_MENU)
                    await TS.time_slot.set()
                    print(msg_id)
                    table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  # запись msg_id в БД
        else: # уровень языка не совпадает вообще ни с кем 
            find_table = table.all()
            for index in range(len(find_table)):
                if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                    record_id = find_table[index]['id']  # достает record_id из БД
                    try:
                        msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                    except:
                        pass
                    try:
                        await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                    except:
                        pass
                    msg_id = (await bot.send_message(message.from_user.id, 
                        text="Sorry, we haven't been able to find a match at that time. Please try another level of the language.",
                        reply_markup=G_MENU)).message_id
                    table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  # запись msg_id в БД
                    print(msg_id)




@dp.callback_query_handler(state=TS.time_slot)
async def set_timeslot(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(time_slot=callback_query.data)
    all_table = table.all() # получаем всю таблицу
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(callback_query.from_user.id):
            old_TS = all_table[index]['fields']['UserTimeSlot']
            record_id = all_table[index]['id']  # достает record_id из БД
            time_slot = callback_query.data
            pattern = r'^[MO|TU|WE|TH|FR|SA|SU]+(0[0-9]|1[0-9]|2[0-3])$'
            
            week = time_slot[0]+time_slot[1]
            start_time = time_slot[2]+time_slot[3]
            week_for_message = week_dict.get(week)
            pared_time = f'\U0001F5D3 {week_for_message}, {start_time}:00 \U0001F5D3'

            old_week = old_TS[0]+old_TS[1]
            old_start_time = old_TS[2]+old_TS[3]
            old_week_for_message = week_dict.get(old_week)
            old_pared_time = f'\U0001F5D3 {old_week_for_message}, {old_start_time}:00 \U0001F5D3'

            if re.fullmatch(pattern, time_slot):
                try:
                    msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                except:
                    pass
                try:
                    await bot.delete_message(callback_query.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                except:
                    pass
                msg_id = (await bot.send_message(callback_query.from_user.id, text=f'Your Time-Slot - {pared_time}.', 
                    reply_markup=GO_FIND)).message_id
                table.update(record_id=str(record_id), fields={'UserTimeSlot': time_slot})
                table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  # запись msg_id в БД
                await state.finish()
            else:
                try:
                    msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                except:
                    pass
                try:
                    await bot.delete_message(callback_query.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                except:
                    pass
                msg_id = (await bot.send_message(callback_query.from_user.id, text=f'Your Time-Slot - {old_pared_time}.', 
                    reply_markup=G_MENU)).message_id
                table.update(record_id=str(record_id), fields={'UserTimeSlot': old_TS})
                table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  # запись msg_id в БД
                await state.finish()

    

"""непосредственно наши сообщения которые будут приходить перед началом + работа с БД"""
async def send_message_cron30(mess):
    first_tg_id = mess['first_tg_id']
    second_tg_id = mess['second_tg_id']
    await bot.send_message(chat_id=int(first_tg_id), text=f'The meeting will begin in 30 minutes.')
    await bot.send_message(chat_id=int(second_tg_id), text=f'The meeting will begin in 30 minutes.')
async def send_message_cron15(mess):
    first_tg_id = mess['first_tg_id']
    second_tg_id = mess['second_tg_id']
    await bot.send_message(chat_id=int(first_tg_id), text=f'The meeting will begin in 15 minutes.')
    await bot.send_message(chat_id=int(second_tg_id), text=f'The meeting will begin in 15 minutes.')
async def send_message_cron5(mess):
    first_tg_id = mess['first_tg_id']
    second_tg_id = mess['second_tg_id']
    await bot.send_message(chat_id=int(first_tg_id), text=f'The meeting will begin in 5 minutes.')
    await bot.send_message(chat_id=int(second_tg_id), text=f'The meeting will begin in 5 minutes.')
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
    msg_id1 = (await bot.send_message(int(first_tg_id), text=f'Встреча состоялась?', reply_markup=CONF_MEET)).message_id
    msg_id2 = (await bot.send_message(int(second_tg_id), text=f'Встреча состоялась?', reply_markup=CONF_MEET)).message_id
    table.update(record_id=str(first_record_id), fields={'msgIDforDEL': str(msg_id1)})
    table.update(record_id=str(second_record_id), fields={'msgIDforDEL': str(msg_id2)})
async def update_cron(bd):
    first_record_id = bd['first_record_id']
    second_record_id = bd['second_record_id']
    table.update(record_id=str(first_record_id), fields={'IsPared': "False"})
    table.update(record_id=str(second_record_id), fields={'IsPared': "False"})


'''выбор роли после успешного митинга'''
@dp.callback_query_handler(text='select_role')
async def callback_select_role(message: types.Message):
    all_table = table.all()
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            record_id = all_table[index]['id']  # достает record_id из БД
            msg_id = (await bot.send_message(
                message.from_user.id, text=f'Заполните форму - [LINK]\n\n\
Choose the role you had in the meeting:', reply_markup=U_STAT)).message_id
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД


"""сценарий при неуспешном митинге"""
@dp.callback_query_handler(text='fail_meet')
async def callback_fail_meet(message: types.Message):
    all_table = table.all()
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            record_id = all_table[index]['id']  # достает record_id из БД
            leave_score = int(all_table[index]['fields']['LeaveMeeting'])
            new_leave = leave_score+1
            msg_id = (await bot.send_message(
                message.from_user.id, text=f'\U0001F62D Очень жаль. Надеемся в следующий раз всё получится.', reply_markup=G_MENU)).message_id
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
            table.update(record_id=str(record_id), fields={"LeaveMeeting": str(new_leave)})  #запись Ливнувших в БД


'''функция отмены митинга'''
@dp.callback_query_handler(text='cancel_meet')
async def callback_find_companion(message: types.Message):
    find_table = table.all()
    first_user_record_id, second_user_record_id, second_tg_id = '', '', ''
    job_name = ''
    is_found = False
    for index in range(len(find_table)): # вытягивание инициатора отмены из БД
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            first_user_record_id = find_table[index]['id']
            job_name = str(find_table[index]['fields']['JobName'])
            second_tg_id = find_table[index]['fields']['IsParedID']
            print(second_tg_id)
    for index in range(len(find_table)):  # вытягивание собеседника для отмены из БД
        if find_table[index]['fields']['UserIDTG'] == second_tg_id:
            second_user_record_id = find_table[index]['id']
            is_found = True
    if is_found == True:
        '''начинаем обновлять данные в БД'''
        table.update(record_id=str(first_user_record_id), fields={'IsPared': 'False'})
        table.update(record_id=str(second_user_record_id), fields={'IsPared': 'False'})
        table.update(record_id=str(first_user_record_id), fields={'UserTimeSlot': 'None'}) # это сделано для исключения спама
        # table.update(record_id=str(second_user_record_id), fields={'UserTimeSlot': 'None'}) # это сделано для исключения спама
        globals()[job_name].shutdown(wait=False) # отключение планировщика
        '''выдача сообщения отмены инициатору'''
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                try:
                    msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                except:
                    pass
                try:
                    await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                except:
                    pass
                msg_id1 = (await bot.send_message(message.from_user.id, 
                    text=f'The meeting was canceled.', 
                    reply_markup=G_MENU)).message_id
                table.update(record_id=str(first_user_record_id), fields={"msgIDforDEL": str(msg_id1)})  #запись msg_id в БД
        '''выдача сообщения отмены сабмисиву'''
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserIDTG'] == second_tg_id:
                try:
                    msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                except:
                    pass
                try:
                    await bot.delete_message(int(second_tg_id), message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                except:
                    pass
                msg_id2 = (await bot.send_message(chat_id=int(second_tg_id), 
                    text=f'The meeting was canceled by your peer.', 
                    reply_markup=G_MENU)).message_id
                table.update(record_id=str(second_user_record_id), fields={"msgIDforDEL": str(msg_id2)})  #запись msg_id в БД



'''кусок подбора собеседника через команду в боте'''
async def find_companion(message: types.Message):
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
        table.update(record_id=str(first_user_record_id), fields={'JobName': name_sched})
        table.update(record_id=str(second_user_record_id), fields={'JobName': name_sched})
        
        '''тут у нас выдача сообщений про успешный метчинг'''
        await bot.send_message(message.from_user.id, 
            text=f'We have found a match for you.\nYour meeting starts on \U0001F5D3 {week_for_message}, {start_time}:00 \U0001F5D3')
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                try:
                    msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                except:
                    pass
                try:
                    await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                except:
                    pass
                msg_id1 = (await bot.send_message(message.from_user.id, 
                    text=f'You will have a meeting with - \U0001F464 {second_user_fname} \U0001F464 \nWe would like to send a reminder half an hour prior to the call.', 
                    reply_markup=C_MEET_MENU)).message_id
                table.update(record_id=str(first_record_id), fields={"msgIDforDEL": str(msg_id1)})  #запись msg_id в БД

        await bot.send_message(chat_id=int(second_tg_id), 
            text=f'We have found a match for you.\nYour meeting starts on \U0001F5D3 {week_for_message}, {start_time}:00 \U0001F5D3')
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserIDTG'] == second_tg_id:
                try:
                    msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                except:
                    pass
                try:
                    await bot.delete_message(int(second_tg_id), message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                except:
                    pass
                msg_id2 = (await bot.send_message(chat_id=int(second_tg_id), 
                    text=f'You will have a meeting with - \U0001F464 {first_user_fname} \U0001F464 \nWe would like to send a reminder half an hour prior to the call.', 
                    reply_markup=C_MEET_MENU)).message_id
                table.update(record_id=str(second_record_id), fields={"msgIDforDEL": str(msg_id2)})  #запись msg_id в БД

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

        '''быстрые задания для тестов (+3 hour - потому что на сервере не минское время)'''
        globals()[name_sched].add_job(send_message_cron30, trigger='cron', day_of_week=time_now.weekday(), hour=int(time_now.hour)+3,
            minute=int(time_now.minute)+1,second=10 , kwargs={'mess': mess}, misfire_grace_time=3)
        globals()[name_sched].add_job(send_message_cron15, trigger='cron', day_of_week=time_now.weekday(), hour=int(time_now.hour)+3,
            minute=int(time_now.minute)+1,second=15 , kwargs={'mess': mess}, misfire_grace_time=3)
        globals()[name_sched].add_job(send_message_cron5, trigger='cron', day_of_week=time_now.weekday(), hour=int(time_now.hour)+3,
            minute=int(time_now.minute)+1,second=20 , kwargs={'mess': mess}, misfire_grace_time=3)
        globals()[name_sched].add_job(send_message_cron, trigger='cron', day_of_week=time_now.weekday(), hour=int(time_now.hour)+3,
            minute=int(time_now.minute)+1,second=25 , kwargs={'mess': mess}, misfire_grace_time=3)
        globals()[name_sched].add_job(send_message_postmeet, trigger='cron', day_of_week=time_now.weekday(), hour=int(time_now.hour)+3,
            minute=int(time_now.minute)+1,second=30 , kwargs={'mess_bd': mess_bd}, misfire_grace_time=3)
        globals()[name_sched].add_job(update_cron, trigger='cron', day_of_week=time_now.weekday(), hour=int(time_now.hour)+3,
            minute=int(time_now.minute)+1,second=30 , kwargs={'bd': bd}, misfire_grace_time=3)
        globals()[name_sched].print_jobs()

        """непосредственно добавление заданий в обработчик"""
        # globals()[name_sched].add_job(send_message_cron30, trigger='cron', day_of_week=start_alert.weekday(), hour=int(start_alert.strftime('%H')), 
        #     minute=30, kwargs={'mess': mess}, misfire_grace_time=3)
        # globals()[name_sched].add_job(send_message_cron15, trigger='cron', day_of_week=start_alert.weekday(), hour=int(start_alert.strftime('%H')), 
        #     minute=45, kwargs={'mess': mess}, misfire_grace_time=3)
        # globals()[name_sched].add_job(send_message_cron5, trigger='cron', day_of_week=start_alert.weekday(), hour=int(start_alert.strftime('%H')), 
        #     minute=55, kwargs={'mess': mess}, misfire_grace_time=3)
        # globals()[name_sched].add_job(send_message_cron, trigger='cron', day_of_week=search_day, hour=int(dt_meet.strftime('%H')),
        #     minute=0, kwargs={'mess': mess}, misfire_grace_time=3)
        # globals()[name_sched].add_job(send_message_postmeet, trigger='cron', day_of_week=search_day, hour=int(dt_meet.strftime('%H')),
        #     minute=40, kwargs={'mess_bd': mess_bd}, misfire_grace_time=3)
        # globals()[name_sched].add_job(update_cron, trigger='cron', day_of_week=search_day, hour=int(dt_meet.strftime('%H')),
        #     minute=40, kwargs={'bd': bd}, misfire_grace_time=3)
        # globals()[name_sched].print_jobs()
    else: # отработка цикла для тех кому пары не нашлось
        list_TS = []
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserIDTG'] != str(message.from_user.id) \
                    and find_table[index]['fields']['UserEngLevel'] == first_user_eng_level \
                    and find_table[index]['fields']['UserTimeSlot'] != first_user_time_slot \
                    and find_table[index]['fields']['UserTimeSlot'] != 'None' \
                    and find_table[index]['fields']['IsPared'] == 'False':
                more_time_slot = find_table[index]['fields']['UserTimeSlot']
                list_TS.append(more_time_slot)
                is_found = False
                more_found = True
                
        if is_found == False and more_found == True: # уровень языка совпадает хоть с кем нибудь, смените ТаймСлот
            find_table = table.all()
            for index in range(len(find_table)):
                if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                    record_id = find_table[index]['id']  # достает record_id из БД
                    try:
                        msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                    except:
                        pass
                    try:
                        await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                    except:
                        pass
                    
                    msg_id = (await bot.send_message(message.from_user.id, 
                        text=f'There are no available peer matches for a given slot.\n\
We saved your choice and would like to send a notification once we find a peer.\n\
There is an opportunity to chat at this time:',
                        reply_markup=genmarkup(list_TS))).message_id
                    # await bot.send_message(message.from_user.id, reply_markup=G_MENU)
                    await TS.time_slot.set()
                    print(msg_id)
                    table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  # запись msg_id в БД
        else: # уровень языка не совпадает вообще ни с кем 
            find_table = table.all()
            for index in range(len(find_table)):
                if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                    record_id = find_table[index]['id']  # достает record_id из БД
                    try:
                        msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                    except:
                        pass
                    try:
                        await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                    except:
                        pass
                    msg_id = (await bot.send_message(message.from_user.id, 
                        text="Sorry, we haven't been able to find a match at that time. Please try another level of the language.",
                        reply_markup=G_MENU)).message_id
                    table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  # запись msg_id в БД
                    print(msg_id)
            



def register_handlers_find_interlocutor(dp: Dispatcher):
    dp.register_message_handler(find_companion, commands=['find_interlocutor'])
    dp.register_message_handler(send_message_cron30, commands=['40000_monkeys_put_a_banana_up_their_butt'])
    dp.register_message_handler(send_message_cron15, commands=['40000_monkeys_put_a_banana_up_their_butt'])
    dp.register_message_handler(send_message_cron5, commands=['40000_monkeys_put_a_banana_up_their_butt'])
    dp.register_message_handler(send_message_cron, commands=['40000_monkeys_put_a_banana_up_their_butt'])
    dp.register_message_handler(send_message_postmeet, commands=['40000_monkeys_put_a_banana_up_their_butt'])
    dp.register_message_handler(update_cron, commands=['40000_monkeys_put_a_banana_up_their_butt'])
    