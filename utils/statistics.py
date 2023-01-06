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
            user_record_id = all_table[index]['id']
            msg_id = int(all_table[index]['fields']['msgIDforDEL'])
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
            await bot.send_message(message.from_user.id, text='Спасибо, ваш ответ сохранен.', reply_markup=G_MENU)
            await bot.delete_message(message.from_user.id, message_id=msg_id)
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
            await bot.send_message(message.from_user.id, text='Поздравляем! Вы успешно провели 15 встреч.', reply_markup=G_MENU)
            await bot.delete_message(message.from_user.id, message_id=msg_id)
            

@dp.callback_query_handler(text='role_candidate')
async def save_role_candidate(message: types.Message):
    all_table = table.all()
    eng_level, hour_goal = '', ''
    u_stat = {}
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and all_table[index]['fields']['UserHourGoal'] != '0':
            user_record_id = all_table[index]['id']
            msg_id = int(all_table[index]['fields']['msgIDforDEL'])
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
            await bot.send_message(message.from_user.id, text='Спасибо, ваш ответ сохранен.', reply_markup=G_MENU)
            await bot.delete_message(message.from_user.id, message_id=msg_id)
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
            await bot.send_message(message.from_user.id, text='Поздравляем! Вы успешно провели 15 встреч.', reply_markup=G_MENU)
            await bot.delete_message(message.from_user.id, message_id=msg_id)



@dp.callback_query_handler(text='statistics')
async def get_statistics(message: types.Message):
    all_table = table.all()
    bad_list = []
    msg_list = []
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            user_stat = eval(all_table[index]['fields']['UserStatistics'])
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
        await bot.send_message(message.from_user.id, text=f'Ваша статистика по ролям:\n{stat_msg}', reply_markup=G_MENU)
    elif bad_list == msg_list:
        await bot.send_message(message.from_user.id, text=f'Данных пока нет. Не игнорируйте сообщение после встречи.', reply_markup=G_MENU)




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