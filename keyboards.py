from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup

ikb = InlineKeyboardMarkup()
ikb_register = InlineKeyboardMarkup()
ib1 = InlineKeyboardButton(text="Задать уровень английского", callback_data='english_level')
ib2 = InlineKeyboardButton(text="Задать таймслот", callback_data="timeslot")
ib3 = InlineKeyboardButton(text="Показать статистику", callback_data='statistics')
id4 = InlineKeyboardButton(text="Зарегистрироваться", callback_data='registration')

ikb.add(ib1).add(ib2).add(ib3)
ikb_register.add(id4)
