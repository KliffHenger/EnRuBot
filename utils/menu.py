from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from user_states import Reg
from aiogram.dispatcher import FSMContext
from airtable_config import table
from keyboards.english_level import user_english_level
from keyboards.menu import menu_button
from keyboards.inline_menu import KB_MENU, G_MENU, START_MENU, NO_EN_LVL, NO_T_SLOT
from config import bot, dp



last_msg = 0


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
            await bot.send_message(message.from_user.id, 
                f"Hello, {user_name} {user_surname}!\nYour level of English - {eng_level}.\nYour Time-Slot - {time_slot}", reply_markup=G_MENU) # инлайн-кнопка приводящая в Главное Меню
        else:
            last_msg = (await bot.send_message(message.from_user.id, 
                f"You are not authorized in the service of searching for interlocutors. Want to log in?", reply_markup=START_MENU)).message_id
            await bot.delete_message(message.from_user.id, message_id=last_msg-1)
            print(last_msg)
            
    except:
        last_msg = (await bot.send_message(message.from_user.id, 
            f"You are not authorized in the service of searching for interlocutors. Want to log in?", reply_markup=START_MENU)).message_id
        await bot.delete_message(message.from_user.id, message_id=last_msg-1)
        print(last_msg)


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
            await message.answer(
                f"Hello, {user_name} {user_surname}!\nYour level of English - {eng_level}.\nYour Time-Slot - {time_slot}", reply_markup=G_MENU) # инлайн-кнопка приводящая в Главное Меню
        else:
            last_msg = (await bot.send_message(message.from_user.id, 
                f"You are not authorized in the service of searching for interlocutors. Want to log in?", reply_markup=START_MENU)).message_id
            await bot.delete_message(message.from_user.id, message_id=last_msg-1)
            print(last_msg)
            
    except:
        last_msg = (await bot.send_message(message.from_user.id, 
            f"You are not authorized in the service of searching for interlocutors. Want to log in?", reply_markup=START_MENU)).message_id
        await bot.delete_message(message.from_user.id, message_id=last_msg-1)
        print(last_msg)


async def menu(message: types.Message):
    find_table = table.all()
    # is_found = False
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserEngLevel'] == str('None'):
            answer_message = """
                <b>MAIN MENU:</b>
                """
            last_msg = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=NO_EN_LVL)).message_id
            await bot.delete_message(message.from_user.id, message_id=last_msg-1)
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserTimeSlot'] == str('None') \
                and find_table[index]['fields']['UserEngLevel'] != str('None'):
            answer_message = """
                <b>MAIN MENU:</b>
                """
            last_msg = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=NO_T_SLOT)).message_id
            await bot.delete_message(message.from_user.id, message_id=last_msg-1)
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserTimeSlot'] != str('None') \
                and find_table[index]['fields']['UserEngLevel'] != str('None'):
            answer_message = """
                <b>MAIN MENU:</b>
                """
            last_msg = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=KB_MENU)).message_id
            await bot.delete_message(message.from_user.id, message_id=last_msg-1)



@dp.callback_query_handler(text='menu')
async def callback_menu(message: types.Message):
    find_table = table.all()
    # is_found = False
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserEngLevel'] == str('None'):
            answer_message = """
                <b>MAIN MENU:</b>
                """
            last_msg = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=NO_EN_LVL)).message_id
            await bot.delete_message(message.from_user.id, message_id=last_msg-1)
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserTimeSlot'] == str('None') \
                and find_table[index]['fields']['UserEngLevel'] != str('None'):
            answer_message = """
                <b>MAIN MENU:</b>
                """
            last_msg = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=NO_T_SLOT)).message_id
            await bot.delete_message(message.from_user.id, message_id=last_msg-1)
        elif find_table[index]['fields']['UserIDTG'] == str(message.from_user.id) \
            and find_table[index]['fields']['UserTimeSlot'] != str('None') \
                and find_table[index]['fields']['UserEngLevel'] != str('None'):
            answer_message = """
                <b>MAIN MENU:</b>
                """
            last_msg = (await bot.send_message(message.from_user.id, text=answer_message, parse_mode='HTML', reply_markup=KB_MENU)).message_id


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
    last_msg = (await message.answer(text='Indicate your level of English', reply_markup=user_english_level)).message_id
    await bot.delete_message(message.from_user.id, message_id=last_msg-1)
    await Reg.user_eng_level.set()

@dp.callback_query_handler(text='eng_level')
async def eng_level(message: types.Message):
    last_msg = (await bot.send_message(message.from_user.id, 'Indicate your level of English', reply_markup=user_english_level)).message_id
    await bot.delete_message(message.from_user.id, message_id=last_msg-1)
    await Reg.user_eng_level.set()


async def set_eng_level(message: types.Message, state: FSMContext):
    """
    Дла начала нам нужно найти record_id нашего пользователя. Далее
    мы обновляем его параметр уровня владения языка в базе
    """
    answer = message.text
    await state.update_data(user_eng_level=answer)
    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
    last_msg = (await message.answer(f"Your level of English - {answer}\n", reply_markup=menu_button)).message_id
    await bot.delete_message(message.from_user.id, message_id=last_msg-1)
    await bot.delete_message(message.from_user.id, message_id=last_msg-2)
    user_level = str(answer)
    table.update(record_id=str(element_id), fields={'UserEngLevel': user_level})
    await state.finish()
    await menu(message)


def register_handlers_menu(dp: Dispatcher):
    dp.register_message_handler(start_bot, Command('start'))
    dp.register_message_handler(menu, commands='menu')
    dp.register_message_handler(statistics, commands='statistics')
    dp.register_message_handler(english_level, commands='eng_level')
    dp.register_message_handler(set_eng_level, state=Reg.user_eng_level)

