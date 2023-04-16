from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from keyboards.inline_menu import G_MENU
from datetime import datetime, timedelta



def genmarkup(list_TS: list): # передаём в функцию data
    markup = InlineKeyboardMarkup() # создаём клавиатуру
    markup.row_width = 1 # кол-во кнопок в строке
    raw_call_TS = list_TS.pop(0)
    call_TS = raw_call_TS[:19]
    for i in list_TS: # цикл для создания кнопок
        first_UTC = i[19:24] # i = 2023-04-30 10:00:00+0100
        # print(first_UTC)
        name_user = i[24:]
        print(name_user)
        delta_hours = int(first_UTC[1]+first_UTC[2]) # +0100
        delta_minutes = int(first_UTC[3]+first_UTC[4])
        str_time = i[:19]
        s_time = datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        u_time = str(s_time + timedelta(hours=delta_hours, minutes=delta_minutes))
        time_for_msg = u_time[:16]
        pared_time = f'\U0001F464{name_user} \U0001F5D3 {time_for_msg}'
        print(pared_time)
        markup.add(InlineKeyboardButton(pared_time, callback_data=str_time)) # Создаём кнопки, pared_time - название, i - каллбек дата
    markup.add(InlineKeyboardButton('Оставить мой ТаймСлот', callback_data='menu'))
    return markup # возвращаем клавиатуру

# list_TS = ['2099-09-29 19:59:59+1000Kliff', '2023-04-30 10:00:00+0100Irinachka']
# genmarkup(list_TS)