from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


user_english_level = InlineKeyboardMarkup().row(
    InlineKeyboardButton('A0', callback_data='A0'),
    InlineKeyboardButton('A0-A1', callback_data='A0-A1'),
    InlineKeyboardButton('A1', callback_data='A1')).row(
    InlineKeyboardButton('A1-A2', callback_data='A1-A2'),
    InlineKeyboardButton('A2', callback_data='A2'),
    InlineKeyboardButton('A2-B1', callback_data='A2-B1')).row(
    InlineKeyboardButton('B1', callback_data='B1'),
    InlineKeyboardButton('B1-B2', callback_data='B1-B2'),
    InlineKeyboardButton('B2', callback_data='B2')).row(
    InlineKeyboardButton('B2-C1', callback_data='B2-C1'),
    InlineKeyboardButton('C1', callback_data='C1'),
    InlineKeyboardButton('C1-C2', callback_data='C1-C2'),
    InlineKeyboardButton('C2', callback_data='C2'))