from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

BTN_ENG_LEVEL = InlineKeyboardButton('\U0001F4DA Select my English Level', callback_data='eng_level')
BTN_TIME_SLOT = InlineKeyboardButton('\U0001F551 Change the time slot', callback_data='timeslot')
BTN_STATISTICS = InlineKeyboardButton('\U0001F4C8 Show stats', callback_data='statistics')
BTN_FIND_INTERLOCUTOR = InlineKeyboardButton('\U0001F91D Find a Peer',  callback_data='find_interlocutor')
BTN_HOUR_GOAL = InlineKeyboardButton('\U0001F3C6 See the Goal', callback_data='hour_goal')
BTN_GEN_MENU = InlineKeyboardButton('\U000026A1\U000026A1\U000026A1 Main Menu \U000026A1\U000026A1\U000026A1', callback_data='menu')
BTN_DA = InlineKeyboardButton('\U00002714 Yes', callback_data='register')
BTN_NET = InlineKeyboardButton('\U0000274C No', callback_data='start')
BTN_START = InlineKeyboardButton('Start', callback_data='start')
BTN_HR = InlineKeyboardButton('\U00002714 HR', callback_data='role_hr')
BTN_CANDIDATE = InlineKeyboardButton('\U0000274C Candidate', callback_data='role_candidate')
BTN_CANCEL_MEET = InlineKeyboardButton('\U000026D4 Cancel a Meeting', callback_data='cancel_meet')


START = InlineKeyboardMarkup().add(BTN_START)
G_MENU = InlineKeyboardMarkup().add(BTN_GEN_MENU)
KB_MENU = InlineKeyboardMarkup().add(BTN_ENG_LEVEL).add(BTN_TIME_SLOT).add(BTN_STATISTICS).add(BTN_FIND_INTERLOCUTOR).add(BTN_HOUR_GOAL)
PARED_MENU = InlineKeyboardMarkup().add(BTN_STATISTICS).add(BTN_HOUR_GOAL)
NO_EN_LVL = InlineKeyboardMarkup().add(BTN_ENG_LEVEL)
NO_T_SLOT = InlineKeyboardMarkup().add(BTN_TIME_SLOT) 
START_MENU = InlineKeyboardMarkup().add(BTN_DA, BTN_NET)
U_STAT = InlineKeyboardMarkup().add(BTN_HR, BTN_CANDIDATE)
C_MEET_MENU = InlineKeyboardMarkup().add(BTN_CANCEL_MEET, BTN_GEN_MENU)

