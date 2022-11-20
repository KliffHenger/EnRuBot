from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_button = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="/menu")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )