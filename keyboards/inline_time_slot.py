from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


BTN_Monday = InlineKeyboardButton('Monday', callback_data='MO')
BTN_Tuesday = InlineKeyboardButton('Tuesday', callback_data='TU')
BTN_Wednesday = InlineKeyboardButton('Wednesday', callback_data='WE')
BTN_Thursday = InlineKeyboardButton('Thursday', callback_data='TH')
BTN_Friday = InlineKeyboardButton('Friday', callback_data='FR')
BTN_Saturday = InlineKeyboardButton('Saturday', callback_data='SA')
BTN_Sunday = InlineKeyboardButton('Sunday', callback_data='SU')

WEEK = InlineKeyboardMarkup().add(BTN_Monday, BTN_Tuesday, BTN_Wednesday, BTN_Thursday, 
                                    BTN_Friday, BTN_Saturday, BTN_Sunday)

