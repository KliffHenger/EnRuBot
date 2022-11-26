from aiogram import types, Dispatcher
from airtable_config import table
from .meeting import createMeeting
from config import bot
from .menu import menu


async def find_companion(message: types.Message):
    find_table = table.all()
    first_user_record_id, first_user_eng_level, first_user_time_slot, second_user_record_id, second_user_tg_id = '', '', '', '', ''
    is_found = False
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            first_user_eng_level = find_table[index]['fields']['UserEngLevel']
            first_user_time_slot = find_table[index]['fields']['UserTimeSlot']
            first_user_record_id = find_table[index]['id']
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] != str(message.from_user.id) and find_table[index]['fields']['UserEngLevel'] == first_user_eng_level and find_table[index]['fields']['UserTimeSlot'] == first_user_time_slot and find_table[index]['fields']['IsPared'] == 'False':
            second_user_tg_id = str(find_table[index]['fields']['UserIDTG'])
            second_user_record_id = find_table[index]['id']
            is_found = True
    if is_found:
        meeting_link, join_password = createMeeting()
        table.update(record_id=str(first_user_record_id), fields={'IsPared': "True"})
        table.update(record_id=str(second_user_record_id), fields={'IsPared': "True"})
        await message.answer(text=f"Join new meeting: {meeting_link}")
        await bot.send_message(chat_id=int(second_user_tg_id), text=f"Hi! You can join new meeting: {meeting_link}")
    else:
        await message.answer(text='Извините, мы никого не смогли найти....')
        await menu(message)


def register_handlers_find_interlocutor(dp: Dispatcher):
    dp.register_message_handler(find_companion, commands=['find_interlocutor'])



