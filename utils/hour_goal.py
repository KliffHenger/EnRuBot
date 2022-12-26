from aiogram import types, Dispatcher
from airtable_config import table
from config import dp, bot
from keyboards.inline_menu import G_MENU


@dp.callback_query_handler(text='hour_goal')
async def get_hour_goal(message: types.Message):
    find_table = table.all()
    user_hour_goal = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            user_hour_goal = find_table[index]['fields']['UserHourGoal']
    msg_id = (await bot.send_message(message.from_user.id, f"You have {user_hour_goal} meetings left to the goal.", reply_markup=G_MENU)).message_id
    print(msg_id)
    # await bot.delete_message(message.from_user.id, msg_id-1)
    

async def get_hour_goal(message: types.Message):
    find_table = table.all()
    user_hour_goal = ''
    for index in range(len(find_table)):
        if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
            user_hour_goal = find_table[index]['fields']['UserHourGoal']
    msg_id = (await message.answer(f"You have {user_hour_goal} meetings left to the goal.", reply_markup=G_MENU)).message_id
    print(msg_id)
    

def register_handlers_hour_goal(dp: Dispatcher):
    dp.register_message_handler(get_hour_goal, commands=['hour_goal'])