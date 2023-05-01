from config import bot, dp, sched
from aiogram import types, Dispatcher
from airtable_config import table
from .meeting import createMeeting
from .intention_meet import intention_status
from datetime import datetime, timedelta
from keyboards.inline_menu import G_MENU, CONF_MEET
from keyboards.inline_intention_meet import KB_intention_status




def meet_connect(first_user_tg_id: str):
    meeting_link, join_password = createMeeting()
    find_table = table.all()
    global first_record_id
    global second_record_id
    global second_user_tg_id
    # global first_user_tg_id
    global first_UTC
    first_record_id, first_user_eng_level, first_user_time_slot, first_server_time_slot, first_UTC, \
    second_record_id, second_user_tg_id = '', '', '', '', '', '', ''
    is_pared = False
    for index in range(len(find_table)): # начало цикла подбора, вытягивание инициатора из БД
        if find_table[index]['fields']['UserIDTG'] == first_user_tg_id:
            first_user_eng_level = find_table[index]['fields']['UserEngLevel']
            first_server_time_slot = find_table[index]['fields']['ServerTimeSlot']
            first_record_id = find_table[index]['id']
    for index in range(len(find_table)):  # вытягивание собеседника из БД
        if find_table[index]['fields']['UserIDTG'] != first_user_tg_id \
                and find_table[index]['fields']['UserEngLevel'] == first_user_eng_level \
                and find_table[index]['fields']['ServerTimeSlot'] == first_server_time_slot \
                and find_table[index]['fields']['IsPared'] == 'False':
            second_user_tg_id = find_table[index]['fields']['UserIDTG']
            second_record_id = find_table[index]['id']
            is_pared = True

            '''начинаем обновлять данные в БД и тут же получаем кое что обратно'''
    if is_pared == True:
        last_find = datetime.now() # тут получаем текущее время на момент поиска собеседника
        str_last_find = last_find.strftime('%Y-%m-%d %H:%M:%S') # приводим datetime к формату для БД
        table.update(record_id=first_record_id, fields={'LastFindPeer': str_last_find}) # пишем в БД время последнего поиска собеседника для доминанта
        table.update(record_id=second_record_id, fields={'LastFindPeer': str_last_find}) # пишем в БД время последнего поиска собеседника для сабмисива
        table.update(record_id=first_record_id, fields={'IsPared': "True"})
        table.update(record_id=second_record_id, fields={'IsPared': "True"})
        table.update(record_id=first_record_id, fields={'IsParedID': second_user_tg_id})
        table.update(record_id=second_record_id, fields={'IsParedID': first_user_tg_id})
        f_dict = table.get(first_record_id)
        first_tg_id = f_dict['fields']['UserIDTG']
        second_tg_id = f_dict['fields']['IsParedID']
        '''тут мы каждому пользователю выдаем по планировщику'''
        name_sched = 'sch'+first_tg_id
        '''названия задач'''
        list_jobs = '_1', '_2', '_3', '_4', '_5', '_6', '_7'
        
        table.update(record_id=first_record_id, fields={'JobName': name_sched})
        table.update(record_id=second_record_id, fields={'JobName': name_sched})
        '''этот кусок кода отвечет за формирование необходимых дат для отсрочки сообщений'''
        # datetime_meet = str(first_user_time_slot)+",00,00"
        dt_meet = datetime.strptime(first_server_time_slot, "%Y-%m-%d %H:%M:%S") # 2023-03-30 23:00:00
        start_alert60 = dt_meet - timedelta(minutes=60)
        start_alert30 = dt_meet - timedelta(minutes=30)
        start_alert15 = dt_meet - timedelta(minutes=15)
        start_alert5 = dt_meet - timedelta(minutes=5)
        dt_meet39 = dt_meet + timedelta(minutes=39)
        dt_meet40 = dt_meet + timedelta(minutes=40)

        '''тут мы собираем квардс для передачи в планировщик'''
        mess = {'first_tg_id': first_tg_id, 'second_tg_id': second_tg_id}
        bd = {'first_record_id':first_record_id, 'second_record_id':second_record_id}
        mess_bd = {'first_tg_id': first_tg_id, 'second_tg_id': second_tg_id, 
                'first_record_id':first_record_id, 'second_record_id':second_record_id}

        '''быстрые задания для тестов'''
        # strt_alert60 = last_find + timedelta(seconds=10)
        # strt_alert30 = last_find + timedelta(seconds=40)
        # strt_alert15 = last_find + timedelta(seconds=50)
        # strt_alert5 = last_find + timedelta(seconds=60)
        # strt_alert = last_find + timedelta(seconds=70)
        # d_meet39 = last_find + timedelta(seconds=80)
        # d_meet40 = last_find + timedelta(seconds=90)
        # sched.add_job(send_message_cron60, trigger='date', run_date=strt_alert60, kwargs={'mess_bd': mess_bd}, 
                                        # misfire_grace_time=3, id=name_sched+list_jobs[6])
        # sched.add_job(send_message_cron30, trigger='date', run_date=strt_alert30, kwargs={'mess_bd': mess_bd}, 
                                        # misfire_grace_time=3, id=name_sched+list_jobs[5])
        # sched.add_job(send_message_cron15, trigger='date', run_date=strt_alert15, kwargs={'mess': mess}, 
                                        # misfire_grace_time=3, id=name_sched+list_jobs[4])
        # sched.add_job(send_message_cron5, trigger='date', run_date=strt_alert5, kwargs={'mess': mess}, 
                                        # misfire_grace_time=3, id=name_sched+list_jobs[3])
        # sched.add_job(send_message_cron, trigger='date', run_date=strt_alert, kwargs={'mess': mess}, 
                                        # misfire_grace_time=3, id=name_sched+list_jobs[2])
        # sched.add_job(send_message_postmeet, trigger='date', run_date=d_meet40, kwargs={'mess_bd': mess_bd}, 
                                        # misfire_grace_time=3, id=name_sched+list_jobs[1])
        # sched.add_job(update_cron, trigger='date', run_date=d_meet39, kwargs={'bd': bd}, 
                                        # misfire_grace_time=3, id=name_sched+list_jobs[0])
        # sched.print_jobs()
        # return str(first_record_id), str(second_record_id)
        
        """непосредственно добавление заданий в обработчик"""
        sched.add_job(send_message_cron60, trigger='date', run_date=str(start_alert60), kwargs={'mess_bd': mess_bd}, 
                                        misfire_grace_time=3, id=name_sched+list_jobs[6])
        sched.add_job(send_message_cron30, trigger='date', run_date=str(start_alert30), kwargs={'mess_bd': mess_bd}, 
                                        misfire_grace_time=3, id=name_sched+list_jobs[5])
        sched.add_job(send_message_cron15, trigger='date', run_date=str(start_alert15), kwargs={'mess': mess}, 
                                        misfire_grace_time=3, id=name_sched+list_jobs[4])
        sched.add_job(send_message_cron5, trigger='date', run_date=str(start_alert5), kwargs={'mess': mess}, 
                                        misfire_grace_time=3, id=name_sched+list_jobs[3])
        sched.add_job(send_message_cron, trigger='date', run_date=str(dt_meet), kwargs={'mess': mess}, 
                                        misfire_grace_time=3, id=name_sched+list_jobs[2])
        sched.add_job(send_message_postmeet, trigger='date', run_date=str(dt_meet40), kwargs={'mess_bd': mess_bd}, 
                                        misfire_grace_time=3, id=name_sched+list_jobs[1])
        sched.add_job(update_cron, trigger='date', run_date=str(dt_meet39), kwargs={'bd': bd}, 
                                        misfire_grace_time=3, id=name_sched+list_jobs[0])
        sched.print_jobs()
        print(first_record_id, second_record_id)
        return str(first_record_id), str(second_record_id)

"""непосредственно наши сообщения которые будут приходить перед началом + работа с БД"""
async def send_message_cron60(mess_bd):
    first_tg_id = mess_bd['first_tg_id']
    second_tg_id = mess_bd['second_tg_id']
    first_record_id = mess_bd['first_record_id']
    second_record_id = mess_bd['second_record_id']
    msg_id1 = (await bot.send_message(chat_id=int(first_tg_id), 
                            text=f'The meeting will begin in 1 hour.\nВы будете присутствовать?', 
                            reply_markup=KB_intention_status)).message_id
    msg_id2 = (await bot.send_message(chat_id=int(second_tg_id), 
                            text=f'The meeting will begin in 1 hour.\nВы будете присутствовать?', 
                            reply_markup=KB_intention_status)).message_id
    table.update(record_id=str(first_record_id), fields={'msgIDforDEL': str(msg_id1)})
    table.update(record_id=str(second_record_id), fields={'msgIDforDEL': str(msg_id2)})
async def send_message_cron30(mess_bd):
    first_tg_id = mess_bd['first_tg_id']
    second_tg_id = mess_bd['second_tg_id']
    first_record_id = mess_bd['first_record_id']
    second_record_id = mess_bd['second_record_id']
    await bot.send_message(chat_id=int(first_tg_id), text=f'The meeting will begin in 30 minutes.')
    await bot.send_message(chat_id=int(second_tg_id), text=f'The meeting will begin in 30 minutes.')
    await intention_status(first_record_id, second_record_id)
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
    table.update(record_id=str(first_record_id), fields={'IsPared': 'False'})
    table.update(record_id=str(second_record_id), fields={'IsPared': 'False'})
    table.update(record_id=str(first_record_id), fields={'UserTimeSlot': 'None'})
    table.update(record_id=str(second_record_id), fields={'UserTimeSlot': 'None'})
    table.update(record_id=str(first_record_id), fields={'ServerTimeSlot': 'None'})
    table.update(record_id=str(second_record_id), fields={'ServerTimeSlot': 'None'})
    table.update(record_id=str(first_record_id), fields={'In_Status': 'None'})
    table.update(record_id=str(second_record_id), fields={'In_Status': 'None'})

"""функция проверки джобов в планировщике"""
async def djobumne(message: types.Message):
    print(sched.get_jobs())

    
def register_handlers_connect(dp: Dispatcher):
    dp.register_message_handler(djobumne, commands=['djobumne']) # это команда для проверки джобов
    dp.register_message_handler(send_message_cron60, commands=['40000_monkeys_put_a_banana_up_their_butt'])
    dp.register_message_handler(send_message_cron30, commands=['40000_monkeys_put_a_banana_up_their_butt'])
    dp.register_message_handler(send_message_cron15, commands=['40000_monkeys_put_a_banana_up_their_butt'])
    dp.register_message_handler(send_message_cron5, commands=['40000_monkeys_put_a_banana_up_their_butt'])
    dp.register_message_handler(send_message_cron, commands=['40000_monkeys_put_a_banana_up_their_butt'])
    dp.register_message_handler(send_message_postmeet, commands=['40000_monkeys_put_a_banana_up_their_butt'])
    dp.register_message_handler(update_cron, commands=['40000_monkeys_put_a_banana_up_their_butt'])