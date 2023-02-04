from aiogram import types, Dispatcher
from airtable_config import table
from config import dp, bot
from keyboards.inline_menu import G_MENU
from .menu import menu


'''получение и вывод цели встреч'''
@dp.callback_query_handler(text='hour_goal')
async def get_hour_goal(message: types.Message):
    find_table = table.all()
    user_hour_goal = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            user_hour_goal = find_table[index]['fields']['UserHourGoal']
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
                text=f"You have {user_hour_goal} meetings (for 40 min) left to the goal.", reply_markup=G_MENU)).message_id
            print(msg_id)
            table.update(record_id=str(record_id), fields={"msgIDforDEL": str(msg_id)})  #запись msg_id в БД
    
    

async def get_hour_goal(message: types.Message):
    find_table = table.all()
    user_hour_goal = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            user_hour_goal = find_table[index]['fields']['UserHourGoal']
    msg_id = (await message.answer(text=f"You have {user_hour_goal} meetings (for 40 min) left to the goal.")).message_id
    print(msg_id)
    await menu(message)
    

def register_handlers_hour_goal(dp: Dispatcher):
    dp.register_message_handler(get_hour_goal, commands=['hour_goal'])