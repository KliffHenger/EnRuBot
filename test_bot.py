from config import bot, dp
from aiogram import executor, types
from airtable_config import table
from keyboards import ikb, ikb_register
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from registration import Reg
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def on_startup(_):
    print('The bot is online!')


@dp.message_handler(commands='start')
async def start_bot(message: types.Message):
    user_id_tg = ''
    for index in range(len(table)):
        if table[index]['fields']['UserIDTG'] == message.from_user.id:
            user_id_tg = table[index]['fields']['UserIDTG']
            await message.answer(
                f"Здравствуйте, {table[index]['fields']['UserName']} {table[index]['fields']['UserSurname']}")
        else:
            continue
    if not user_id_tg:
        await message.answer('Здравствуйте! Пройдем регистрацию в боте!', reply_markup=ikb_register)


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
                KeyboardButton(text=f"{message.from_user.last_name}")
            ],
            [
                KeyboardButton(text=f"Отмена регистрации")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(f"<b>{message.text}</b>, теперь введите Вашу фамилию: ", reply_markup=user_surname)
    Reg.user_surname.set()


@dp.message_handler(state=Reg.user_surname)
async def get_email(message: types.Message, state: FSMContext):
    await state.update_data(user_surname=message.text)
    user_email = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f"{message.text}")
            ],
            [
                KeyboardButton(text=f"Отмена регистрации")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(f"<b>{message.text}</b>, теперь введите Вашу фамилию: ", parse_mode='HTML')
    Reg.user_surname.set()





if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
