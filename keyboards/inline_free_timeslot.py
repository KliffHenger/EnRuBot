from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from keyboards.inline_menu import G_MENU
from datetime import datetime, timedelta



def genmarkup(list_TS: list): # передаём в функцию data
    markup = InlineKeyboardMarkup() # создаём клавиатуру
    markup.row_width = 1 # кол-во кнопок в строке
    # print(list_TS)
    call_TS = list_TS.pop(0)
    for i in list_TS: # цикл для создания кнопок
        first_UTC = i[-5:] # i = 2023-04-30 10:00:00+0100
        delta_hours = int(first_UTC[1]+first_UTC[2]) # +0100
        delta_minutes = int(first_UTC[3]+first_UTC[4])
        str_time = i[:19]
        s_time = datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        u_time = str(s_time + timedelta(hours=delta_hours, minutes=delta_minutes))
        time_for_msg = u_time[:16]
        pared_time = f'\U0001F5D3 {time_for_msg} \U0001F5D3'
        # print(pared_time)
        markup.add(InlineKeyboardButton(pared_time, callback_data=str_time)) # Создаём кнопки, pared_time - название, i - каллбек дата
    markup.add(InlineKeyboardButton('\U000026A1\U000026A1\U000026A1 Main Menu \U000026A1\U000026A1\U000026A1', callback_data=call_TS))
    return markup # возвращаем клавиатуру

# list_TS = ['2099-09-29 19:59:59+1000', '2023-04-30 10:00:00+0100']
# genmarkup(list_TS)