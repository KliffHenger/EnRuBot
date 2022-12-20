from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

BTN_ENG_LEVEL = InlineKeyboardButton('Change the level of English', callback_data='eng_level')
BTN_TIME_SLOT = InlineKeyboardButton('Change Time-Slot', callback_data='timeslot')
BTN_STATISTICS = InlineKeyboardButton('View Statistics (не работает)', callback_data='statistics')
BTN_FIND_INTERLOCUTOR = InlineKeyboardButton('Find the Interlocutor',  callback_data='find_interlocutor')
BTN_HOUR_GOAL = InlineKeyboardButton('See the Goal', callback_data='hour_goal')
BTN_GEN_MENU = InlineKeyboardButton('Main Menu', callback_data='menu')
BTN_DA = InlineKeyboardButton('Yes', callback_data='register')
BTN_NET = InlineKeyboardButton('No', callback_data='start')

# START = ReplyKeyboardMarkup().add(BTN_START)
G_MENU = InlineKeyboardMarkup().add(BTN_GEN_MENU)
KB_MENU = InlineKeyboardMarkup().add(BTN_ENG_LEVEL).add(BTN_TIME_SLOT).add(BTN_STATISTICS).add(BTN_FIND_INTERLOCUTOR).add(BTN_HOUR_GOAL)
NO_EN_LVL = InlineKeyboardMarkup().add(BTN_ENG_LEVEL)
NO_T_SLOT = InlineKeyboardMarkup().add(BTN_TIME_SLOT) 
START_MENU = InlineKeyboardMarkup().add(BTN_DA, BTN_NET)

