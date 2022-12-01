from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from user_states import Reg
from aiogram.dispatcher import FSMContext
from airtable_config import table
from keyboards.english_level import user_english_level
from keyboards.menu import menu_button
from keyboards.inline_menu import KB_MENU, G_MENU
from config import bot, dp



isCall = False


async def start_bot(message: types.Message):
    """
    если ник пользователя лежит в базе, то бот поприветствует юзера.
    если же нет, то попросит почту. Если почта есть в БД - пустит дальше.
    Если нет - по факту будет "тупик"
    """
    find_table = table.all()
    is_found = False
    user_name, user_surname = '', ''
    try:
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                user_name = find_table[index]['fields']['UserName']
                user_surname = find_table[index]['fields']['UserSurname']
                is_found = True
        if is_found:
            await message.answer(
                f"Здравствуйте, {user_name} {user_surname}!", reply_markup=G_MENU) # инлайн-кнопка приводящая в Главное Меню
        else:
            await message.answer(f"Для прохождения идентификации с базой учеников нажмите /register")
    except:
        await message.answer(f"Для прохождения идентификации с базой учеников нажмите /register")


async def menu(message: types.Message):
    answer_message = """
    ГЛАВНОЕ МЕНЮ:\n
    1. Вы можете задать уровень знания английского.\n
    2. Задать таймслот.\n
    3. Посмотреть статистику.\n
    4. Найти собеседника.\n
    """
    await bot.send_message(message.chat.id, text=answer_message, reply_markup=KB_MENU) # инлайн-кнопка выводящая пункты Главного Меню

@dp.callback_query_handler(text='menu')
async def callback_menu(message: types.Message):
    answer_message = """
    ГЛАВНОЕ МЕНЮ:\n
    1. Вы можете задать уровень знания английского.\n
    2. Задать таймслот.\n
    3. Посмотреть статистику.\n
    4. Найти собеседника.\n
    """
    await bot.send_message(message.from_user.id, text=answer_message, reply_markup=KB_MENU) # инлайн-кнопка выводящая пункты Главного Меню


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

@dp.callback_query_handler(text='eng_level')
async def eng_level(message: types.Message):
    await bot.send_message(message.from_user.id, 'Укажите Ваш уровень английского', reply_markup=user_english_level)
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
    await message.answer(f"Ваш уровень английского - {answer}\n", reply_markup=menu_button)
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

