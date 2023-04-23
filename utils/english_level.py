from aiogram import types, Dispatcher
from user_states import Reg
from aiogram.dispatcher import FSMContext
from airtable_config import table
from keyboards.inline_english_level import user_english_level
from config import bot, dp
from utils.menu import menu
from aiogram.utils.markdown import hlink
import re

'''
Вход в режим выбора уровня языка
'''
@dp.callback_query_handler(text='eng_level')
async def eng_level(message: types.Message):
    all_table = table.all()
    for index in range(len(all_table)):
        if all_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            record_id = all_table[index]['id']  # достает record_id из БД
            try:
                msg_id_get = int(all_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            except:
                pass
            try:
                await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            except:
                pass
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"Please select your level.\n\
You can check your level on {hlink ('TEST', 'https://airtable.com/shrRKW2Hn6f9UNGVj?hide_ChatBotTest=true&prefill_ChatBotTest=true')} ", 
                disable_web_page_preview=True, parse_mode='HTML', reply_markup=user_english_level)).message_id
            print(msg_id)
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  # запись msg_id в БД
            
'''
Кусок старого ввода Уровня Языка может пригодиться для ручного ввода с клавиатуры.
'''
async def set_eng_level(message: types.Message, state: FSMContext):
    """
    Дла начала нам нужно найти record_id нашего пользователя. Далее
    мы обновляем его параметр уровня владения языка в базе
    """
    pattern = r'A0|A0-A1|A1|A1-A2|A2|A2-B1|B1|B1-B2|B2|B2-C1|C1|C1-C2|C2'
    if re.fullmatch(pattern, message.text):
        # await state.update_data(user_eng_level=message.text)
        find_table = table.all()
        element_id = ''
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                element_id = find_table[index]['id']
                msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                msg_id = (await message.answer(f"You have a {message.text} English level.")).message_id
                print(msg_id)
                user_level = str(message.text)
                table.update(record_id=str(element_id), fields={"msgIDforDEL": str(msg_id)})  # запись msg_id в БД
                table.update(record_id=str(element_id), fields={'UserEngLevel': user_level})
                # await state.finish()
                await menu(message)
    else:
        find_table = table.all()
        element_id = ''
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                element_id = find_table[index]['id']
                msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
                await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
                msg_id = (await bot.send_message(message.from_user.id, 
                    text='Oops! Wrong format!\nTry again, please. Make sure you use the keyboard.', 
                    reply_markup=user_english_level)).message_id
                print(msg_id)
                table.update(record_id=str(element_id), fields={"msgIDforDEL": str(msg_id)})

'''
Тут описанны все кнопки выбора Уровней Языка
'''
@dp.callback_query_handler(text='A0')
async def set_level_A0(message: types.Message, state: FSMContext):
    txt = 'A0'
    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            msg_id = (await bot.send_message(message.from_user.id, text=f"You have a {txt} English level.")).message_id
            print(msg_id)
            user_level = str(txt)
            table.update(record_id=str(element_id), fields={"msgIDforDEL": str(msg_id)}) # запись msg_id в БД
            table.update(record_id=str(element_id), fields={'UserEngLevel': user_level}) # запись EngLevel в БД
            await menu(message) # выдача всего Главного Меню

@dp.callback_query_handler(text='A0-A1')
async def set_level_A0_A1(message: types.Message, state: FSMContext):
    txt = 'A0-A1'
    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            msg_id = (await bot.send_message(message.from_user.id, text=f"You have a {txt} English level.")).message_id
            print(msg_id)
            user_level = str(txt)
            table.update(record_id=str(element_id), fields={"msgIDforDEL": str(msg_id)}) # запись msg_id в БД
            table.update(record_id=str(element_id), fields={'UserEngLevel': user_level})
            await menu(message)
    
@dp.callback_query_handler(text='A1')
async def set_level_A1(message: types.Message, state: FSMContext):
    txt = 'A1'
    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            msg_id = (await bot.send_message(message.from_user.id, text=f"You have a {txt} English level.")).message_id
            print(msg_id)
            user_level = str(txt)
            table.update(record_id=str(element_id), fields={"msgIDforDEL": str(msg_id)}) # запись msg_id в БД
            table.update(record_id=str(element_id), fields={'UserEngLevel': user_level})
            await menu(message)

@dp.callback_query_handler(text='A1-A2')
async def set_level_A1_A2(message: types.Message, state: FSMContext):
    txt = 'A1-A2'
    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            msg_id = (await bot.send_message(message.from_user.id, text=f"You have a {txt} English level.")).message_id
            print(msg_id)
            user_level = str(txt)
            table.update(record_id=str(element_id), fields={"msgIDforDEL": str(msg_id)}) # запись msg_id в БД
            table.update(record_id=str(element_id), fields={'UserEngLevel': user_level})
            await menu(message)

@dp.callback_query_handler(text='A2')
async def set_level_A2(message: types.Message, state: FSMContext):
    txt = 'A2'
    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            msg_id = (await bot.send_message(message.from_user.id, text=f"You have a {txt} English level.")).message_id
            print(msg_id)
            user_level = str(txt)
            table.update(record_id=str(element_id), fields={"msgIDforDEL": str(msg_id)}) # запись msg_id в БД
            table.update(record_id=str(element_id), fields={'UserEngLevel': user_level})
            await menu(message)

@dp.callback_query_handler(text='A2-B1')
async def set_level_A2_B1(message: types.Message, state: FSMContext):
    txt = 'A2-B1'
    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            msg_id = (await bot.send_message(message.from_user.id, text=f"You have a {txt} English level.")).message_id
            print(msg_id)
            user_level = str(txt)
            table.update(record_id=str(element_id), fields={"msgIDforDEL": str(msg_id)}) # запись msg_id в БД
            table.update(record_id=str(element_id), fields={'UserEngLevel': user_level})
            await menu(message)

@dp.callback_query_handler(text='B1')
async def set_level_B1(message: types.Message, state: FSMContext):
    txt = 'B1'
    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            msg_id = (await bot.send_message(message.from_user.id, text=f"You have a {txt} English level.")).message_id
            print(msg_id)
            user_level = str(txt)
            table.update(record_id=str(element_id), fields={"msgIDforDEL": str(msg_id)}) # запись msg_id в БД
            table.update(record_id=str(element_id), fields={'UserEngLevel': user_level})
            await menu(message)

@dp.callback_query_handler(text='B1-B2')
async def set_level_B1_B2(message: types.Message, state: FSMContext):
    txt = 'B1-B2'
    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            msg_id = (await bot.send_message(message.from_user.id, text=f"You have a {txt} English level.")).message_id
            print(msg_id)
            user_level = str(txt)
            table.update(record_id=str(element_id), fields={"msgIDforDEL": str(msg_id)}) # запись msg_id в БД
            table.update(record_id=str(element_id), fields={'UserEngLevel': user_level})
            await menu(message)

@dp.callback_query_handler(text='B2')
async def set_level_B2(message: types.Message, state: FSMContext):
    txt = 'B2'
    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            msg_id = (await bot.send_message(message.from_user.id, text=f"You have a {txt} English level.")).message_id
            print(msg_id)
            user_level = str(txt)
            table.update(record_id=str(element_id), fields={"msgIDforDEL": str(msg_id)}) # запись msg_id в БД
            table.update(record_id=str(element_id), fields={'UserEngLevel': user_level})
            await menu(message)

@dp.callback_query_handler(text='B2-C1')
async def set_level_B2_C1(message: types.Message, state: FSMContext):
    txt = 'B2-C1'
    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            msg_id = (await bot.send_message(message.from_user.id, text=f"You have a {txt} English level.")).message_id
            print(msg_id)
            user_level = str(txt)
            table.update(record_id=str(element_id), fields={"msgIDforDEL": str(msg_id)}) # запись msg_id в БД
            table.update(record_id=str(element_id), fields={'UserEngLevel': user_level})
            await menu(message)

@dp.callback_query_handler(text='C1')
async def set_level_C1(message: types.Message, state: FSMContext):
    txt = 'C1'
    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            msg_id = (await bot.send_message(message.from_user.id, text=f"You have a {txt} English level.")).message_id
            print(msg_id)
            user_level = str(txt)
            table.update(record_id=str(element_id), fields={"msgIDforDEL": str(msg_id)}) # запись msg_id в БД
            table.update(record_id=str(element_id), fields={'UserEngLevel': user_level})
            await menu(message)

@dp.callback_query_handler(text='C1-C2')
async def set_level_C1_C2(message: types.Message, state: FSMContext):
    txt = 'C1-C2'
    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            msg_id = (await bot.send_message(message.from_user.id, text=f"You have a {txt} English level.")).message_id
            print(msg_id)
            user_level = str(txt)
            table.update(record_id=str(element_id), fields={"msgIDforDEL": str(msg_id)}) # запись msg_id в БД
            table.update(record_id=str(element_id), fields={'UserEngLevel': user_level})
            await menu(message)

@dp.callback_query_handler(text='C2')
async def set_level_C2(message: types.Message, state: FSMContext):
    txt = 'C2'
    find_table = table.all()
    element_id = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            element_id = find_table[index]['id']
            msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            msg_id = (await bot.send_message(message.from_user.id, text=f"You have a {txt} English level.")).message_id
            print(msg_id)
            user_level = str(txt)
            table.update(record_id=str(element_id), fields={"msgIDforDEL": str(msg_id)}) # запись msg_id в БД
            table.update(record_id=str(element_id), fields={'UserEngLevel': user_level})
            await menu(message)

'''
Тут все сообщения написаные пользователем отлавливаются и получают реакцию.
Надо бы его перенести куда-нибудь в более очевидное место. Но потом.
'''
# async def echo_message(message: types.Message):
#     find_table = table.all()
#     for index in range(len(find_table)):
#         if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
#             msg_id = (await bot.send_message(message.from_user.id, 
#                 text='Oops! Wrong format!\nTry again, please. Make sure you use the keyboard.')).message_id
#             print(msg_id)

def register_handlers_english_level(dp: Dispatcher):
    dp.register_message_handler(set_eng_level, state=Reg.user_eng_level)
    # dp.register_message_handler(echo_message)