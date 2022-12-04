from aiogram import types, Dispatcher
from airtable_config import table
from .meeting import createMeeting
from config import bot, dp
from .menu import menu
from keyboards.inline_menu import G_MENU
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio



@dp.callback_query_handler(text='find_interlocutor')
async def callback_find_companion(message: types.Message):
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

        await bot.send_message(message.from_user.id, text=f"Join new meeting: {meeting_link}")
        await bot.send_message(chat_id=int(second_user_tg_id), text=f"Hi! You can join new meeting: {meeting_link}")
        await asyncio.sleep(60)
        table.update(record_id=str(first_user_record_id), fields={'IsPared': "False"})
        table.update(record_id=str(second_user_record_id), fields={'IsPared': "False"})
    else:
        await bot.send_message(message.from_user.id, text='Извините, мы никого не смогли найти....', reply_markup=G_MENU)
        


async def find_companion(message: types.Message):
    """
    Функция поиска собеседника. Наша цель на данном этапе: найти человека с подходящими
    параметрами. На первом шаге мы ищем двоих пользователей в базе для получения данных.
    После данной операции нам необзодимо провести операцию сравнения. Если параметры языка и времени у
    пользователей совпадают, то они образуют пару. Если нет - бот выводит: 'Извините, мы никого не смогли найти....'.
    Ровно в этот момент их значения поля 'IsPared' в базе становится True.
    По истечению 40 минут (в данной функции пока что одна минута) их значение 'IsPared'
    снова снанет False.
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
