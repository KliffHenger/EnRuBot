from aiogram import types, Dispatcher
from airtable_config import table
from config import dp, bot
from keyboards.inline_menu import G_MENU
from aiogram.utils.markdown import hlink



'''очень соообщение с инструкцией и ссылкой которой нет'''
@dp.callback_query_handler(text='instruction')
async def get_instruction(message: types.Message):
    find_table = table.all()
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            record_id = find_table[index]['id']  # достает record_id из БД
            try:
                msg_id_get = int(find_table[index]['fields']['msgIDforDEL'])  # достает msg_id из БД
            except:
                pass
            try:
                await bot.delete_message(message.from_user.id, message_id=msg_id_get) # удаляет сообщение по msg_id из БД
            except:
                pass
            msg_id = (await bot.send_message(message.from_user.id, 
                text=f"This chat bot is created to offer interview practice for candidates who are looking for a job.\n\
The goal is to have 4 meetings (for 40 min) of speaking practice.\n\
We believe that after these meetings you will be more confident, relaxed and prepared for different situations during your interview.\n\
\n\
During these meetings you will be able to play the role of a recruiter or a candidate or both.\n\
\n\
Please use the following {hlink ('lists of questions', 'https://enru.me/chatbot/?utm=user')}. In our collection you will find General questions (about your education, experience, personality, behavioral questions) or Questions about your potential position or role, your expertise.\n\
\n\
Our bot will help you:\n\
\U000025AA to select your English level\n\
\U000025AA set a convenient time for a meeting\n\
\U000025AA to find a peer", parse_mode='HTML',
                reply_markup=G_MENU)).message_id
            print(msg_id)
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД