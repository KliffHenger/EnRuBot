from aiogram import types, Dispatcher
from user_states import TimeSlot
from aiogram.dispatcher import FSMContext
from keyboards.time_slot import WEEK
from keyboards.inline_menu import G_MENU
from airtable_config import table
from utils.menu import menu
from config import dp, bot

import re



'''(1)Начало ввода ТаймСлота(старт "машины состояний")'''
@dp.callback_query_handler(text='timeslot')
async def callback_timeslot_input(message: types.Message):
    all_table = table.all()
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            record_id = all_table[index]['id']  # достает record_id из БД
            msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Please select a possible day for your meeting.", reply_markup=WEEK)).message_id
            print(msg_id)
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
            await TimeSlot.week_day.set()

async def time_slot_input(message: types.Message):
    all_table = table.all()
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            record_id = all_table[index]['id']  # достает record_id из БД
            msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Please select a possible day for your meeting.", reply_markup=WEEK)).message_id
            print(msg_id)
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
            await TimeSlot.week_day.set()


'''(2)Ввод дня недели'''

async def get_week_day(message: types.Message,  state: FSMContext):
    pattern = r'MO|TU|WE|TH|FR|SA|SU'
    if re.fullmatch(pattern, message.text):
        await state.update_data(week_day=message.text)
        all_table = table.all()
        for index in range(len(all_table)):
            if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                record_id = all_table[index]['id']  # достает record_id из БД
                msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                msg_id = (await bot.send_message(message.from_user.id, 
                    f"Great. You've selected - {message.text}.\nNext, please write in the time you would be comfortable to start at: \nFor example: 17 or 09.")).message_id
                print(msg_id)
                table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
                await TimeSlot.start_time.set()
    else:
        all_table = table.all()
        for index in range(len(all_table)):
            if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                record_id = all_table[index]['id']  # достает record_id из БД
                msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                msg_id = (await bot.send_message(message.from_user.id, 
                    text='Oops! Wrong format!\nTry again, please. Make sure you use the keyboard.', reply_markup=WEEK)).message_id
                print(msg_id)
                table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД


# '''(3)Ввод времени начала'''
# async def get_start_time(message: types.Message, state: FSMContext):
#     pattern = r'^0[0-9]|1[0-9]|2[0-3]$'
#     if re.fullmatch(pattern, message.text):
#         await state.update_data(start_time=message.text)
#         await message.answer(f"Вы выбрали {message.text}.")
#         await TimeSlot.end_time.set()
#     else:
#         await message.answer(text='Вы ввели что-то не то. \nКорректный формат от 00 до 23')


# '''(4)Ввод времени конца (завершение "машины состояний")'''
# async def get_end_time(message: types.Message, state: FSMContext):
#     await state.update_data(end_time=message.text)
#     data = await state.get_data()
#     week_day = data.get('week_day')
#     start_time = data.get('start_time')
#     end_time = data.get('end_time')
#     user_time_slot = week_day+start_time+end_time
#     find_table = table.all()
#     element_id = ''
#     for index in range(len(find_table)):
#         if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
#             element_id = find_table[index]['id']
#     await message.answer(f"Ваш тайм-слот - {user_time_slot}-00 - {start_time}-40.")
#     table.update(str(element_id), {'UserTimeSlot': user_time_slot})
#     await state.finish()
#     await menu(message)

    '''
    (3v2-4v2)Ввод времени начала (завершение "машины состояний")
    Закомментить/раскомментить что необходимо
    '''


async def get_start_time(message: types.Message, state: FSMContext):
    pattern = r'^0[0-9]|1[0-9]|2[0-3]$'
    if re.fullmatch(pattern, message.text):
        await state.update_data(start_time=message.text)
        msg_id = (await bot.send_message(message.from_user.id, f"You chose {message.text}.")).message_id
        print(msg_id)
        # await bot.delete_message(message.from_user.id, msg_id-2)
        # await message.delete()
        data = await state.get_data()
        week_day = data.get('week_day')
        start_time = data.get('start_time')
        user_time_slot = week_day + start_time
        find_table = table.all()
        element_id = ''
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                element_id = find_table[index]['id']
                msg_id = (await bot.send_message(message.from_user.id, 
                    text=f"Your Time-Slot - {user_time_slot}-00 - {start_time}-40.")).message_id
                print(msg_id)
                # await bot.delete_message(message.from_user.id, msg_id-1)
                table.update(str(element_id), {'UserTimeSlot': user_time_slot})
                await state.finish()
                await menu(message)
    else:
        msg_id = (await bot.send_message(message.from_user.id, 
            text='Sorry, this is not a valid time value. \nPlease re-enter numbers from 00 to 23.')).message_id
        print(msg_id)
        # await bot.delete_message(message.from_user.id, msg_id-2)
        # await message.delete()


def register_handlers_time_slot(dp: Dispatcher):
    dp.register_message_handler(time_slot_input, commands=['timeslot'])
    dp.register_message_handler(get_week_day, state=TimeSlot.week_day)
    dp.register_message_handler(get_start_time, state=TimeSlot.start_time)
    # dp.register_message_handler(get_end_time, state=TimeSlot.end_time)  раскомментить если понадобится
