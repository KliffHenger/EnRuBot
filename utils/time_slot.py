from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from user_states import TimeSlot
from aiogram.dispatcher import FSMContext
from test_bot import menu
from airtable_config import table
from utils.menu import menu
import re


async def time_slot_input(message: types.Message):
    await message.answer(f"Выберите ближайший подходящий день недели.")

    await TimeSlot.week_day.set()


# async def get_user_name(message: types.Message, state: FSMContext):
#     await state.update_data(user_name=message.text)
#     await message.answer(f"<b>{message.text}</b>, теперь введите Вашу фамилию: ",
#                          parse_mode='HTML')
#     await Reg.user_surname.set()


# async def get_email(message: types.Message, state: FSMContext):
#     await state.update_data(user_surname=message.text)
#     await message.answer(f"Теперь введите Вашу электронную почту: ", parse_mode='HTML')
#     await Reg.user_email.set()


# async def set_user_email(message: types.Message, state=FSMContext):
#     pattern = r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$'
#     if re.fullmatch(pattern, message.text):
#         await state.update_data(user_email=message.text)
#         data = await state.get_data()
#         user_name = data.get('user_name')
#         user_surname = data.get('user_surname')
#         user_email = data.get('user_email')
#         table.create(fields={'UserName': user_name, 'UserSurname': user_surname, 'UserEmail': user_email,
#                              'UserIDTG': str(message.from_user.id)})
#         await message.answer("Регистрация успешно завершена!\n")
#         await state.finish()
#         await menu(message)
#     else:
#         await message.answer(text='Введите корректное значение электронной почты.')


# def register_handlers_registration(dp: Dispatcher):
#     dp.register_message_handler(bot_register, Command('register'))
#     dp.register_message_handler(get_user_name, state=Reg.user_name)
#     dp.register_message_handler(get_email, state=Reg.user_surname)
#     dp.register_message_handler(set_user_email, state=Reg.user_email)
