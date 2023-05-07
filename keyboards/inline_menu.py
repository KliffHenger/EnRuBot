from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


BTN_INSTR = InlineKeyboardButton('\U00002753 Instruction', callback_data='instruction')
BTN_ENG_LEVEL = InlineKeyboardButton('\U0001F4DA Select my English Level', callback_data='eng_level')
BTN_TIME_SLOT = InlineKeyboardButton('\U0001F551 Enter the time slot', callback_data='timeslot')
BTN_SHOW_TS = InlineKeyboardButton('\U0001F551  Show available time slots', callback_data='other_time_slots')
BTN_STATISTICS = InlineKeyboardButton('\U0001F4C8 Show stats', callback_data='statistics')
BTN_FIND_INTERLOCUTOR = InlineKeyboardButton('\U0001F91D Find a Partner',  callback_data='find_interlocutor')
# BTN_HOUR_GOAL = InlineKeyboardButton('\U0001F3C6 See the Goal', callback_data='hour_goal')
BTN_GEN_MENU = InlineKeyboardButton('\U000026A1 Main Menu \U000026A1', callback_data='menu')
BTN_DA = InlineKeyboardButton('\U00002714 Yes', callback_data='register')
BTN_NET = InlineKeyboardButton('\U0000274C No', callback_data='start')
BTN_START = InlineKeyboardButton('Start', callback_data='start')
BTN_HR = InlineKeyboardButton('\U0001F60E HR', callback_data='role_hr')
BTN_CANDIDATE = InlineKeyboardButton('\U0001F913 Candidate', callback_data='role_candidate')
BTN_CANCEL_MEET = InlineKeyboardButton('\U000026D4 Cancel a Meeting', callback_data='cancel_meet')
BTN_SUCC = InlineKeyboardButton('\U00002714 Yes', callback_data='select_role')
BTN_FAIL = InlineKeyboardButton('\U0000274C No', callback_data='fail_meet')
BTN_SET_CITY = InlineKeyboardButton('\U0001F5FA	Select a city', callback_data='set_city')


START = InlineKeyboardMarkup().add(BTN_START)
G_MENU = InlineKeyboardMarkup().add(BTN_GEN_MENU)
KB_MENU = InlineKeyboardMarkup().add(BTN_ENG_LEVEL).add(BTN_SHOW_TS).add(BTN_STATISTICS).add(BTN_INSTR).add(BTN_SET_CITY)
PARED_MENU = InlineKeyboardMarkup().add(BTN_CANCEL_MEET).add(BTN_INSTR).add(BTN_STATISTICS)
NO_EN_LVL = InlineKeyboardMarkup().add(BTN_ENG_LEVEL)
NO_T_SLOT = InlineKeyboardMarkup().add(BTN_ENG_LEVEL).add(BTN_SHOW_TS) 
START_MENU = InlineKeyboardMarkup().add(BTN_DA, BTN_NET)
CONF_MEET = InlineKeyboardMarkup().add(BTN_SUCC, BTN_FAIL)
U_STAT = InlineKeyboardMarkup().add(BTN_HR, BTN_CANDIDATE)
C_MEET_MENU = InlineKeyboardMarkup().add(BTN_CANCEL_MEET, BTN_GEN_MENU)
C_MEET = InlineKeyboardMarkup().add(BTN_CANCEL_MEET)
GO_FIND = InlineKeyboardMarkup().add(BTN_FIND_INTERLOCUTOR).add(BTN_GEN_MENU)
SET_TS = InlineKeyboardMarkup().add(BTN_TIME_SLOT)
SET_ENlvl_and_TS = InlineKeyboardMarkup().add(BTN_ENG_LEVEL).add(BTN_TIME_SLOT)


