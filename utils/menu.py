from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from user_states import Reg
from aiogram.dispatcher import FSMContext
from airtable_config import table
from keyboards.english_level import user_english_level
from keyboards.menu import menu_button
from keyboards.inline_menu import KB_MENU, G_MENU, START_MENU, NO_EN_LVL, NO_T_SLOT
from config import bot, dp
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
    try:
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                user_name = find_table[index]['fields']['UserName']
                user_surname = find_table[index]['fields']['UserSurname']
                eng_level = find_table[index]['fields']['UserEngLevel']
                time_slot = find_table[index]['fields']['UserTimeSlot']
                is_found = True
        if is_found:
            msg_id = (await bot.send_message(message.from_user.id, 
                f"Hello, {user_name} {user_surname}!\nYour level of English - {eng_level}.\nYour Time-Slot - {time_slot}.", 
                    reply_markup=G_MENU)).message_id
            print(msg_id)
            # await message.delete()
        else:
            msg_id = (await bot.send_message(message.from_user.id, 
                f"1You are not authorized in the service of searching a peer. Want to log in?", 
                    reply_markup=START_MENU)).message_id
            print(msg_id)
            # await bot.delete_message(message.from_user.id, msg_id-1)
            
    except:
        msg_id = (await bot.send_message(message.from_user.id, 
            f"2You are not authorized in the service of searching a peer. Want to log in?", 
                reply_markup=START_MENU)).message_id
        print(msg_id)
        # await bot.delete_message(message.from_user.id, msg_id-1)


async def start_bot(message: types.Message):
    """
    если ник пользователя лежит в базе, то бот поприветствует юзера.
    если же нет, то попросит почту. Если почта есть в БД - пустит дальше.
    Если нет - по факту будет "тупик"
    """
    find_table = table.all()
    is_found = False
    user_name, user_surname, eng_level, time_slot = '', '', '', ''
    try:
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                user_name = find_table[index]['fields']['UserName']
                user_surname = find_table[index]['fields']['UserSurname']
                eng_level = find_table[index]['fields']['UserEngLevel']
                time_slot = find_table[index]['fields']['UserTimeSlot']
                is_found = True
        if is_found:
            msg_id = (await message.answer(f"Hello, {user_name} {user_surname}!\nYour level of English - {eng_level}.\nYour Time-Slot - {time_slot}.", 
                reply_markup=G_MENU)).message_id
            print(msg_id)
            # await message.delete()
        else:
            msg_id = (await bot.send_message(message.from_user.id, 
                f"3You are not authorized in the service of searching a peer. Want to log in?", reply_markup=START_MENU)).message_id
            print(msg_id)
            # await message.delete()

    except:
        msg_id = (await bot.send_message(message.from_user.id, 
            f"4You are not authorized in the service of searching a peer. Want to log in?", reply_markup=START_MENU)).message_id
        print(msg_id)

async def menu(message: types.Message):
    find_table = table.all()
    # is_found = False
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserEngLevel'] == str('None'):
            answer_message = """
                <b>\U000026A1\U000026A1\U000026A1 Main Menu: \U000026A1\U000026A1\U000026A1</b>
                """
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=NO_EN_LVL)).message_id
            print(msg_id)
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserTimeSlot'] == str('None') \
                and find_table[index]['fields']['UserEngLevel'] != str('None'):
            answer_message = """
                <b>\U000026A1\U000026A1\U000026A1 Main Menu: \U000026A1\U000026A1\U000026A1</b>
                """
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=NO_T_SLOT)).message_id
            print(msg_id)
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserTimeSlot'] != str('None') \
                and find_table[index]['fields']['UserEngLevel'] != str('None'):
            answer_message = """
                <b>\U000026A1\U000026A1\U000026A1 Main Menu: \U000026A1\U000026A1\U000026A1</b>
                """
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=KB_MENU)).message_id
            print(msg_id)



@dp.callback_query_handler(text='menu')
async def callback_menu(message: types.Message):
    find_table = table.all()
    # is_found = False
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserEngLevel'] == str('None'):
            answer_message = """
                <b>\U000026A1\U000026A1\U000026A1 Main Menu: \U000026A1\U000026A1\U000026A1</b>
                """
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=NO_EN_LVL)).message_id
            print(str(msg_id) + "MENU")
            # await bot.delete_message(message.from_user.id, msg_id-1)
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserTimeSlot'] == str('None') \
                and find_table[index]['fields']['UserEngLevel'] != str('None'):
            answer_message = """
                <b>\U000026A1\U000026A1\U000026A1 Main Menu: \U000026A1\U000026A1\U000026A1</b>
                """
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=NO_T_SLOT)).message_id
            print(str(msg_id) + "MENU")
            # await bot.delete_message(message.from_user.id, msg_id-1)
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserTimeSlot'] != str('None') \
                and find_table[index]['fields']['UserEngLevel'] != str('None'):
            answer_message = """
                <b>\U000026A1\U000026A1\U000026A1 Main Menu: \U000026A1\U000026A1\U000026A1</b>
                """
            msg_id = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=KB_MENU)).message_id
            print(str(msg_id) + "MENU")
            # await bot.delete_message(message.from_user.id, msg_id-1)


async def statistics(message: types.Message):
    await message.answer("""
    -уровень английского с 01.01.2022 - <b>B1</b>\n
    -количество встреч в роли HR - 2\n
    -количество встреч в роли кандидата - 3\n
    -количество часов в каждой роли:\n
    в роли HR - 2 часа\n
    в роли кандидата - 1 час\n
    """, parse_mode='HTML')


async def english_level(message: types.Message):
    msg_id = (await message.answer(text='Please select your English level', reply_markup=user_english_level)).message_id
    print(msg_id)
    # await bot.delete_message(message.from_user.id, msg_id-1)
    # await message.delete()
    await Reg.user_eng_level.set()

@dp.callback_query_handler(text='eng_level')
async def eng_level(message: types.Message):
    msg_id = (await bot.send_message(message.from_user.id, 
        'Please select your English level', reply_markup=user_english_level)).message_id
    print(msg_id)
    # await bot.delete_message(message.from_user.id, msg_id-1)
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
        msg_id = (await message.answer(f"Your level of English - {message.text}\n", reply_markup=G_MENU)).message_id
        print(msg_id)
        user_level = str(message.text)
        table.update(record_id=str(element_id), fields={'UserEngLevel': user_level})
        await state.finish()
    else:
        msg_id = (await bot.send_message(message.from_user.id, 
            text='You enter something wrong. \nThe correct format is entered from the keyboard.')).message_id
        print(msg_id)



def register_handlers_menu(dp: Dispatcher):
    dp.register_message_handler(start_bot, Command('start'))
    dp.register_message_handler(menu, commands='menu')
    dp.register_message_handler(statistics, commands='statistics')
    dp.register_message_handler(english_level, commands='eng_level')
    dp.register_message_handler(set_eng_level, state=Reg.user_eng_level)

