from config import bot, dp
from aiogram import executor, types
from airtable_config import table, find_table
from keyboards import ikb, ikb_register
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from registration import Reg
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import re


async def on_startup(_):
    print('The bot is online!')


@dp.message_handler(commands='menu')
async def menu(message: types.Message):
    await message.answer("""
    Добро пожаловать в меню!\n
    1. Задать уровень английского /eng_level\n
    2. Задать таймслот /timeslot\n
    3. Показать статистику /statistics\n
    """)


@dp.message_handler(Command('start'))
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


@dp.message_handler(Command('register'))
async def bot_register(message: types.Message):
    user_name = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f"{message.from_user.first_name}")
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(f"Для начала регистрации введите Ваше имя: ", reply_markup=user_name)
    await Reg.user_name.set()


@dp.message_handler(state=Reg.user_name)
async def get_user_name(message: types.Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await message.answer(f"<b>{message.text}</b>, теперь введите Вашу фамилию: ",
                         parse_mode='HTML')
    await Reg.user_surname.set()


@dp.message_handler(state=Reg.user_surname)
async def get_email(message: types.Message, state: FSMContext):
    await state.update_data(user_surname=message.text)
    await message.answer(f"Теперь введите Вашу электронную почту: ", parse_mode='HTML')
    await Reg.user_email.set()


@dp.message_handler(state=Reg.user_email)
async def set_user_email(message: types.Message, state=FSMContext):
    await state.update_data(user_email=message.text)
    data = await state.get_data()
    user_name = data.get('user_name')
    user_surname = data.get('user_surname')
    user_email = data.get('user_email')
    table.create(fields={'UserName': user_name, 'UserSurname': user_surname, 'UserEmail': user_email,
                         'UserIDTG': str(message.from_user.id)})
    await message.answer("Регистрация успешно завершена!\n Для прохождения в меню нажмите /menu.")


@dp.message_handler(commands=['statistics'])
async def statistics(message: types.Message):
    await message.answer("""
    -уровень английского с 01.01.2022 - <b>B1</b>\n
    -количество встреч в роли HR - 2\n
    -количество встреч в роли кандидата - 3\n
    -количество часов в каждой роли:\n
    в роли HR - 2 часа\n
    в роли кандидата - 1 час\n
    """, parse_mode='HTML')


@dp.message_handler(commands=['eng_level'])
async def english_level(message: types.Message):
    await message.answer('Выберите ваш уровень английского: ')
    user_english_level = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="A1")
            ],
            [
                KeyboardButton(text="A2")
            ],
            [
                KeyboardButton(text="B1")
            ],
            [
                KeyboardButton(text="B2")
            ],
            [
                KeyboardButton(text="C1")
            ],
            [
                KeyboardButton(text="C2")
            ],

        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(text='Укажите Ваш уровень английского', reply_markup=user_english_level)
    await Reg.user_eng_level.set()


@dp.message_handler(state=Reg.user_eng_level)
async def set_eng_level(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(user_eng_level=answer)
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
    table.update(record_id=element_id, fields={'UserEngLevel': message.text})
    await message.answer(f"Ваш уровень англйиского - {answer}\n"
                         f"Для прохождения в меню нажмите /menu")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
