from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from datetime import datetime
import text
from utils import *
from sql_utils import *


router = Router()
"""
ИЗМЕНИТЬ МОЙ tg_user_id на 321138226
"""

@router.message(Command("start"))  # при /start проверяем есть ли чел в базе данных
async def start_handler(msg: Message):
    # check user
    print(find_user(msg.from_user.id))
    if is_enable := find_user(msg.from_user.id):
        await msg.answer(text.greet_user % {'username': msg.from_user.username})
    elif is_enable == False:
        await msg.answer(text.banned_user % {'username': msg.from_user.username})
    else:
        await msg.answer(text.greet_unknown_user % {'username': msg.from_user.username})
        keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отправить номер телефона 📱", request_contact=True)]], one_time_keyboard=True)
        await msg.answer("Отправь свой контакт:", reply_markup=keyboard)


@router.message(F.contact)
async def message_handler(msg: Message):
    phone_number = msg.contact.phone_number


@router.message()  # при пустом/неизвестном сообщении проверяем есть ли чел в базе данных
async def start_handler(msg: Message):
    # check user
    print(find_user(msg.from_user.id))
    if is_enable := find_user(msg.from_user.id):
        await msg.answer(text.greet_user % {'username': msg.from_user.username})
    elif is_enable == False:
        await msg.answer(text.banned_user % {'username': msg.from_user.username})
    else:
        await msg.answer(text.greet_unknown_user % {'username': msg.from_user.username})
        keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отправить номер телефона 📱", request_contact=True)]], one_time_keyboard=True)
        await msg.answer("Отправь свой контакт:", reply_markup=keyboard)
