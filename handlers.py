# База aiogram
from aiogram import Router, F  # обработчики
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton  #типы
from aiogram.filters import Command  # фильтры

# Важные модули
from datetime import datetime # время и дата

# Свои модули
import text  # тексты сообщений
from utils import *  # общие утилиты
import sql_utils # утилиты работы с бд
import keyboard  # клавиатуры и inline кнопки

# aiogram FSM модуль
from states import Registration  # свой модули с состояниями
from aiogram.fsm.context import FSMContext  # управление состояниями


router = Router()
"""
ИЗМЕНИТЬ МОЙ tg_user_id на 321138226

"""


@router.message(Command("start"))  # при /start проверяем есть ли чел в базе данных
async def start_handler(msg: Message):
    # check user
    try:
        is_enable = check_user(msg.from_user.id)
        if is_enable is None:  # если юзера нет в БД
            await msg.answer(text.unknown_user % {'username': msg.from_user.username},
                             reply_markup=keyboard.contact_send)

        elif is_enable:  # если он есть и активен
            await msg.answer(text.greet_user % {'username': msg.from_user.username})

        else:  # если есть и забанен
            await msg.answer(text.banned_user % {'username': msg.from_user.username})

    except Exception as excp:
        await msg.answer(text.error_db % {'username': msg.from_user.username})
        print(excp)


@router.message(F.contact)
async def contact_handler(msg: Message):
    phone_number = msg.contact.phone_number


@router.message(F.text.lower().contains('мяу'))
async def start_handler(msg: Message):
    await msg.answer("гав")
    make_log(msg.from_user.id, msg.message_id, msg.text, 'гав')


@router.message()  # при пустом / неизвестном сообщении проверяем есть ли чел в базе данных
async def unknown_handler(msg: Message):
    # check user
    try:
        is_enable = check_user(msg.from_user.id)
        if is_enable is None:  # если юзера нет в БД
            await msg.answer(text.unknown_user % {'username': msg.from_user.username},
                             reply_markup=keyboard.contact_send)

        elif is_enable:  # если он есть и активен
            await msg.answer(text.greet_user % {'username': msg.from_user.username})

        else:  # если есть и забанен
            await msg.answer(text.banned_user % {'username': msg.from_user.username})

    except Exception as excp:
        await msg.answer(text.error_db % {'username': msg.from_user.username})
        print(excp)

