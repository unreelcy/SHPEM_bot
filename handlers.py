# База aiogram
from aiogram import Router, F  # обработчики
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton  # типы
from aiogram.filters import Command  # фильтры


# Важные модули
import re

# Свои модули
import text  # тексты сообщений
import utils
from utils import *  # общие утилиты
import sql_utils  # утилиты работы с бд
from keyboard import CallbackData
import keyboard  # клавиатуры и inline кнопки


# aiogram FSM модуль
from states import Registration  # свой модули с состояниями
from aiogram.fsm.context import FSMContext  # управление состояниями


router = Router()

"""
ИЗМЕНИТЬ МОЙ tg_user_id на 321138226
"""

'''------- FSM HANDLERS -------'''


@router.message(Registration.phone_number)  # первый этап регистрации
async def contact_handler(msg: Message, state: FSMContext):
    if msg.contact:
        await msg.answer(text.Regis.successful_contact)
        make_log(msg.from_user.id, msg.message_id, msg.text, text.Regis.successful_contact)
        await state.update_data(phone_number=msg.contact.phone_number)
        await state.set_state(Registration.name)
    else:
        await msg.answer(text.Regis.retry_contact_send, reply_markup=keyboard.contact_send_kb)
        make_log(msg.from_user.id, msg.message_id, msg.text, text.Regis.retry_contact_send)


@router.message(Registration.name)
async def name_handler(msg: Message, state: FSMContext):

    if len(msg.text.split()) >= 2:
        fio = [word.capitalize() for word in msg.text.strip().strip('"').strip("'").split()]
        await state.update_data(name=' '.join(fio))
        data = await state.get_data()
        await state.clear()

        try:
            add_user(msg.from_user.id, msg.from_user.username, data)
            await msg.answer(text.Regis.successful_name, reply_markup=keyboard.to_main_menu_kb)
            make_log(msg.from_user.id, msg.message_id, msg.text, text.Regis.successful_name)
        except Exception as excp:
            print(excp)
            await msg.answer(text.Er.error_db % {'username': msg.from_user.username})
            make_log(msg.from_user.id, msg.message_id, msg.text, text.Er.error_db % {'username': msg.from_user.username})
    else:
        await msg.answer(text.Regis.retry_name_send)
        make_log(msg.from_user.id, msg.message_id, msg.text, text.Regis.retry_contact_send)


"""----- CALLBACK HANDLERS ----"""


@router.callback_query(F.data == CallbackData.main_menu)
async def main_menu_handler(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(text.Menus.main_menu, reply_markup=keyboard.main_menu_kb)


@router.callback_query(F.data == CallbackData.event_list)
async def event_list_handler(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(utils.check_events(), reply_markup=keyboard.event_list_kb)


"""---- COMMAND HANDLERS ------"""


@router.message(F.text.regexp(r'\/event_[0-9]+'))
async def event_info_handler(msg: Message):
    event_id = int(msg.text.split('/event_')[1])
    print(event_id)
    event_info, status = get_event_info(event_id)
    if status == 'single' and event_info[0] == '🟩':
        await msg.answer(event_info, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            keyboard.event_list_bt,
            InlineKeyboardButton(text='Забронировать место',
                                 callback_data=f'{keyboard.CallbackData.make_book}+{event_id}')]]
        ))
        make_log(msg.from_user.id, msg.message_id, msg.text, event_info)
    else:
        await msg.answer(event_info, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[keyboard.event_list_bt]]))
        make_log(msg.from_user.id, msg.message_id, msg.text, event_info)


@router.message(Command("start"))  # при /start проверяем есть ли чел в базе данных
async def start_handler(msg: Message, state: FSMContext):
    # check user
    try:
        is_enable = check_user(msg.from_user.id)
        if is_enable is None:  # если юзера нет в БД
            await state.set_state(Registration.phone_number)
            await msg.answer(text.Greet.unknown_user % {'username': msg.from_user.username},
                             reply_markup=keyboard.contact_send_kb)
            make_log(msg.from_user.id, msg.message_id, msg.text, text.Greet.unknown_user)

        elif is_enable:  # если он есть и активен
            await msg.answer(text.Greet.greet_user % {'username': msg.from_user.username}, reply_markup=keyboard.main_menu_kb)
            make_log(msg.from_user.id, msg.message_id, msg.text, text.Greet.greet_user % {'username': msg.from_user.username})

        else:  # если есть и забанен
            await msg.answer(text.Greet.banned_user % {'username': msg.from_user.username})
            make_log(msg.from_user.id, msg.message_id, msg.text, text.Greet.banned_user % {'username': msg.from_user.username})

    except Exception as excp:
        await msg.answer(text.Er.error_db % {'username': msg.from_user.username})
        make_log(msg.from_user.id, msg.message_id, msg.text, text.Er.error_db % {'username': msg.from_user.username})


"""------- SECRET HANDLER -----"""


@router.message(F.text.lower().contains('мяу'))
async def myau_handler(msg: Message):
    await msg.answer("гав")
    make_log(msg.from_user.id, msg.message_id, msg.text, 'гав')


"""------- OTHER HANDLERS ------"""


@router.message(Command("start"))  # при /start проверяем есть ли чел в базе данных
async def start_handler(msg: Message, state: FSMContext):
    # check user
    try:
        is_enable = check_user(msg.from_user.id)
        if is_enable is None:  # если юзера нет в БД
            await state.set_state(Registration.phone_number)
            await msg.answer(text.Greet.unknown_user % {'username': msg.from_user.username},
                             reply_markup=keyboard.contact_send_kb)
            make_log(msg.from_user.id, msg.message_id, msg.text, text.Greet.unknown_user)

        elif is_enable:  # если он есть и активен
            await msg.answer(text.Greet.greet_user % {'username': msg.from_user.username},
                             reply_markup=keyboard.main_menu_kb)
            make_log(msg.from_user.id, msg.message_id, msg.text,
                     text.Greet.greet_user % {'username': msg.from_user.username})

        else:  # если есть и забанен
            await msg.answer(text.Greet.banned_user % {'username': msg.from_user.username})
            make_log(msg.from_user.id, msg.message_id, msg.text,
                     text.Greet.banned_user % {'username': msg.from_user.username})

    except Exception as excp:
        await msg.answer(text.Er.error_db % {'username': msg.from_user.username})
        make_log(msg.from_user.id, msg.message_id, msg.text, text.Er.error_db % {'username': msg.from_user.username})
