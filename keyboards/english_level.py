from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_english_level = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="A1")
            ],
            [
                KeyboardButton(text="A2")
            ],
            [
                KeyboardButton(text="B1")
            ],
            [
                KeyboardButton(text="B2")
            ],
            [
                KeyboardButton(text="C1")
            ],
            [
                KeyboardButton(text="C2")
            ],

        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )