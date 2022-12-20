from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_english_level = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(
    KeyboardButton(text="A0"),
    KeyboardButton(text="A0-A1"),
    KeyboardButton(text="A1")).row(
    KeyboardButton(text="A1-A2"),
    KeyboardButton(text="A2"),
    KeyboardButton(text="A2-B1")).row(
    KeyboardButton(text="B1"),
    KeyboardButton(text="B1-B2"),
    KeyboardButton(text="B2")).row(
    KeyboardButton(text="B2-C1"),
    KeyboardButton(text="C1"),
    KeyboardButton(text="C1-C2"),
    KeyboardButton(text="C2"))