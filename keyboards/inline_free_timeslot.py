from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline_menu import G_MENU
from config import week_dict


def genmarkup(list_TS): # передаём в функцию data
    markup = InlineKeyboardMarkup() # создаём клавиатуру
    markup.row_width = 1 # кол-во кнопок в строке
    for i in list_TS: # цикл для создания кнопок
        week = i[0]+i[1]
        start_time = i[2]+i[3]
        week_for_message = week_dict.get(week)
        pared_time = f'\U0001F5D3 {week_for_message}, {start_time}:00 (UTC +0)\U0001F5D3'
        markup.add(InlineKeyboardButton(pared_time, callback_data=i)) # Создаём кнопки, pared_time - название, i - каллбек дата
    markup.add(InlineKeyboardButton('\U000026A1\U000026A1\U000026A1 Main Menu \U000026A1\U000026A1\U000026A1', callback_data='menu'))
    return markup # возвращаем клавиатуру
