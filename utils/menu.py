from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from user_states import Reg 
from aiogram.dispatcher import FSMContext
from airtable_config import table, at
from airtable_config import find_table
from keyboards.english_level import user_english_level
from keyboards.menu import menu_button

# TODO: It is necessary to fix setting english level
#       (set_eng_level function)
#       I don't know what to do exactly. I have 422 error during trying to update a record


async def start_bot(message: types.Message):
    is_found = False
    user_name, user_surname = '', ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            user_name = find_table[index]['fields']['UserName']
            user_surname = find_table[index]['fields']['UserSurname']
            is_found = True
    if is_found:
        await message.answer(f"Здравствуйте, {user_name} {user_surname}!\n Для прохождения в меню нажмите /menu")
    else:
        await message.answer(f"Для прохождения регистрации нажмите /register")


async def menu(message: types.Message):
    await message.answer("""
    Добро пожаловать в меню!\n
    1. Задать уровень английского /eng_level\n
    2. Задать таймслот /timeslot\n
    3. Показать статистику /statistics\n
    """)


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
    await message.answer(text='Укажите Ваш уровень английского', reply_markup=user_english_level)
    await Reg.user_eng_level.set()


async def set_eng_level(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(user_eng_level=answer)
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
    await message.answer(f"Ваш уровень английского - {answer}\n", reply_markup=menu_button)
    # 422 user error. After restarting of the project
    # I don't have any troubles with setting english level
    table.update(record_id=str(element_id), fields={'UserEngLevel': str(message.text)})
    await state.finish()
    await menu(message)


# async def define_timeslot(message: types.Message):
#     await message.answer(
#         text='Задайте, пожалуйста, тайм-слот на следующей неделе с 21 по 27 ноября 2022 в формате MO1718, где MO - Monday, 17 (17:00) время начала тайм-слота, 18 (18:00) - время окончания тайм-слота"')


def register_handlers_menu(dp: Dispatcher):
    dp.register_message_handler(start_bot, Command('start'))
    dp.register_message_handler(menu, commands='menu')
    dp.register_message_handler(statistics, commands='statistics')
    dp.register_message_handler(english_level, commands='eng_level')
    dp.register_message_handler(set_eng_level, state=Reg.user_eng_level)
    # dp.register_message_handler(define_timeslot, commands='timeslot')
