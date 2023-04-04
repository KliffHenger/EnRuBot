from aiogram import types, Dispatcher
from config import bot, dp
from keyboards.inline_menu import U_STAT, G_MENU
from airtable_config import msg_table





def register_handlers_time_slot(dp: Dispatcher):
    dp.register_message_handler(send_now_all_users, commands=['3301send_now_all_users'])
    dp.register_message_handler(send_now_noreg_users, commands=['3301send_now_noreg_users'])
    dp.register_message_handler(send_ever_week_all_users, commands=['3301send_ever_week_all_users'])