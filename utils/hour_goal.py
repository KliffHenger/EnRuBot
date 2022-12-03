from aiogram import types, Dispatcher
from airtable_config import table
from config import dp, bot
from keyboards.inline_menu import KB_MENU


@dp.callback_query_handler(text='hour_goal')
async def get_hour_goal(message: types.Message):
    find_table = table.all()
    user_hour_goal = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            user_hour_goal = find_table[index]['fields']['UserHourGoal']
    await bot.send_message(message.from_user.id, f"Вам осталось {user_hour_goal} встреч до цели.", reply_markup=KB_MENU)
    

async def get_hour_goal(message: types.Message):
    find_table = table.all()
    user_hour_goal = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            user_hour_goal = find_table[index]['fields']['UserHourGoal']
    await message.answer(f"Вам осталось {user_hour_goal} встреч до цели.", reply_markup=KB_MENU)
    

def register_handlers_hour_goal(dp: Dispatcher):
    dp.register_message_handler(get_hour_goal, commands=['hour_goal'])