from aiogram import types, Dispatcher
from config import bot, dp
from keyboards.inline_menu import U_STAT, G_MENU
from airtable_config import msg_table, table


async def send_now_all_users(message: types.Message):
    all_table = table.all()
    msg_tb = msg_table.get('recT3yyKolTij69an')
    for index in range(len(all_table)):
        tg_id = all_table[index]['fields']['UserIDTG']
        text_msg = msg_tb['fields']['Text']
        try:
            await bot.send_message(int(tg_id), text=text_msg, reply_markup=G_MENU)
        except:
            pass

async def send_now_noreg_users(message: types.Message):
    all_table = table.all()
    msg_tb = msg_table.get('recG8BPHIGdZIg0NO')
    for index in range(len(all_table)):
        tg_id = all_table[index]['fields']['UserIDTG']
        en_lvl = all_table[index]['fields']['UserEngLevel']
        text_msg = msg_tb['fields']['Text']
        if en_lvl == 'None': # сюда попадают все, кто нормально не зарегался в боте
            try:
                await bot.send_message(int(tg_id), text=text_msg, reply_markup=G_MENU)
            except:
                pass
        else: # сюда попадают остальные, но трогать их не надо. Они и так молодцы.
            pass



def register_handlers_send_msg(dp: Dispatcher):
    dp.register_message_handler(send_now_all_users, commands=['3301send_now_all_users'])
    dp.register_message_handler(send_now_noreg_users, commands=['3301send_now_noreg_users'])