from aiogram import types, Dispatcher
from user_states import TimeSlot
from aiogram.dispatcher import FSMContext
from keyboards.inline_time_slot import HOUR
from keyboards.inline_menu import G_MENU
from airtable_config import table
from utils.menu import menu
from config import dp, bot
from datetime import datetime, timedelta
from utils.simple_calendar import calendar_callback as simple_cal_callback, SimpCalendar
from aiogram.dispatcher.filters import Text
import re



'''(1)Начало ввода ТаймСлота(старт "машины состояний")'''
@dp.callback_query_handler(Text(equals=['timeslot'], ignore_case=True))
async def callback_timeslot_input(message: types.Message):
    all_table = table.all()
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            record_id = all_table[index]['id']  # достает record_id из БД
            # first_user_time_slot = all_table[index]['fields']['UserTimeSlot']
            # week = first_user_time_slot[0]+first_user_time_slot[1]
            # week_for_message = week_dict.get(week)
            # search_day = WEEKDAYS.index(week_for_message.lower())
            # mo,  = 
            # time_now = datetime.now()
            # date_now = datetime.date(time_now)
            # day_now = time_now.weekday()


            try:
                msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            except:
                pass
            try:
                await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            except:
                pass
            await bot.send_message(message.from_user.id, 
                text=f"Please select a possible day for your meeting.", reply_markup=await SimpCalendar().start_calendar())
            # print(msg_id)
            # table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
            # await TimeSlot.week_day.set()

async def time_slot_input(message: types.Message):
    all_table = table.all()
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            record_id = all_table[index]['id']  # достает record_id из БД
            msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Please select a possible day for your meeting.", reply_markup=await SimpCalendar().start_calendar())).message_id
            print(msg_id)
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
            # await TimeSlot.week_day.set()


'''(2)Ввод дня недели'''

# async def get_week_day(message: types.Message,  state: FSMContext):
#     pattern = r'MO|TU|WE|TH|FR|SA|SU'
#     if re.fullmatch(pattern, message.text):
#         await state.update_data(week_day=message.text)
#         all_table = table.all()
#         for index in range(len(all_table)):
#             if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
#                 record_id = all_table[index]['id']  # достает record_id из БД
#                 msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
#                 await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
#                 msg_id = (await bot.send_message(message.from_user.id, 
#                     f"Great. You've selected - {message.text}.\nNext, please write in the time you would be comfortable to start at: \nFor example: 17 or 09.")).message_id
#                 print(msg_id)
#                 table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
#                 await TimeSlot.start_time.set()
#     else:
#         all_table = table.all()
#         for index in range(len(all_table)):
#             if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
#                 record_id = all_table[index]['id']  # достает record_id из БД
#                 msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
#                 await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
#                 msg_id = (await bot.send_message(message.from_user.id, 
#                     text='Oops! Wrong format!\nTry again, please. Make sure you use the keyboard.', reply_markup=WEEK)).message_id
#                 print(msg_id)
#                 table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД

@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(message: types.Message, callback_data: dict):
    selected, date = await SimpCalendar().process_selection(message, callback_data)
    # print(selected)
    if selected:
        sel_date = date.date()
        print(sel_date)
        correct_date = f'{date.strftime("%Y-%m-%d")}'
        user_date_now = datetime.now().date()
        if user_date_now <= sel_date:
            # await state.update_data(week_day={date.strftime("%d/%m/%Y")})
            all_table = table.all()
            for index in range(len(all_table)):
                if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                    record_id = all_table[index]['id']  # достает record_id из БД
                    msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                    # await bot.delete_message(callback_query.message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                    
                    msg_id = (await bot.send_message(message.from_user.id, 
                        f"Great. You've selected - {correct_date}.\nNext, please select the time for your meeting:", 
                        reply_markup=HOUR)).message_id
                    print(msg_id)
                    table.update(record_id=str(record_id), fields={"UserDateSlot": str(correct_date)})
                    table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
                # await TimeSlot.start_time.set()
        else:
            all_table = table.all()
            for index in range(len(all_table)):
                if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                    record_id = all_table[index]['id']  # достает record_id из БД
                    # msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                    # await bot.delete_message(callback_query.message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                    msg_id = (await bot.send_message(message.from_user.id, 
                        f"\U0000203C Please choose a coming date. The selected date is in the past:", 
                        reply_markup=await SimpCalendar().start_calendar())).message_id


'''(3)Ввод времени начала'''

@dp.callback_query_handler(text='00')
async def set_start_00(message: types.Message):
    start_time = '00'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='01')
async def set_start_00(message: types.Message):
    start_time = '01'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='02')
async def set_start_00(message: types.Message):
    start_time = '02'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='03')
async def set_start_00(message: types.Message):
    start_time = '03'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='04')
async def set_start_00(message: types.Message):
    start_time = '04'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='05')
async def set_start_00(message: types.Message):
    start_time = '05'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='06')
async def set_start_00(message: types.Message):
    start_time = '06'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='07')
async def set_start_00(message: types.Message):
    start_time = '07'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='08')
async def set_start_00(message: types.Message):
    start_time = '08'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='09')
async def set_start_00(message: types.Message):
    start_time = '09'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='10')
async def set_start_00(message: types.Message):
    start_time = '10'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='11')
async def set_start_00(message: types.Message):
    start_time = '11'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='12')
async def set_start_00(message: types.Message):
    start_time = '12'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='13')
async def set_start_00(message: types.Message):
    start_time = '13'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='14')
async def set_start_00(message: types.Message):
    start_time = '14'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='15')
async def set_start_00(message: types.Message):
    start_time = '15'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='16')
async def set_start_00(message: types.Message):
    start_time = '16'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='17')
async def set_start_00(message: types.Message):
    start_time = '17'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='18')
async def set_start_00(message: types.Message):
    start_time = '18'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='19')
async def set_start_00(message: types.Message):
    start_time = '19'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='20')
async def set_start_00(message: types.Message):
    start_time = '20'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='21')
async def set_start_00(message: types.Message):
    start_time = '21'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='22')
async def set_start_00(message: types.Message):
    start_time = '22'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)

@dp.callback_query_handler(text='23')
async def set_start_00(message: types.Message):
    start_time = '23'
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {start_time}.")).message_id
    print(msg_id)
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            day_meet = find_table[index]['fields']['UserDateSlot'] # дата из БД
            pared_time = f'\U0001F5D3 {day_meet} {start_time}:00 - {start_time}:40' # подготовка под будущее сообщение
            new_time_slot = day_meet+' '+start_time+':00:00' # строковый ТС
            user_UTC = find_table[index]['fields']['UTC'] # UTC пациента
            user_time_slot = datetime.strptime(new_time_slot, '%Y-%m-%d %H:%M:%S') # строковый ТС --> в datatime
            if user_UTC[0] == '+': # смотрим что UTC положительный
                server_time_slot = user_time_slot - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            else: # смотрим что UTC отрицательный
                server_time_slot = user_time_slot + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                          minutes=int(user_UTC[3]+user_UTC[4])) # datetime выбора юзверя в серверное datetime
            s_now = datetime.now().strftime('%Y-%m-%d %H') # дата и час сейчас на сервере
            serv_now = s_now+':00:00' # округляшки серверного времение
            server_now = datetime.strptime(serv_now, '%Y-%m-%d %H:%M:%S') # перевод из строки в datetime
            server_simile = server_now + timedelta(hours=2) # добавка 2 часа чтобы точно успели оповещения придти
            if user_UTC[0] == '+': # смотрим что UTC положительный
                user_ts_min = server_now + timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            else: # смотрим что UTC отрицательный
                user_ts_min = server_now - timedelta(hours=int(user_UTC[1]+user_UTC[2]),
                                                    minutes=int(user_UTC[3]+user_UTC[4])) # формирование времени пользователя 
            u_TS_min = user_ts_min + timedelta(hours=2) # формирование минимального времени которое пользователь может указать
            user_min_TS = u_TS_min.strftime('%Y-%m-%d %H:%M') # перевод минимального ТС в строковый формат
            if server_simile <= server_time_slot:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {pared_time}\n\
We saved your choice and would like to send a notification once we find a partner.")).message_id
                print(msg_id)
                table.update(str(element_id), {'ServerTimeSlot': str(server_time_slot)})
                table.update(str(element_id), {'UserTimeSlot': new_time_slot})
                await menu(message)
            else:
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Please select a date and time no earlier than {user_min_TS}", reply_markup=HOUR)).message_id
                print(msg_id)


# async def get_start_time(message: types.Message, state: FSMContext):
#     pattern = r'^0[0-9]|1[0-9]|2[0-3]$'
#     if re.fullmatch(pattern, message.text):
#         await state.update_data(start_time=message.text)
#         msg_id = (await bot.send_message(message.from_user.id, f"You chose {message.text}.")).message_id
#         print(msg_id)
#         data = await state.get_data()
#         week_day = data.get('week_day')
#         start_time = data.get('start_time')
#         user_time_slot = week_day + start_time
#         find_table = table.all()
#         element_id = ''
#         for index in range(len(find_table)):
#             if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
#                 element_id = find_table[index]['id']
#                 msg_id = (await bot.send_message(message.from_user.id, 
#                     text=f"Your Time-Slot - {user_time_slot}:00 - {start_time}:40.")).message_id
#                 print(msg_id)
#                 table.update(str(element_id), {'UserTimeSlot': user_time_slot})
#                 await state.finish()
#                 await menu(message)
#     else:
#         msg_id = (await bot.send_message(message.from_user.id, 
#             text='Sorry, this is not a valid time value. \nPlease re-enter numbers from 00 to 23.')).message_id
#         print(msg_id)


def register_handlers_time_slot(dp: Dispatcher):
    dp.register_message_handler(time_slot_input, commands=['timeslot'])
    # dp.register_message_handler(get_week_day, state=TimeSlot.week_day)
    # dp.register_message_handler(get_start_time, state=TimeSlot.start_time)
