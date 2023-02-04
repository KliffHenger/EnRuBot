from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline_menu import G_MENU


def genmarkup(list_TS): # передаём в функцию data
    markup = InlineKeyboardMarkup() # создаём клавиатуру
    markup.row_width = 1 # кол-во кнопок в строке
    for i in list_TS: # цикл для создания кнопок
        markup.add(InlineKeyboardButton(i, callback_data=i)) # Создаём кнопки, i[1] - название, i[2] - каллбек дата
    markup.add(InlineKeyboardButton('\U000026A1\U000026A1\U000026A1 Main Menu \U000026A1\U000026A1\U000026A1', callback_data='menu'))
    return markup # возвращаем клавиатуру
