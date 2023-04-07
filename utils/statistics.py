from aiogram import types, Dispatcher
from config import bot, dp
from keyboards.inline_menu import U_STAT, G_MENU
from airtable_config import table
import json
import aiogram
# from user_states import UserRole




@dp.callback_query_handler(text='role_hr')
async def save_role_hr(message: types.Message):
    all_table = table.all()
    eng_level, hour_goal = '', ''
    u_stat = {}
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and all_table[index]['fields']['UserHourGoal'] != '0':
            user_record_id = all_table[index]['id']  # достает record_id из БД
            msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            '''тут у нас ковыряние json-а и обновление его на +1'''
            eng_level = str(all_table[index]['fields']['UserEngLevel'])
            u_stat = eval(all_table[index]['fields']['UserStatistics'])
            u_eng_lvl = u_stat.get(eng_level)
            old_HR = u_eng_lvl.get('HR')
            u_eng_lvl['HR'] = old_HR + 1
            u_stat[eng_level] = u_eng_lvl
            table.update(record_id=str(user_record_id), fields={'UserStatistics': str(u_stat)})
            '''тут отнимаем от цели 1 встречу'''
            hour_goal = int(all_table[index]['fields']['UserHourGoal']) - 1
            table.update(record_id=str(user_record_id), fields={'UserHourGoal': str(hour_goal)})
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            msg_id = (await bot.send_message(message.from_user.id, 
                text='Thanks! Your reply has been saved!', reply_markup=G_MENU)).message_id
            print(msg_id)
            table.update(record_id=str(user_record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
        elif all_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and all_table[index]['fields']['UserHourGoal'] == '0':
            user_record_id = all_table[index]['id']
            msg_id = int(all_table[index]['fields']['msgIDforDEL'])
            '''тут у нас ковыряние json-а и обновление его на +1'''
            eng_level = str(all_table[index]['fields']['UserEngLevel'])
            u_stat = eval(all_table[index]['fields']['UserStatistics'])
            u_eng_lvl = u_stat.get(eng_level)
            old_HR = u_eng_lvl.get('HR')
            u_eng_lvl['HR'] = old_HR
            u_stat[eng_level] = u_eng_lvl
            table.update(record_id=str(user_record_id), fields={'UserStatistics': str(u_stat)})
            await bot.send_message(message.from_user.id, text="Well done! You've successfully had  15 meetings.", reply_markup=G_MENU)
            await bot.delete_message(message.from_user.id, message_id=msg_id)
            

@dp.callback_query_handler(text='role_candidate')
async def save_role_candidate(message: types.Message):
    all_table = table.all()
    eng_level, hour_goal = '', ''
    u_stat = {}
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and all_table[index]['fields']['UserHourGoal'] != '0':
            user_record_id = all_table[index]['id']  # достает record_id из БД
            msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            '''тут у нас ковыряние json-а и обновление его на +1'''
            eng_level = str(all_table[index]['fields']['UserEngLevel'])
            u_stat = eval(all_table[index]['fields']['UserStatistics'])
            u_eng_lvl = u_stat.get(eng_level)
            old_HR = u_eng_lvl.get('Candidate')
            u_eng_lvl['Candidate'] = old_HR + 1
            u_stat[eng_level] = u_eng_lvl
            table.update(record_id=str(user_record_id), fields={'UserStatistics': str(u_stat)})
            '''тут отнимаем от цели 1 встречу'''
            hour_goal = int(all_table[index]['fields']['UserHourGoal']) - 1
            table.update(record_id=str(user_record_id), fields={'UserHourGoal': str(hour_goal)})
            await bot.delete_message(message.from_user.id, message_id=msg_id_get)   # удаляет сообщение по msg_id из БД
            msg_id = (await bot.send_message(message.from_user.id, 
                text='Thanks! Your reply has been saved!', reply_markup=G_MENU)).message_id
            print(msg_id)
            table.update(record_id=str(user_record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
        elif all_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and all_table[index]['fields']['UserHourGoal'] == '0':
            user_record_id = all_table[index]['id']
            msg_id = int(all_table[index]['fields']['msgIDforDEL'])
            '''тут у нас ковыряние json-а и обновление его на +1'''
            eng_level = str(all_table[index]['fields']['UserEngLevel'])
            u_stat = eval(all_table[index]['fields']['UserStatistics'])
            u_eng_lvl = u_stat.get(eng_level)
            old_HR = u_eng_lvl.get('Candidate')
            u_eng_lvl['Candidate'] = old_HR
            u_stat[eng_level] = u_eng_lvl
            table.update(record_id=str(user_record_id), fields={'UserStatistics': str(u_stat)})
            await bot.send_message(message.from_user.id, text="Well done! You've successfully had  15 meetings.", reply_markup=G_MENU)
            await bot.delete_message(message.from_user.id, message_id=msg_id)



@dp.callback_query_handler(text='statistics')
async def get_statistics(message: types.Message):
    all_table = table.all()
    bad_list = []
    msg_list = []
    for index in range(len(all_table)):  # тут формируем список статистики
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            user_stat = eval(all_table[index]['fields']['UserStatistics'])
            user_hour_goal = all_table[index]['fields']['UserHourGoal']
            for index in user_stat:
                if user_stat[index]['HR'] != 0 or user_stat[index]['Candidate'] != 0:
                    eng_lvl = index
                    role = user_stat[eng_lvl]
                    strings = []
                    for key,item in role.items():
                        strings.append("{}: {}".format(key, item))
                    result = str(", ".join(strings))
                    all_list = eng_lvl +" ("+ result +")\n"
                    msg_list.append(all_list)
                    stat_msg =  ' '.join([str(elem) for elem in msg_list])
    if bad_list != msg_list:
        for index in range(len(all_table)):
            if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                record_id = all_table[index]['id']  # достает record_id из БД
                try:
                    msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                except:
                    pass
                try:
                    await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                except:
                    pass
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f'Your stats by roles:\n{stat_msg}\n\n\
You have {user_hour_goal} meetings (for 40 min) left to the goal.', reply_markup=G_MENU)).message_id
                print(msg_id)
                table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
    elif bad_list == msg_list:
        for index in range(len(all_table)):
            if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                record_id = all_table[index]['id']  # достает record_id из БД
                msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"No data on your statistics is available yet.\n\
For progress tracking please don't skip the message after the meeting.\n\n\
You have {user_hour_goal} meetings (for 40 min) left to the goal.", reply_markup=G_MENU)).message_id
                print(msg_id)
                table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД




    # await bot.send_message(message.from_user.id, """
    # -уровень английского с 01.01.2022 - <b>B1</b>\n
    # -количество встреч в роли HR - 2\n
    # -количество встреч в роли кандидата - 3\n
    # -количество часов в каждой роли:\n
    # в роли HR - 2 часа\n
    # в роли кандидата - 1 час\n
    # """, parse_mode='HTML', reply_markup=U_STAT)
    
            

# def register_handlers_statistics(dp: Dispatcher):
#     dp.register_message_handler(select_role)