from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from airtable_config import table
from keyboards.inline_menu import KB_MENU, G_MENU, START_MENU, NO_EN_LVL, NO_T_SLOT, PARED_MENU
from config import bot, dp, week_dict




@dp.callback_query_handler(text='start')
async def start_bot(message: types.Message):
    """
    если ник пользователя лежит в базе, то бот поприветствует юзера.
    если же нет, то попросит почту. Если почта есть в БД - пустит дальше.
    Если нет - сообщит про это.
    """
    find_table = table.all()
    is_found = False
    user_name, user_surname, eng_level, time_slot = '', '', '', ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            user_name = find_table[index]['fields']['UserName']
            user_surname = find_table[index]['fields']['UserSurname']
            # eng_level = find_table[index]['fields']['UserEngLevel']
            # time_slot = find_table[index]['fields']['UserTimeSlot']
            is_found = True
    if is_found:
        msg_id = (await bot.send_message(message.from_user.id, 
            text=f"Hello, {user_name} {user_surname}!" 
                )).message_id
        print(msg_id)
        await menu(message)
        # await message.delete()
    else:
        msg_id = (await bot.send_message(message.from_user.id, 
            text=f"Sorry, you are not authorized to join yet. Would you like to sign in?", 
                reply_markup=START_MENU)).message_id
        print(msg_id)
        await bot.delete_message(message.from_user.id, msg_id-1)


async def start_bot(message: types.Message, state: FSMContext):
    """
    если ник пользователя лежит в базе, то бот поприветствует юзера.
    если же нет, то попросит почту. Если почта есть в БД - пустит дальше.
    Если нет - по факту будет "тупик"
    """
    await state.finish()
    find_table = table.all()
    is_found = False
    user_name, user_surname, eng_level, time_slot = '', '', '', ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            user_name = find_table[index]['fields']['UserName']
            user_surname = find_table[index]['fields']['UserSurname']
            # eng_level = find_table[index]['fields']['UserEngLevel']
            # time_slot = find_table[index]['fields']['UserTimeSlot']
            is_found = True
    if is_found:
        msg_id = (await message.answer(f"Hello, {user_name} {user_surname}!"
            )).message_id
        print(msg_id)
        await menu(message)
        # await message.delete()
    else:
        msg_id = (await bot.send_message(message.from_user.id, 
            f"Sorry, you are not authorized to join yet. Would you like to sign in?", reply_markup=START_MENU)).message_id
        print(msg_id)
        await message.delete()


async def menu(message: types.Message):
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['IsPared'] == 'True':
            eng_level = find_table[index]['fields']['UserEngLevel']
            time_slot = find_table[index]['fields']['UserTimeSlot']

            week = time_slot[0]+time_slot[1]
            start_time = time_slot[2]+time_slot[3]
            week_for_message = week_dict.get(week)
            pared_time = f'{week_for_message}, {start_time}:00'
            record_id = find_table[index]['id']  # достает record_id из БД
            try:
                msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            except:
                pass
            try:
                await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            except:
                pass
            answer_message = f"You have a - {eng_level} English level.\nYour Time-Slot - {pared_time}.\n\n\
\U000026A1 \U000026A1 \U000026A1 Main Menu: \U000026A1 \U000026A1 \U000026A1 \n\
The following functions are disabled before the meeting at: {pared_time}.\n\
\U0001F6AB \U0001F4DA Select my English Level \U0001F6AB\n\
\U0001F6AB \U0001F551 Change the time slot \U0001F6AB"
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=PARED_MENU)).message_id
            print(str(msg_id) + "MENU pared_true")
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserEngLevel'] == str('None'):
            eng_level = find_table[index]['fields']['UserEngLevel']
            time_slot = find_table[index]['fields']['UserTimeSlot']

            week = time_slot[0]+time_slot[1]
            start_time = time_slot[2]+time_slot[3]
            week_for_message = week_dict.get(week)
            pared_time = f'{week_for_message}, {start_time}:00'

            record_id = find_table[index]['id']  # достает record_id из БД
            answer_message = f"You have a - {eng_level} English level.\nYour Time-Slot - {pared_time}.\n\n\
\U000026A1\U000026A1\U000026A1 Main Menu: \U000026A1\U000026A1\U000026A1"
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=NO_EN_LVL)).message_id
            print(str(msg_id) + "MENU")
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserTimeSlot'] == str('None') \
                and find_table[index]['fields']['UserEngLevel'] != str('None'):
            eng_level = find_table[index]['fields']['UserEngLevel']
            time_slot = find_table[index]['fields']['UserTimeSlot']

            week = time_slot[0]+time_slot[1]
            start_time = time_slot[2]+time_slot[3]
            week_for_message = week_dict.get(week)
            pared_time = f'{week_for_message}, {start_time}:00'

            record_id = find_table[index]['id']  # достает record_id из БД
            answer_message = f"You have a - {eng_level} English level.\nYour Time-Slot - {pared_time}.\n\n\
\U000026A1\U000026A1\U000026A1 Main Menu: \U000026A1\U000026A1\U000026A1"
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=NO_T_SLOT)).message_id
            print(str(msg_id) + "MENU")
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserTimeSlot'] != str('None') \
                and find_table[index]['fields']['UserEngLevel'] != str('None'):
            eng_level = find_table[index]['fields']['UserEngLevel']
            time_slot = find_table[index]['fields']['UserTimeSlot']

            week = time_slot[0]+time_slot[1]
            start_time = time_slot[2]+time_slot[3]
            week_for_message = week_dict.get(week)
            pared_time = f'{week_for_message}, {start_time}:00'

            record_id = find_table[index]['id']  # достает record_id из БД
            try:
                msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            except:
                pass
            try:
                await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            except:
                pass
            answer_message = f"You have a - {eng_level} English level.\nYour Time-Slot - {pared_time}.\n\n\
\U000026A1\U000026A1\U000026A1 Main Menu: \U000026A1\U000026A1\U000026A1"
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=KB_MENU)).message_id
            print(str(msg_id) + "MENU")
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД


@dp.callback_query_handler(text='menu')
async def callback_menu(message: types.Message):
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['IsPared'] == 'True':
            eng_level = find_table[index]['fields']['UserEngLevel']
            time_slot = find_table[index]['fields']['UserTimeSlot']

            week = time_slot[0]+time_slot[1]
            start_time = time_slot[2]+time_slot[3]
            week_for_message = week_dict.get(week)
            pared_time = f'{week_for_message}, {start_time}:00'

            record_id = find_table[index]['id']  # достает record_id из БД
            try:
                msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            except:
                pass
            try:
                await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            except:
                pass
            answer_message = f"You have a - {eng_level} English level.\nYour Time-Slot - {pared_time}.\n\n\
\U000026A1 \U000026A1 \U000026A1 Main Menu: \U000026A1 \U000026A1 \U000026A1 \n\
The following functions are disabled before the meeting at: {pared_time}.\n\
\U0001F6AB \U0001F4DA Select my English Level \U0001F6AB\n\
\U0001F6AB \U0001F551 Change the time slot \U0001F6AB"
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=PARED_MENU)).message_id
            print(str(msg_id) + "MENU inline pared_true")
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserEngLevel'] == str('None'):
            eng_level = find_table[index]['fields']['UserEngLevel']
            time_slot = find_table[index]['fields']['UserTimeSlot']

            week = time_slot[0]+time_slot[1]
            start_time = time_slot[2]+time_slot[3]
            week_for_message = week_dict.get(week)
            pared_time = f'{week_for_message}, {start_time}:00'

            record_id = find_table[index]['id']  # достает record_id из БД
            answer_message = f"You have a - {eng_level} English level.\nYour Time-Slot - {pared_time}.\n\n\
\U000026A1\U000026A1\U000026A1 Main Menu: \U000026A1\U000026A1\U000026A1"
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=NO_EN_LVL)).message_id
            print(str(msg_id) + "MENU inline")
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserTimeSlot'] == str('None') \
                and find_table[index]['fields']['UserEngLevel'] != str('None'):
            eng_level = find_table[index]['fields']['UserEngLevel']
            time_slot = find_table[index]['fields']['UserTimeSlot']

            week = time_slot[0]+time_slot[1]
            start_time = time_slot[2]+time_slot[3]
            week_for_message = week_dict.get(week)
            pared_time = f'{week_for_message}, {start_time}:00'

            record_id = find_table[index]['id']  # достает record_id из БД
            answer_message = f"You have a - {eng_level} English level.\nYour Time-Slot - {pared_time}.\n\n\
\U000026A1\U000026A1\U000026A1 Main Menu: \U000026A1\U000026A1\U000026A1"
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=NO_T_SLOT)).message_id
            print(str(msg_id) + "MENU inline")
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserTimeSlot'] != str('None') \
                and find_table[index]['fields']['UserEngLevel'] != str('None'):
            eng_level = find_table[index]['fields']['UserEngLevel']
            time_slot = find_table[index]['fields']['UserTimeSlot']

            week = time_slot[0]+time_slot[1]
            start_time = time_slot[2]+time_slot[3]
            week_for_message = week_dict.get(week)
            pared_time = f'{week_for_message}, {start_time}:00'

            record_id = find_table[index]['id']  # достает record_id из БД
            try:
                msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            except:
                pass
            try:
                await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            except:
                pass
            answer_message = f"You have a - {eng_level} English level.\nYour Time-Slot - {pared_time}.\n\n\
\U000026A1\U000026A1\U000026A1 Main Menu: \U000026A1\U000026A1\U000026A1"
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=KB_MENU)).message_id
            print(str(msg_id) + "MENU inline")
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД




def register_handlers_menu(dp: Dispatcher):
    dp.register_message_handler(start_bot, Command('start'))
    dp.register_message_handler(menu, commands='menu')
    # dp.register_message_handler(english_level, commands='eng_level')
    # dp.register_message_handler(set_eng_level, state=Reg.user_eng_level)

