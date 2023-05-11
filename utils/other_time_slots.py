from aiogram import types, Dispatcher
from airtable_config import table
from .meeting import createMeeting
from config import bot, dp, sched
from .time_slot import time_slot_input
from .connect import meet_connect
from .menu import menu
from keyboards.inline_menu import G_MENU, U_STAT, C_MEET_MENU, SET_ENlvl_and_TS, SET_TS
from keyboards.inline_free_timeslot import genmarkup
from utils.simple_calendar import calendar_callback as simple_cal_callback, SimpCalendar
from datetime import datetime, timedelta
from user_states import TS
from aiogram.dispatcher import FSMContext
import re



@dp.callback_query_handler(text='other_time_slots')
async def callback_other_time_slots(message: types.Message):
    find_table = table.all()
    global first_user_record_id
    global second_user_record_id
    global second_user_tg_id
    global first_user_tg_id
    global first_server_time_slot
    global first_UTC
    first_user_record_id, first_user_eng_level, first_user_time_slot, first_server_time_slot, first_UTC, \
    second_user_record_id, second_user_tg_id = '', '', '', '', '', '', ''
    first_user_tg_id = str(message.from_user.id)
    more_found = False
    list_TS = []
    for index in range(len(find_table)): # начало цикла подбора, вытягивание инициатора из БД
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            first_user_eng_level = find_table[index]['fields']['UserEngLevel']
            first_server_time_slot = find_table[index]['fields']['ServerTimeSlot']
            list_TS.append(first_server_time_slot)
            first_user_time_slot = find_table[index]['fields']['UserTimeSlot']
            f_UTC = find_table[index]['fields']['UTC']
            first_user_fname = find_table[index]['fields']['UserName']
            first_user_record_id = find_table[index]['id']
    for index in range(len(find_table)): # отработка цикла возможных пар
        if find_table[index]['fields']['UserIDTG'] != str(message.from_user.id) \
            and find_table[index]['fields']['UserEngLevel'] == first_user_eng_level \
            and find_table[index]['fields']['ServerTimeSlot'] != 'None' \
            and find_table[index]['fields']['IsPared'] == 'False':
            more_time_slot = str(find_table[index]['fields']['ServerTimeSlot'])
            user_name = str(find_table[index]['fields']['UserName'])
            for_list = more_time_slot+str(f_UTC)+user_name
            list_TS.append(for_list)
            more_found = True
    if more_found == True: # уровень языка совпадает хоть с кем нибудь, смените ТаймСлот
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                record_id = find_table[index]['id']  # достает record_id из БД
                old_uTS = str(find_table[index]['fields']['UserTimeSlot'])
                try:
                    msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                except:
                    pass
                try:
                    await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                except:
                    pass
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f'There is an opportunity to chat at this time:',
                    reply_markup=genmarkup(list_TS))).message_id
                # await bot.send_message(message.from_user.id, text=f'Your current time slot - \U0001F5D3 {old_uTS[:16]} \U0001F5D3.', reply_markup=G_MENU)
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
                    text="Sorry, we couldn't find a match for that time. \
Could you try another language level or suggest a time slot that works for you?",
                    reply_markup=SET_ENlvl_and_TS)).message_id
                table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  # запись msg_id в БД
                print(msg_id)


'''это берет данные из сгенерированой клавиатуры со свободными ТС'''
@dp.callback_query_handler(state=TS.time_slot)
async def set_timeslot(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(time_slot=callback_query.data)
    all_table = table.all() # получаем всю таблицу
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(callback_query.from_user.id):
            old_sTS = str(all_table[index]['fields']['ServerTimeSlot'])
            old_uTS = str(all_table[index]['fields']['UserTimeSlot'])
            first_UTC = all_table[index]['fields']['UTC']
            record_id = all_table[index]['id']  # достает record_id из БД
            raw_time_slot = callback_query.data
            time_slot = raw_time_slot[:19]
            pattern = r'^(?:19[0-9][0-9]|20[0-9][0-9])-(?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12][0-9]|3[01])+([, ])+(0[0-9]|1[0-9]|2[0-3])+(:)+([0-5][0-9])+(:)+([0-5][0-9])$'
            if raw_time_slot == old_sTS:
                await bot.send_message(callback_query.from_user.id, text=f'Your Time-Slot now - {old_uTS[:16]}.', reply_markup=G_MENU)
                # table.update(record_id=str(record_id), fields={'ServerTimeSlot': time_slot})
                await state.finish()
            else:
                if re.fullmatch(pattern, time_slot):
                    delta_hours = int(first_UTC[1]+first_UTC[2]) # +0100
                    delta_minutes = int(first_UTC[3]+first_UTC[4])
                    s_time = datetime.strptime(time_slot, "%Y-%m-%d %H:%M:%S")
                    if first_UTC[0] == '+':  # смотрим что UTC положительный
                        u_time = str(s_time + timedelta(hours=delta_hours, minutes=delta_minutes))
                    else: # смотрим что UTC отрицательный
                        u_time = str(s_time - timedelta(hours=delta_hours, minutes=delta_minutes))
                    pared_time = f'\U0001F5D3 {u_time[:16]}'
                    pared_hour = f'{u_time[11:14]}'
                    old_pared_time = f'\U0001F5D3 {old_uTS[:16]}'
                    try:
                        msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                    except:
                        pass
                    try:
                        await bot.delete_message(callback_query.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                    except:
                        pass
                    msg_id = (await bot.send_message(callback_query.from_user.id, text=f'Your Time-Slot - {pared_time} - {pared_hour}40.')).message_id
                    table.update(record_id=str(record_id), fields={'ServerTimeSlot': time_slot})
                    table.update(record_id=str(record_id), fields={'UserTimeSlot': u_time})
                    table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  # запись msg_id в БД
                    await state.finish()
                    first_record_id, second_record_id = meet_connect(first_user_tg_id) # ВАЖНО! Функция получает ID, мэтчит и выдает record_id пользователей из пары
                    f_dict = table.get(first_record_id)
                    s_dict = table.get(second_record_id)
                    first_user_time_slot = f_dict['fields']['UserTimeSlot']
                    first_user_fname = f_dict['fields']['UserName']
                    second_user_fname = s_dict['fields']['UserName']
                    second_tg_id = s_dict['fields']['UserIDTG']
                    second_user_time_slot = s_dict['fields']['UserTimeSlot']
                    '''тут у нас выдача сообщений про успешный метчинг'''
                    await bot.send_message(callback_query.from_user.id, 
                        text=f'We have found a match for you.\nYour meeting starts on \U0001F5D3 {first_user_time_slot[:16]}')
                    for index in range(len(all_table)):
                        if all_table[index]['fields']['UserIDTG'] == str(callback_query.from_user.id):
                            try:
                                msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                            except:
                                pass
                            try:
                                await bot.delete_message(callback_query.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                            except:
                                pass
                            msg_id1 = (await bot.send_message(callback_query.from_user.id, 
                                text=f'You will have a Zoom-meeting with - \U0001F464 {second_user_fname}\nWe would like to send a reminder one hour before the call.', 
                                reply_markup=C_MEET_MENU)).message_id
                            table.update(record_id=str(first_record_id), fields={"msgIDforDEL": str(msg_id1)})  #запись msg_id в БД

                    '''тут сообщение для сабмисива'''
                    await bot.send_message(chat_id=int(second_tg_id), 
                        text=f'We have found a match for you.\nYour meeting starts on \U0001F5D3 {second_user_time_slot[:16]}')
                    for index in range(len(all_table)):
                        if all_table[index]['fields']['UserIDTG'] == second_tg_id:
                            try:
                                msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                            except:
                                pass
                            try:
                                await bot.delete_message(int(second_tg_id), message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                            except:
                                pass
                            msg_id2 = (await bot.send_message(chat_id=int(second_tg_id), 
                                text=f'You will have a Zoom-meeting with - \U0001F464 {first_user_fname}\nWe would like to send a reminder one hour before the call.', 
                                reply_markup=C_MEET_MENU)).message_id
                            table.update(record_id=str(second_record_id), fields={"msgIDforDEL": str(msg_id2)})  #запись msg_id в БД
                else:
                    print('Exept')
                    await state.finish()
                    all_table = table.all()
                    for index in range(len(all_table)):
                        if all_table[index]['fields']['UserIDTG'] == str(callback_query.from_user.id):
                            record_id = all_table[index]['id']  # достает record_id из БД
                            msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                            await bot.delete_message(callback_query.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                            msg_id = (await bot.send_message(callback_query.from_user.id, 
                                text=f"Please select a possible day for your meeting.", reply_markup=await SimpCalendar().start_calendar())).message_id
                            print(msg_id)
                            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
            # except :
            #     print('Exept Val')
            #     await state.finish()
            #     message = callback_query.message
            #     await time_slot_input(message)


            

    




'''выбор роли после успешного митинга'''
@dp.callback_query_handler(text='select_role')
async def callback_select_role(message: types.Message):
    all_table = table.all()
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            record_id = all_table[index]['id']  # достает record_id из БД
            try:
                msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            except:
                print('msg_id не нашелся в БД')
            try:
                await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            except:
                print('Бот не смог удалить сообщение')
            msg_id = (await bot.send_message(
                message.from_user.id, text=f'Please fill out the form at [LINK]\n\n\
What was your role in the speaking practice?', reply_markup=U_STAT)).message_id
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД


"""сценарий при неуспешном митинге"""
@dp.callback_query_handler(text='fail_meet')
async def callback_fail_meet(message: types.Message):
    all_table = table.all()
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            record_id = all_table[index]['id']  # достает record_id из БД
            leave_score = int(all_table[index]['fields']['LeaveMeeting'])
            try:
                msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            except:
                print('msg_id не нашелся в БД')
            try:
                await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            except:
                print('Бот не смог удалить сообщение')
                    
            new_leave = leave_score+1
            msg_id = (await bot.send_message(
                message.from_user.id, text=f"\U0001F62D We're sorry to hear that. We hope it works out better next time.", reply_markup=G_MENU)).message_id
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
            table.update(record_id=str(record_id), fields={"LeaveMeeting": str(new_leave)})  #запись Ливнувших в БД


'''функция отмены митинга'''
@dp.callback_query_handler(text='cancel_meet')
async def callback_cancel_meet(message: types.Message):
    find_table = table.all()
    first_user_record_id, second_user_record_id, second_tg_id = '', '', ''
    job_name = ''
    is_found = False
    for index in range(len(find_table)): # вытягивание инициатора отмены из БД
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            first_user_record_id = find_table[index]['id']
            job_name = find_table[index]['fields']['JobName']
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
        table.update(record_id=str(first_user_record_id), fields={'ServerTimeSlot': 'None'})
        table.update(record_id=str(first_user_record_id), fields={'In_Status': 'None'})
        table.update(record_id=str(second_user_record_id), fields={'In_Status': 'None'})
        try:
            sched.remove_job(job_name+'_1')
        except:
            print('Бот не нашел Джобу 1')
        try:
            sched.remove_job(job_name+'_2')
        except:
            print('Бот не нашел Джобу 2')
        try:
            sched.remove_job(job_name+'_3')
        except:
            print('Бот не нашел Джобу 3')
        try:
            sched.remove_job(job_name+'_4')
        except:
            print('Бот не нашел Джобу 4')
        try:
            sched.remove_job(job_name+'_5')
        except:
            print('Бот не нашел Джобу 5')
        try:
            sched.remove_job(job_name+'_6')
        except:
            print('Бот не нашел Джобу 6')
        try:
            sched.remove_job(job_name+'_7')
        except:
            print('Бот не нашел Джобу 7')
        try:
            sched.remove_job(job_name+'_8')
        except:
            print('Бот не нашел Джобу 8')
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
                    text=f'The meeting was canceled by your partner.', 
                    reply_markup=G_MENU)).message_id
                table.update(record_id=str(second_user_record_id), fields={"msgIDforDEL": str(msg_id2)})  #запись msg_id в БД


