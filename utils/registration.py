from aiogram import types, Dispatcher
from user_states import Reg
from aiogram.dispatcher import FSMContext
from airtable_config import table
from utils.menu import menu
import re


async def bot_register(message: types.Message):
    await message.answer(f"Пожалуйста, введите Вашу электронную почту:")
    await Reg.user_email.set()


async def set_user_email(message: types.Message, state=FSMContext):
    """
    Изначально была валидация почты. В процессе я её убрал.
    Дело в том, что регулярка не обрабатывает тот случай,
    когда в самой почте может быть несколько точек.
    код не убирал, коль что - добавишь. Если tg_id пользователя
    есть в базе - пропустит дальше. Если нет - попросит почту.
    Если почта есть в базе, то значение tg_id будет обновлено, а бот
    пустит пользователя дальше. Если нет - "тупик"
    """
    pattern = r'^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,3}$'
    is_found = False
    if re.fullmatch(pattern, message.text):
        is_found = False
        await state.update_data(user_email=message.text)
        find_table = table.all()
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserEmail'] == message.text:
                is_found = True
                element_id = find_table[index]['id']
                await message.answer(
                    f"Добро пожаловать, {find_table[index]['fields']['UserName']} {find_table[index]['fields']['UserSurname']}")
                await state.finish()
                table.update(record_id=str(element_id), fields={"UserIDTG": str(message.from_user.id)})
                await menu(message)
        if not is_found:
            await message.answer(
                "Вас нет в базе учеников! Свяжитесь с администрацией школы для выяснения подробностей.")
            await state.finish()
    else:
        await message.answer(text='Введите корректное значение электронной почты.')


def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(bot_register, commands=['register'])
    dp.register_message_handler(set_user_email, state=Reg.user_email)
