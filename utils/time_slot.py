from aiogram import types, Dispatcher
from user_states import TimeSlot
from aiogram.dispatcher import FSMContext
from keyboards.inline_time_slot import WEEK, HOUR
from keyboards.inline_menu import G_MENU
from airtable_config import table
from utils.menu import menu
from config import dp, bot, week_dict

import re



'''(1)Начало ввода ТаймСлота(старт "машины состояний")'''
@dp.callback_query_handler(text='timeslot')
async def callback_timeslot_input(message: types.Message):
    all_table = table.all()
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

@dp.callback_query_handler(text='MO', state=TimeSlot.week_day)
async def set_week_MO(message: types.Message, state: FSMContext):
    txt = 'MO'
    await state.update_data(week_day=txt)
    all_table = table.all()
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            record_id = all_table[index]['id']  # достает record_id из БД
            msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            correct_week = week_dict.get(txt)
            msg_id = (await bot.send_message(message.from_user.id, 
                f"Great. You've selected - {correct_week}.\nNext, please write in the time you would be comfortable to start at:", 
                reply_markup=HOUR)).message_id
            print(msg_id)
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
            await TimeSlot.start_time.set()

@dp.callback_query_handler(text='TU', state=TimeSlot.week_day)
async def set_week_TU(message: types.Message, state: FSMContext):
    txt = 'TU'
    await state.update_data(week_day=txt)
    all_table = table.all()
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            record_id = all_table[index]['id']  # достает record_id из БД
            msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            correct_week = week_dict.get(txt)
            msg_id = (await bot.send_message(message.from_user.id, 
                f"Great. You've selected - {correct_week}.\nNext, please write in the time you would be comfortable to start at:", 
                reply_markup=HOUR)).message_id
            print(msg_id)
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
            await TimeSlot.start_time.set()

@dp.callback_query_handler(text='WE', state=TimeSlot.week_day)
async def set_week_WE(message: types.Message, state: FSMContext):
    txt = 'WE'
    await state.update_data(week_day=txt)
    all_table = table.all()
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            record_id = all_table[index]['id']  # достает record_id из БД
            msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            correct_week = week_dict.get(txt)
            msg_id = (await bot.send_message(message.from_user.id, 
                f"Great. You've selected - {correct_week}.\nNext, please write in the time you would be comfortable to start at:", 
                reply_markup=HOUR)).message_id
            print(msg_id)
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
            await TimeSlot.start_time.set()

@dp.callback_query_handler(text='TH', state=TimeSlot.week_day)
async def set_week_TH(message: types.Message, state: FSMContext):
    txt = 'TH'
    await state.update_data(week_day=txt)
    all_table = table.all()
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            record_id = all_table[index]['id']  # достает record_id из БД
            msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            correct_week = week_dict.get(txt)
            msg_id = (await bot.send_message(message.from_user.id, 
                f"Great. You've selected - {correct_week}.\nNext, please write in the time you would be comfortable to start at:", 
                reply_markup=HOUR)).message_id
            print(msg_id)
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
            await TimeSlot.start_time.set()

@dp.callback_query_handler(text='FR', state=TimeSlot.week_day)
async def set_week_FR(message: types.Message, state: FSMContext):
    txt = 'FR'
    await state.update_data(week_day=txt)
    all_table = table.all()
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            record_id = all_table[index]['id']  # достает record_id из БД
            msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            correct_week = week_dict.get(txt)
            msg_id = (await bot.send_message(message.from_user.id, 
                f"Great. You've selected - {correct_week}.\nNext, please write in the time you would be comfortable to start at:", 
                reply_markup=HOUR)).message_id
            print(msg_id)
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
            await TimeSlot.start_time.set()

@dp.callback_query_handler(text='SA', state=TimeSlot.week_day)
async def set_week_SA(message: types.Message, state: FSMContext):
    txt = 'SA'
    await state.update_data(week_day=txt)
    all_table = table.all()
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            record_id = all_table[index]['id']  # достает record_id из БД
            msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            correct_week = week_dict.get(txt)
            msg_id = (await bot.send_message(message.from_user.id, 
                f"Great. You've selected - {correct_week}.\nNext, please write in the time you would be comfortable to start at:", 
                reply_markup=HOUR)).message_id
            print(msg_id)
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
            await TimeSlot.start_time.set()

@dp.callback_query_handler(text='SU', state=TimeSlot.week_day)
async def set_week_SU(message: types.Message, state: FSMContext):
    txt = 'SU'
    await state.update_data(week_day=txt)
    all_table = table.all()
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            record_id = all_table[index]['id']  # достает record_id из БД
            msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            correct_week = week_dict.get(txt)
            msg_id = (await bot.send_message(message.from_user.id, 
                f"Great. You've selected - {correct_week}.\nNext, please write in the time you would be comfortable to start at:", 
                reply_markup=HOUR)).message_id
            print(msg_id)
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
            await TimeSlot.start_time.set()

'''(3)Ввод времени начала'''

@dp.callback_query_handler(text='00', state=TimeSlot.start_time)
async def set_start_00(message: types.Message, state: FSMContext):
    txt = '00'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='01', state=TimeSlot.start_time)
async def set_start_01(message: types.Message, state: FSMContext):
    txt = '01'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='02', state=TimeSlot.start_time)
async def set_start_02(message: types.Message, state: FSMContext):
    txt = '02'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='03', state=TimeSlot.start_time)
async def set_start_03(message: types.Message, state: FSMContext):
    txt = '03'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='04', state=TimeSlot.start_time)
async def set_start_04(message: types.Message, state: FSMContext):
    txt = '04'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='05', state=TimeSlot.start_time)
async def set_start_05(message: types.Message, state: FSMContext):
    txt = '05'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='06', state=TimeSlot.start_time)
async def set_start_06(message: types.Message, state: FSMContext):
    txt = '06'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='07', state=TimeSlot.start_time)
async def set_start_07(message: types.Message, state: FSMContext):
    txt = '07'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='08', state=TimeSlot.start_time)
async def set_start_08(message: types.Message, state: FSMContext):
    txt = '08'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='09', state=TimeSlot.start_time)
async def set_start_09(message: types.Message, state: FSMContext):
    txt = '09'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='10', state=TimeSlot.start_time)
async def set_start_10(message: types.Message, state: FSMContext):
    txt = '10'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='11', state=TimeSlot.start_time)
async def set_start_11(message: types.Message, state: FSMContext):
    txt = '11'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='12', state=TimeSlot.start_time)
async def set_start_12(message: types.Message, state: FSMContext):
    txt = '12'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='13', state=TimeSlot.start_time)
async def set_start_13(message: types.Message, state: FSMContext):
    txt = '13'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='14', state=TimeSlot.start_time)
async def set_start_14(message: types.Message, state: FSMContext):
    txt = '14'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='15', state=TimeSlot.start_time)
async def set_start_15(message: types.Message, state: FSMContext):
    txt = '15'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='16', state=TimeSlot.start_time)
async def set_start_16(message: types.Message, state: FSMContext):
    txt = '16'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='17', state=TimeSlot.start_time)
async def set_start_17(message: types.Message, state: FSMContext):
    txt = '17'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='18', state=TimeSlot.start_time)
async def set_start_18(message: types.Message, state: FSMContext):
    txt = '18'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='19', state=TimeSlot.start_time)
async def set_start_19(message: types.Message, state: FSMContext):
    txt = '19'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='20', state=TimeSlot.start_time)
async def set_start_20(message: types.Message, state: FSMContext):
    txt = '20'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='21', state=TimeSlot.start_time)
async def set_start_21(message: types.Message, state: FSMContext):
    txt = '21'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='22', state=TimeSlot.start_time)
async def set_start_22(message: types.Message, state: FSMContext):
    txt = '22'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)

@dp.callback_query_handler(text='23', state=TimeSlot.start_time)
async def set_start_23(message: types.Message, state: FSMContext):
    txt = '23'
    await state.update_data(start_time=txt)
    msg_id = (await bot.send_message(message.from_user.id, f"You chose {txt}.")).message_id
    print(msg_id)
    data = await state.get_data()
    week_day = data.get('week_day')
    start_time = data.get('start_time')
    user_time_slot = week_day + start_time

    week = user_time_slot[0]+user_time_slot[1]
    s_time = user_time_slot[2]+user_time_slot[3]
    week_for_message = week_dict.get(week)
    pared_time = f'\U0001F5D3 {week_for_message}, {s_time}:00 - {s_time}:40 \U0001F5D3'

    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Your Time-Slot - {pared_time}")).message_id
            print(msg_id)
            table.update(str(element_id), {'UserTimeSlot': user_time_slot})
            await state.finish()
            await menu(message)



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
