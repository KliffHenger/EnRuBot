from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


BTN_yes_i_will = InlineKeyboardButton('\U00002714 Да, я могу.', callback_data='yes_i_will')
BTN_no_i_will_not = InlineKeyboardButton('\U0000274C Нет, я не смогу.', callback_data='no_i_will_not')

KB_intention_status = InlineKeyboardMarkup().add(BTN_yes_i_will, BTN_no_i_will_not)