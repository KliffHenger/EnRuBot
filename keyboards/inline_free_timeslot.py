from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def genmarkup(list_TS): # передаём в функцию data
    markup = InlineKeyboardMarkup() # создаём клавиатуру
    markup.row_width = 1 # кол-во кнопок в строке
    for i in list_TS: # цикл для создания кнопок
        markup.add(InlineKeyboardButton(i, callback_data=i)) #Создаём кнопки, i[1] - название, i[2] - каллбек дата
    return markup # возвращаем клавиатуру
