from config import bot, dp, sched
from aiogram import types, Dispatcher
from airtable_config import table
from keyboards.inline_menu import G_MENU


@dp.callback_query_handler(text=f'yes_i_will')
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
                message.from_user.id, text=f'Thank you, we will inform your partner.')).message_id
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
            table.update(record_id=str(record_id), fields={'In_Status': 'True'})  #запись In_Status в БД

@dp.callback_query_handler(text=f'no_i_will_not')
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
                message.from_user.id, text=f'Thank you, we will inform your partner.')).message_id
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
            table.update(record_id=str(record_id), fields={'In_Status': 'False'})  #запись In_Status в БД

async def intention_status(first_record_id: str, second_record_id: str):
    f_table = table.get(first_record_id)
    s_table = table.get(second_record_id)
    first_tg_id = f_table['fields']['UserIDTG']
    second_tg_id = s_table['fields']['UserIDTG']
    first_user_name = f_table['fields']['UserName']
    second_user_name = s_table['fields']['UserName']
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
    if f_table['fields']['In_Status'] == 'True' and s_table['fields']['In_Status'] == 'True': # 1 - Да, 2 - Да
        await bot.send_message(int(first_tg_id), text=f'{second_user_name} has confirmed their attendance.')
        await bot.send_message(int(second_tg_id), text=f'{first_user_name} has confirmed their attendance.')
    if f_table['fields']['In_Status'] == 'False' and s_table['fields']['In_Status'] == 'False': # 1 - Нет, 2 - Нет
        await bot.send_message(int(first_tg_id), text=f'Unfortunately, you do not intend to attend. We are going to cancel your meeting and notify your partner.', reply_markup=G_MENU)
        await bot.send_message(int(second_tg_id), text=f'Unfortunately, you do not intend to attend. We are going to cancel your meeting and notify your partner.', reply_markup=G_MENU)
        await cancel_meet(first_record_id, second_record_id)
    if f_table['fields']['In_Status'] == 'False' and s_table['fields']['In_Status'] == 'False': # 1 - Не знаю, 2 - Не знаю
        await bot.send_message(int(first_tg_id), text=f'You and {second_user_name} have not confirmed participation in the speaking practice. We will send you the reminders and a link, but we are not sure that the meeting will take place.')
        await bot.send_message(int(second_tg_id), text=f'You and {first_user_name} have not confirmed participation in the speaking practice. We will send you the reminders and a link, but we are not sure that the meeting will take place.')
    if f_table['fields']['In_Status'] == 'True' and s_table['fields']['In_Status'] == 'False': # 1 - Да, 2 - Нет
        await bot.send_message(int(first_tg_id), text=f'{second_user_name} has not confirmed their attendance. The meeting is canceled.', reply_markup=G_MENU)
        await bot.send_message(int(second_tg_id), text=f'Unfortunately, you do not intend to attend. We are going to cancel your meeting and notify your partner.', reply_markup=G_MENU)
        await cancel_meet(first_record_id, second_record_id)
    if f_table['fields']['In_Status'] == 'False' and s_table['fields']['In_Status'] == 'True': # 1 - Нет, 2 - Да
        await bot.send_message(int(first_tg_id), text=f'Unfortunately, you do not intend to attend. We are going to cancel your meeting and notify your partner.', reply_markup=G_MENU)
        await bot.send_message(int(second_tg_id), text=f'{first_user_name} has not confirmed their attendance. The meeting is canceled.', reply_markup=G_MENU)
        await cancel_meet(first_record_id, second_record_id)
    if f_table['fields']['In_Status'] == 'True' and s_table['fields']['In_Status'] == 'None': # 1 - Да, 2 - Не знаю
        await bot.send_message(int(first_tg_id), text=f'{second_user_name} have not confirmed participation in the speaking practice. We will send you the reminders and a link, but we are not sure that the meeting will take place.')
        await bot.send_message(int(second_tg_id), text=f"You have not confirmed participation in the speaking practice. We will send you the reminders and a link, but we are not sure that the meeting will take place.")
    if f_table['fields']['In_Status'] == 'None' and s_table['fields']['In_Status'] == 'True': # 1 - Не знаю, 2 - Да
        await bot.send_message(int(first_tg_id), text=f"You have not confirmed participation in the speaking practice. We will send you the reminders and a link, but we are not sure that the meeting will take place.")
        await bot.send_message(int(second_tg_id), text=f'{first_user_name} have not confirmed participation in the speaking practice. We will send you the reminders and a link, but we are not sure that the meeting will take place.')
    if f_table['fields']['In_Status'] == 'None' and s_table['fields']['In_Status'] == 'False': # 1 - Не знаю, 2 - Нет
        await bot.send_message(int(first_tg_id), text=f'{second_user_name} has not confirmed their attendance. The meeting is canceled.', reply_markup=G_MENU)
        await bot.send_message(int(second_tg_id), text=f'Unfortunately, you do not intend to attend. We are going to cancel your meeting and notify your partner.', reply_markup=G_MENU)
        await cancel_meet(first_record_id, second_record_id)
    if f_table['fields']['In_Status'] == 'False' and s_table['fields']['In_Status'] == 'None': # 1 - Нет, 2 - Не знаю
        await bot.send_message(int(first_tg_id), text=f'Unfortunately, you do not intend to attend. We are going to cancel your meeting and notify your partner.', reply_markup=G_MENU)
        await bot.send_message(int(second_tg_id), text=f'{first_user_name} has not confirmed their attendance. The meeting is canceled.', reply_markup=G_MENU)
        await cancel_meet(first_record_id, second_record_id)
    

async def cancel_meet(first_record_id: str, second_record_id: str):
    f_table = table.get(first_record_id)
    job_name = f_table['fields']['JobName']
    table.update(record_id=str(first_record_id), fields={'IsPared': 'False'})
    table.update(record_id=str(second_record_id), fields={'IsPared': 'False'})
    table.update(record_id=str(first_record_id), fields={'UserTimeSlot': 'None'}) # это сделано для исключения спама
    table.update(record_id=str(second_record_id), fields={'UserTimeSlot': 'None'}) # это сделано для исключения спама
    table.update(record_id=str(first_record_id), fields={'ServerTimeSlot': 'None'})
    table.update(record_id=str(second_record_id), fields={'ServerTimeSlot': 'None'})
    table.update(record_id=str(first_record_id), fields={'In_Status': 'None'})
    table.update(record_id=str(second_record_id), fields={'In_Status': 'None'})
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


def register_handlers_intention_meet(dp: Dispatcher):
    dp.register_message_handler(intention_status, commands=['3301_intention_status'])