from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

BTN_ENG_LEVEL = InlineKeyboardButton('\U0001F4DA Change the level of English', callback_data='eng_level')
BTN_TIME_SLOT = InlineKeyboardButton('\U0001F551 Change Time-Slot', callback_data='timeslot')
BTN_STATISTICS = InlineKeyboardButton('\U0001F4C8 Show Stats (не работает)', callback_data='statistics')
BTN_FIND_INTERLOCUTOR = InlineKeyboardButton('\U0001F91D Find a Peer',  callback_data='find_interlocutor')
BTN_HOUR_GOAL = InlineKeyboardButton('\U0001F3C6 See the Goal', callback_data='hour_goal')
BTN_GEN_MENU = InlineKeyboardButton('\U000026A1\U000026A1\U000026A1 Main Menu \U000026A1\U000026A1\U000026A1', callback_data='menu')
BTN_DA = InlineKeyboardButton('\U0001F3C6 Yes', callback_data='register')
BTN_NET = InlineKeyboardButton('\U0001F3C6 No', callback_data='start')
BTN_START = InlineKeyboardButton('Start', callback_data='start')

START = InlineKeyboardMarkup().add(BTN_START)
G_MENU = InlineKeyboardMarkup().add(BTN_GEN_MENU)
KB_MENU = InlineKeyboardMarkup().add(BTN_ENG_LEVEL).add(BTN_TIME_SLOT).add(BTN_STATISTICS).add(BTN_FIND_INTERLOCUTOR).add(BTN_HOUR_GOAL)
NO_EN_LVL = InlineKeyboardMarkup().add(BTN_ENG_LEVEL)
NO_T_SLOT = InlineKeyboardMarkup().add(BTN_TIME_SLOT) 
START_MENU = InlineKeyboardMarkup().add(BTN_DA, BTN_NET)

