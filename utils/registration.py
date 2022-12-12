from aiogram import types, Dispatcher
from user_states import Reg
from aiogram.dispatcher import FSMContext
from airtable_config import table
from utils.menu import menu
from config import bot, dp
import re



last_msg = 0


async def bot_register(message: types.Message):
    last_msg = (await bot.send_message(message.from_user.id,
        f"Пожалуйста, введите Вашу электронную почту:")).message_id
    # await bot.delete_message(message.from_user.id, message_id=last_msg-2)
    await bot.delete_message(message.from_user.id, message_id=last_msg-1)
    await Reg.user_email.set()

@dp.callback_query_handler(text='register')
async def bot_register(message: types.Message):
    last_msg = (await bot.send_message(message.from_user.id,
        f"Пожалуйста, введите Вашу электронную почту:")).message_id
    # await bot.delete_message(message.from_user.id, message_id=last_msg-2)
    await bot.delete_message(message.from_user.id, message_id=last_msg-1)
    await Reg.user_email.set()

async def set_user_email(message: types.Message, state=FSMContext):
    """
    Валидация почты работает. Если tg_id пользователя
    есть в базе - пропустит дальше. Если нет - попросит почту.
    Если почта есть в базе, то значение tg_id будет обновлено, а бот
    пустит пользователя дальше.
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
                wrong_date = None
                wrong_status = False
                element_id = find_table[index]['id']
                last_msg = (await bot.send_message(message.from_user.id,
                    f"Добро пожаловать, {find_table[index]['fields']['UserName']} {find_table[index]['fields']['UserSurname']}")).message_id
                await bot.delete_message(message.from_user.id, message_id=last_msg-1)
                await state.finish()
                table.update(record_id=str(element_id), fields={"UserIDTG": str(message.from_user.id)})
                table.update(record_id=str(element_id), fields={"UserEngLevel": str(wrong_date)})
                table.update(record_id=str(element_id), fields={"UserTimeSlot": str(wrong_date)})
                table.update(record_id=str(element_id), fields={"IsPared": str(wrong_status)})
                await menu(message)
        if not is_found:
            last_msg = (await bot.send_message(message.from_user.id,
                "Вас нет в базе учеников! Свяжитесь с администрацией школы для выяснения подробностей.")).message_id
            await bot.delete_message(message.from_user.id, message_id=last_msg-2)
            await bot.delete_message(message.from_user.id, message_id=last_msg-1)
            await state.finish()
    else:
        last_msg = (await bot.send_message(message.from_user.id,
            text='Введите корректное значение электронной почты.')).message_id
        await bot.delete_message(message.from_user.id, message_id=last_msg-2)
        await bot.delete_message(message.from_user.id, message_id=last_msg-1)



def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(bot_register, commands=['register'])
    dp.register_message_handler(set_user_email, state=Reg.user_email)
