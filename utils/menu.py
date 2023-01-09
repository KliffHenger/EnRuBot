from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from user_states import Reg
from aiogram.dispatcher import FSMContext
from airtable_config import table
from keyboards.english_level import user_english_level
from keyboards.menu import menu_button
from keyboards.inline_menu import KB_MENU, G_MENU, START_MENU, NO_EN_LVL, NO_T_SLOT, PARED_MENU
from config import bot, dp, week_dict
import re



@dp.callback_query_handler(text='start')
async def start_bot(message: types.Message):
    """
    если ник пользователя лежит в базе, то бот поприветствует юзера.
    если же нет, то попросит почту. Если почта есть в БД - пустит дальше.
    Если нет - по факту будет "тупик"
    """
    find_table = table.all()
    is_found = False
    user_name, user_surname, eng_level, time_slot = '', '', '', ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            user_name = find_table[index]['fields']['UserName']
            user_surname = find_table[index]['fields']['UserSurname']
            eng_level = find_table[index]['fields']['UserEngLevel']
            time_slot = find_table[index]['fields']['UserTimeSlot']
            is_found = True
    if is_found:
        msg_id = (await bot.send_message(message.from_user.id, 
            text=f"Hello, {user_name} {user_surname}!\nYou have a {eng_level} English level.\nYour Time-Slot - {time_slot}." 
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


async def start_bot(message: types.Message):
    """
    если ник пользователя лежит в базе, то бот поприветствует юзера.
    если же нет, то попросит почту. Если почта есть в БД - пустит дальше.
    Если нет - по факту будет "тупик"
    """
    find_table = table.all()
    is_found = False
    user_name, user_surname, eng_level, time_slot = '', '', '', ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            user_name = find_table[index]['fields']['UserName']
            user_surname = find_table[index]['fields']['UserSurname']
            eng_level = find_table[index]['fields']['UserEngLevel']
            time_slot = find_table[index]['fields']['UserTimeSlot']
            is_found = True
    if is_found:
        msg_id = (await message.answer(f"Hello, {user_name} {user_surname}!\nYou have a - {eng_level} English level.\nYour Time-Slot - {time_slot}."
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
        f_tg_id = message.from_user.id
        if find_table[index]['fields']['UserIDTG'] == str(f_tg_id) \
            and find_table[index]['fields']['IsPared'] == 'True':
            f_timeSlot = find_table[index]['fields']['UserTimeSlot']
            week = f_timeSlot[0]+f_timeSlot[1]
            start_time = f_timeSlot[2]+f_timeSlot[3]
            week_for_message = week_dict.get(week)
            pared_time = f'{week_for_message}, {start_time}-00'
            record_id = find_table[index]['id']
            answer_message = f"\U000026A1 \U000026A1 \U000026A1 Main Menu: \U000026A1 \U000026A1 \U000026A1 \n\
Функции:\n\
\U0001F6AB \U0001F4DA Change the level of English\n\
\U0001F6AB \U0001F551 Change Time-Slot\n\
\U0001F6AB\U0001F6ABЗАБЛОКИРОВАНЫ\U0001F6AB\U0001F6AB\n\
до того момента пока не состоится встреча в {pared_time}."
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=PARED_MENU)).message_id
            print(str(msg_id) + "MENU inline pared_true")
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserEngLevel'] == str('None'):
            record_id = find_table[index]['id']
            answer_message = """
                    <b>\U000026A1\U000026A1\U000026A1 Main Menu: \U000026A1\U000026A1\U000026A1</b>
                """
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=NO_EN_LVL)).message_id
            print(str(msg_id) + "MENU inline")
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserTimeSlot'] == str('None') \
                and find_table[index]['fields']['UserEngLevel'] != str('None'):
            record_id = find_table[index]['id']  # для записи msg_id удаляемого сообщения
            answer_message = """
                    <b>\U000026A1\U000026A1\U000026A1 Main Menu: \U000026A1\U000026A1\U000026A1</b>
                """
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=NO_T_SLOT)).message_id
            print(str(msg_id) + "MENU inline")
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserTimeSlot'] != str('None') \
                and find_table[index]['fields']['UserEngLevel'] != str('None'):
            record_id = find_table[index]['id']
            answer_message = """
                    <b>\U000026A1\U000026A1\U000026A1 Main Menu: \U000026A1\U000026A1\U000026A1</b>
                """
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=KB_MENU)).message_id
            print(str(msg_id) + "MENU inline")
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})


@dp.callback_query_handler(text='menu')
async def callback_menu(message: types.Message):
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['IsPared'] == 'True':
            f_timeSlot = find_table[index]['fields']['UserTimeSlot']
            week = f_timeSlot[0]+f_timeSlot[1]
            start_time = f_timeSlot[2]+f_timeSlot[3]
            week_for_message = week_dict.get(week)
            pared_time = f'{week_for_message}, {start_time}-00'
            record_id = find_table[index]['id']
            msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            answer_message = f"\U000026A1 \U000026A1 \U000026A1 Main Menu: \U000026A1 \U000026A1 \U000026A1 \n\
The following functions are disabled before the meeting at: {pared_time}.\n\
\U0001F6AB \U0001F4DA Select my English Level \U0001F6AB\n\
\U0001F6AB \U0001F551 Change the time slot \U0001F6AB"
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=PARED_MENU)).message_id
            print(str(msg_id) + "MENU inline pared_true")
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserEngLevel'] == str('None'):
            record_id = find_table[index]['id']
            answer_message = """
                    <b>\U000026A1\U000026A1\U000026A1 Main Menu: \U000026A1\U000026A1\U000026A1</b>
                """
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=NO_EN_LVL)).message_id
            print(str(msg_id) + "MENU inline")
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserTimeSlot'] == str('None') \
                and find_table[index]['fields']['UserEngLevel'] != str('None'):
            record_id = find_table[index]['id']
            answer_message = """
                    <b>\U000026A1\U000026A1\U000026A1 Main Menu: \U000026A1\U000026A1\U000026A1</b>
                """
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=NO_T_SLOT)).message_id
            print(str(msg_id) + "MENU inline")
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserTimeSlot'] != str('None') \
                and find_table[index]['fields']['UserEngLevel'] != str('None'):
            record_id = find_table[index]['id']
            msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            answer_message = """
                    <b>\U000026A1\U000026A1\U000026A1 Main Menu: \U000026A1\U000026A1\U000026A1</b>
                """
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=KB_MENU)).message_id
            print(str(msg_id) + "MENU inline")
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})



async def english_level(message: types.Message):
    msg_id = (await message.answer(text='Please select your English level', reply_markup=user_english_level)).message_id
    print(msg_id)
    # await bot.delete_message(message.from_user.id, msg_id-1)
    # await message.delete()
    await Reg.user_eng_level.set()

@dp.callback_query_handler(text='eng_level')
async def eng_level(message: types.Message):
    all_table = table.all()
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            record_id = all_table[index]['id']  # достает record_id из БД
            msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            msg_id = (await bot.send_message(message.from_user.id, 
                'Please select your English level', reply_markup=user_english_level)).message_id
            print(msg_id)
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
            await Reg.user_eng_level.set()


async def set_eng_level(message: types.Message, state: FSMContext):
    """
    Дла начала нам нужно найти record_id нашего пользователя. Далее
    мы обновляем его параметр уровня владения языка в базе
    """
    pattern = r'A0|A0-A1|A1|A1-A2|A2|A2-B1|B1|B1-B2|B2|B2-C1|C1|C1-C2|C2'
    if re.fullmatch(pattern, message.text):
        await state.update_data(user_eng_level=message.text)
        find_table = table.all()
        element_id = ''
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                element_id = find_table[index]['id']
                msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                msg_id = (await message.answer(f"You have a {message.text} English level.")).message_id
                print(msg_id)
                user_level = str(message.text)
                table.update(record_id=str(element_id), fields={"msgIDforDEL": str(msg_id)})
                table.update(record_id=str(element_id), fields={'UserEngLevel': user_level})
                await state.finish()
                await menu(message)
    else:
        find_table = table.all()
        element_id = ''
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                element_id = find_table[index]['id']
                msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                msg_id = (await bot.send_message(message.from_user.id, 
                    text='Something has been entered incorrectly.\nPlease use the keypad to enter the valid format.', 
                    reply_markup=user_english_level)).message_id
                print(msg_id)
                table.update(record_id=str(element_id), fields={"msgIDforDEL": str(msg_id)})



def register_handlers_menu(dp: Dispatcher):
    dp.register_message_handler(start_bot, Command('start'))
    dp.register_message_handler(menu, commands='menu')
    dp.register_message_handler(english_level, commands='eng_level')
    dp.register_message_handler(set_eng_level, state=Reg.user_eng_level)

