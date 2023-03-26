from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline_menu import G_MENU


def genmarkup(list_TS): # передаём в функцию data
    markup = InlineKeyboardMarkup() # создаём клавиатуру
    markup.row_width = 1 # кол-во кнопок в строке
    for i in list_TS: # цикл для создания кнопок
        pared_time = f'\U0001F5D3 {i}:00 (UTC +0)\U0001F5D3'
        markup.add(InlineKeyboardButton(pared_time, callback_data=i)) # Создаём кнопки, pared_time - название, i - каллбек дата
    markup.add(InlineKeyboardButton('\U000026A1\U000026A1\U000026A1 Main Menu \U000026A1\U000026A1\U000026A1', callback_data='menu'))
    return markup # возвращаем клавиатуру
