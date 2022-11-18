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


@dp.message_handler(Command('menu'))
async def menu(message: types.Message):
    await message.answer('Добро пожаловать в меню!')


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
            [
                KeyboardButton(text=f"Отменить регистрацию")
            ]

        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(f"Для начала регистрации введите Ваше имя: ", reply_markup=user_name)
    await Reg.user_name.set()


@dp.message_handler(state=Reg.user_name)
async def get_user_name(message: types.Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    user_surname = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f"Отмена регистрации")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(f"<b>{message.text}</b>, теперь введите Вашу фамилию: ", reply_markup=user_surname,
                         parse_mode='HTML')
    await Reg.user_surname.set()


@dp.message_handler(state=Reg.user_surname)
async def get_email(message: types.Message, state: FSMContext):
    await state.update_data(user_surname=message.text)
    user_email = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f"Отмена регистрации")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(f"Теперь введите Вашу электронную почту: ", parse_mode='HTML', reply_markup=user_email)
    await Reg.user_email.set()


@dp.message_handler(state=Reg.user_email)
async def set_user_email(message: types.Message, state=FSMContext):
    await state.update_data(user_email=message.text)
    pattern = r'^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$'
    if re.fullmatch(pattern, message.text):
        await state.update_data(user_email=message.text)
        data = await state.get_data()
        user_name = data.get('user_name')
        user_surname = data.get('user_surname')
        user_email = data.get('user_email')
        table.create(fields={'UserName': user_name, 'UserSurname': user_surname, 'UserEmail': user_email,
                             'UserIDTG': str(message.from_user.id)})
        await message.answer("Регистрация успешно завершена!\n Для прохождения в меню нажмите /menu.")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
