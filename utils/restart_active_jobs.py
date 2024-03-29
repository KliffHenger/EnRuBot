from config import bot, dp, sched
from aiogram import types, Dispatcher
from .meeting import createMeeting
from .intention_meet import intention_status
from airtable_config import table
from keyboards.inline_menu import G_MENU, CONF_MEET
from keyboards.inline_intention_meet import KB_intention_status
from datetime import datetime, timedelta



async def for_rest():
    all_table = table.all()
    for index in range(len(all_table)):
        if all_table[index]['fields']['IsPared'] == 'True':
            record_id = all_table[index]['id']
            table.update(record_id=record_id, fields={'NoActive': 'True'})


async def restart_jobs():
    all_table = table.all()
    first_record_id, first_tg_id, first_server_time_slot, second_record_id, second_tg_id, job1_name = '', '', '', '', '', ''
    # is_found = False
    for index in range(len(all_table)):
        if all_table[index]['fields']['NoActive'] == 'True':
            first_tg_id = all_table[index]['fields']['UserIDTG']
            job1_name = all_table[index]['fields']['JobName']
            second_tg_id = all_table[index]['fields']['IsParedID']
            first_server_time_slot = all_table[index]['fields']['ServerTimeSlot']
            first_record_id = all_table[index]['id']
    for index in range(len(all_table)):  # вытягивание собеседника из БД
        if all_table[index]['fields']['UserIDTG'] != first_tg_id \
            and all_table[index]['fields']['NoActive'] == 'True' \
            and all_table[index]['fields']['UserIDTG'] == second_tg_id \
            and all_table[index]['fields']['JobName'] == job1_name:
            second_record_id = all_table[index]['id']
            # is_found = True
    # if is_found == True:
            list_jobs = '_1', '_2', '_3', '_4', '_5', '_6', '_7', '_8'
            if first_server_time_slot:    # этот кусок кода отвечет за формирование необходимых дат для отсрочки сообщений
                dt_meet = datetime.strptime(first_server_time_slot, "%Y-%m-%d %H:%M:%S") # 2023-03-30 23:00:00
                start_alert60 = dt_meet - timedelta(minutes=60)
                start_alert31 = dt_meet - timedelta(minutes=31)
                start_alert30 = dt_meet - timedelta(minutes=30)
                start_alert15 = dt_meet - timedelta(minutes=15)
                start_alert5 = dt_meet - timedelta(minutes=5)
                dt_meet40 = dt_meet + timedelta(minutes=40)
            '''тут мы собираем квардс для передачи в планировщик'''
            mess = {'first_tg_id': first_tg_id, 'second_tg_id': second_tg_id}
            print('Перезапуск заданий планировщика у '+str(mess))
            bd = {'first_record_id':first_record_id, 'second_record_id':second_record_id}
            mess_bd = {'first_tg_id': first_tg_id, 'second_tg_id': second_tg_id, 
                        'first_record_id':first_record_id, 'second_record_id':second_record_id}
            """непосредственно добавление заданий в обработчик"""
            sched.add_job(re_send_message_cron60, trigger='date', run_date=str(start_alert60), kwargs={'mess_bd': mess_bd}, 
                                                misfire_grace_time=3, id=job1_name+list_jobs[7])
            sched.add_job(re_status_meet31, trigger='date', run_date=str(start_alert31), kwargs={'mess_bd': mess_bd}, 
                                                misfire_grace_time=3, id=job1_name+list_jobs[6])
            sched.add_job(re_send_message_cron30, trigger='date', run_date=str(start_alert30), kwargs={'mess_bd': mess_bd}, 
                                                misfire_grace_time=3, id=job1_name+list_jobs[5])
            sched.add_job(re_send_message_cron15, trigger='date', run_date=str(start_alert15), kwargs={'mess': mess}, 
                                                misfire_grace_time=3, id=job1_name+list_jobs[4])
            sched.add_job(re_send_message_cron5, trigger='date', run_date=str(start_alert5), kwargs={'mess': mess}, 
                                                misfire_grace_time=3, id=job1_name+list_jobs[3])
            sched.add_job(re_send_message_cron, trigger='date', run_date=str(dt_meet), kwargs={'mess': mess}, 
                                                misfire_grace_time=3, id=job1_name+list_jobs[2])
            sched.add_job(re_send_message_postmeet, trigger='date', run_date=str(dt_meet40), kwargs={'mess_bd': mess_bd}, 
                                                misfire_grace_time=3, id=job1_name+list_jobs[1])
            sched.add_job(re_update_cron, trigger='date', run_date=str(dt_meet40), kwargs={'bd': bd}, 
                                                misfire_grace_time=3, id=job1_name+list_jobs[0])
            sched.print_jobs() 
            table.update(record_id=str(first_record_id), fields={'NoActive': 'False'})
            table.update(record_id=str(second_record_id), fields={'NoActive': 'False'})
            await restart_jobs()

"""непосредственно наши сообщения которые будут приходить перед началом + работа с БД"""
async def re_send_message_cron60(mess_bd):
    first_tg_id = mess_bd['first_tg_id']
    second_tg_id = mess_bd['second_tg_id']
    first_record_id = mess_bd['first_record_id']
    second_record_id = mess_bd['second_record_id']
    msg_id1 = (await bot.send_message(chat_id=int(first_tg_id), 
                            text=f'The meeting starts in an hour.\nAre you joining?', 
                            reply_markup=KB_intention_status)).message_id
    msg_id2 = (await bot.send_message(chat_id=int(second_tg_id), 
                            text=f'The meeting starts in an hour.\nAre you joining?', 
                            reply_markup=KB_intention_status)).message_id
    table.update(record_id=str(first_record_id), fields={'msgIDforDEL': str(msg_id1)})
    table.update(record_id=str(second_record_id), fields={'msgIDforDEL': str(msg_id2)})
async def re_status_meet31(mess_bd):
    first_tg_id = mess_bd['first_tg_id']
    second_tg_id = mess_bd['second_tg_id']
    first_record_id = mess_bd['first_record_id']
    second_record_id = mess_bd['second_record_id']
    f_table = table.get(first_record_id)
    s_table = table.get(second_record_id)
    try:
        msg1_id_get = int(f_table['fields']['msgIDforDEL'])  # достает msg1_id из БД
        msg2_id_get = int(s_table['fields']['msgIDforDEL'])  # достает msg2_id из БД
    except:
        print('msg_id не нашелся в БД')
    try:
        await bot.delete_message(int(first_tg_id), message_id=msg1_id_get) # удаляет сообщение по msg1_id из БД
        await bot.delete_message(int(second_tg_id), message_id=msg2_id_get) # удаляет сообщение по msg2_id из БД
    except:
        print('Бот не смог удалить сообщение')
    await intention_status(first_record_id, second_record_id)
async def re_send_message_cron30(mess_bd):
    first_tg_id = mess_bd['first_tg_id']
    second_tg_id = mess_bd['second_tg_id']
    await bot.send_message(chat_id=int(first_tg_id), text=f'The meeting will begin in 30 minutes.')
    await bot.send_message(chat_id=int(second_tg_id), text=f'The meeting will begin in 30 minutes.')
async def re_send_message_cron15(mess):
    first_tg_id = mess['first_tg_id']
    second_tg_id = mess['second_tg_id']
    await bot.send_message(chat_id=int(first_tg_id), text=f'The meeting will begin in 15 minutes.')
    await bot.send_message(chat_id=int(second_tg_id), text=f'The meeting will begin in 15 minutes.')
async def re_send_message_cron5(mess):
    first_tg_id = mess['first_tg_id']
    second_tg_id = mess['second_tg_id']
    await bot.send_message(chat_id=int(first_tg_id), text=f'The meeting will begin in 5 minutes.')
    await bot.send_message(chat_id=int(second_tg_id), text=f'The meeting will begin in 5 minutes.')
async def re_send_message_cron(mess):
    first_tg_id = mess['first_tg_id']
    second_tg_id = mess['second_tg_id']
    meeting_link, join_password = createMeeting()
    await bot.send_message(chat_id=int(first_tg_id), text=f'Join new meeting: {meeting_link}', reply_markup=G_MENU)
    await bot.send_message(chat_id=int(second_tg_id), text=f'Join new meeting: {meeting_link}', reply_markup=G_MENU)
async def re_send_message_postmeet(mess_bd):
    first_tg_id = mess_bd['first_tg_id']
    second_tg_id = mess_bd['second_tg_id']
    first_record_id = mess_bd['first_record_id']
    second_record_id = mess_bd['second_record_id']
    msg_id1 = (await bot.send_message(int(first_tg_id), text=f'Did the meeting take place?', reply_markup=CONF_MEET)).message_id
    msg_id2 = (await bot.send_message(int(second_tg_id), text=f'Did the meeting take place?', reply_markup=CONF_MEET)).message_id
    table.update(record_id=str(first_record_id), fields={'msgIDforDEL': str(msg_id1)})
    table.update(record_id=str(second_record_id), fields={'msgIDforDEL': str(msg_id2)})
async def re_update_cron(bd):
    first_record_id = bd['first_record_id']
    second_record_id = bd['second_record_id']
    table.update(record_id=str(first_record_id), fields={'IsPared': 'False'})
    table.update(record_id=str(second_record_id), fields={'IsPared': 'False'})
    table.update(record_id=str(first_record_id), fields={'UserTimeSlot': 'None'})
    table.update(record_id=str(second_record_id), fields={'UserTimeSlot': 'None'})
    table.update(record_id=str(first_record_id), fields={'ServerTimeSlot': 'None'})
    table.update(record_id=str(second_record_id), fields={'ServerTimeSlot': 'None'})
    table.update(record_id=str(first_record_id), fields={'In_Status': 'None'})
    table.update(record_id=str(second_record_id), fields={'In_Status': 'None'})





def register_handlers_restart_active_jobs(dp: Dispatcher):
    dp.register_message_handler(re_send_message_cron60, commands=['40000_monkeys_put_a_banana_up_their_butt'])
    dp.register_message_handler(re_status_meet31, commands=['40000_monkeys_put_a_banana_up_their_butt'])
    dp.register_message_handler(re_send_message_cron30, commands=['40000_monkeys_put_a_banana_up_their_butt'])
    dp.register_message_handler(re_send_message_cron15, commands=['40000_monkeys_put_a_banana_up_their_butt'])
    dp.register_message_handler(re_send_message_cron5, commands=['40000_monkeys_put_a_banana_up_their_butt'])
    dp.register_message_handler(re_send_message_cron, commands=['40000_monkeys_put_a_banana_up_their_butt'])
    dp.register_message_handler(re_send_message_postmeet, commands=['40000_monkeys_put_a_banana_up_their_butt'])
    dp.register_message_handler(re_update_cron, commands=['40000_monkeys_put_a_banana_up_their_butt'])