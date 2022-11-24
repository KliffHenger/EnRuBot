from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


BTN_Monday = KeyboardButton(text='MO')
BTN_Tuesday = KeyboardButton(text='TU')
BTN_Wednesday = KeyboardButton(text='WE')
BTN_Thursday = KeyboardButton(text='TH')
BTN_Friday = KeyboardButton(text='FR')
BTN_Saturday = KeyboardButton(text='SA')
BTN_Sunday = KeyboardButton(text='SU')

WEEK = ReplyKeyboardMarkup(one_time_keyboard=True).add(BTN_Monday, BTN_Tuesday, BTN_Wednesday, BTN_Thursday, 
                                    BTN_Friday, BTN_Saturday, BTN_Sunday)

