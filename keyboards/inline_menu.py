from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

BTN_ENG_LEVEL = InlineKeyboardButton('Уровень Английского', callback_data='eng_level')
BTN_TIME_SLOT = InlineKeyboardButton('ТаймСлот', callback_data='timeslot')
BTN_STATISTICS = InlineKeyboardButton('Статистика', callback_data='statistics')
BTN_FIND_INTERLOCUTOR = InlineKeyboardButton('Найти Собеседника',  callback_data='find_interlocutor')

# START = ReplyKeyboardMarkup().add(BTN_START)

KB_MENU = InlineKeyboardMarkup().add(BTN_ENG_LEVEL, BTN_TIME_SLOT, BTN_STATISTICS, BTN_FIND_INTERLOCUTOR)