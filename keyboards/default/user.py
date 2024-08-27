from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_markup = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="Ro'yxatdan o'tish"),
        ],
    ],
    resize_keyboard=True
)


user_data_confirm = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text="Tasdiqlash "),
            KeyboardButton(text="Bekor qilish"),
        ],
    ],
    resize_keyboard=True
)