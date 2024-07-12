from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

contact_send = ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="Отправить номер телефона 📱", request_contact=True)]],
                one_time_keyboard=True)