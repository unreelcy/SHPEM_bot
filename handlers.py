# База aiogram
from aiogram import Router, F  # обработчики
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton  # типы
from aiogram.filters import Command  # фильтры



import states
# Свои модули
import text  # тексты сообщений
import utils
from utils import *  # общие утилиты
import sql_utils  # утилиты работы с бд
from keyboard import CallbackData
import keyboard  # клавиатуры и inline кнопки


# aiogram FSM модуль
import states  # свой модули с состояниями
from aiogram.fsm.context import FSMContext  # управление состояниями


router = Router()

"""

ИЗМЕНИТЬ МОЙ tg_user_id на 321138226

"""

''' - - - - - - - FSM HANDLERS - - - - - - - '''


@router.message(states.Registration.phone_number)  # первый этап регистрации
async def contact_handler(msg: Message, state: FSMContext):
    if msg.contact:
        await msg.answer(text.Regis.name)
        make_log(msg.from_user.id, msg.message_id, msg.text, text.Regis.name)
        await state.update_data(phone_number=msg.contact.phone_number)
        await state.set_state(states.Registration.name)
    else:
        await msg.answer(text.Regis.retry_contact_send, reply_markup=keyboard.contact_send_kb)
        make_log(msg.from_user.id, msg.message_id, msg.text, text.Regis.retry_contact_send)


@router.message(states.Registration.name)
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
            await msg.answer(text.Er.error_db)
            make_log(msg.from_user.id, msg.message_id, msg.text, text.Er.error_db, excp)
    else:
        await msg.answer(text.Regis.retry_name_send)
        make_log(msg.from_user.id, msg.message_id, msg.text, text.Regis.retry_contact_send)


@router.message(states.Booking.num_seats)
async def num_seats_handler(msg: Message, state: FSMContext):
    n = msg.text
    if n.isalnum() and 0 < int(n) < 100:
        await state.update_data(num_seats=int(n))
        data = await state.get_data()
        make_book(data, msg.from_user.id)
        await msg.answer(text.succefull_book(data['num_seats']), reply_markup=keyboard.event_info_sample())
        make_log(msg.from_user.id, msg.message_id, msg.text, text.succefull_book(data['num_seats']))
    else:
        await msg.answer(text.Booking.retry_num_seats, reply_markup=keyboard.event_info_sample())
        make_log(msg.from_user.id, msg.message_id, msg.text, text.Booking.retry_num_seats)


""" - - - - - CALLBACK HANDLERS - - - -"""


@router.callback_query(F.data == CallbackData.main_menu)
async def main_menu_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.answer()
    await callback_query.message.edit_text(text.Btns.main_menu, reply_markup=keyboard.main_menu_kb)


@router.callback_query(F.data == CallbackData.event_list)
async def event_list_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.answer()
    event_list_text, next_page_data = utils.check_events()
    await callback_query.message.edit_text(event_list_text,
                                           reply_markup=keyboard.event_list_or_group('', next_page_data))


@router.callback_query(F.data.startswith('make_book+'))
async def book_step_one(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.set_state(states.Booking.event_id)
    await state.update_data(event_id=int(callback_query.data.split('+')[1]))
    await state.set_state(states.Booking.book_type)
    await callback_query.message.edit_text(text=text.Booking.book_type, reply_markup=keyboard.book_type_kb)


@router.callback_query(F.data.startswith('book_type+'))
async def book_step_one(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.update_data(book_type=callback_query.data.split('+')[1])
    await state.set_state(states.Booking.num_seats)
    await callback_query.message.edit_text(text=text.Booking.num_seats, reply_markup=keyboard.event_info_sample())


""" - - - - COMMAND HANDLERS - - - - - - """


@router.message(F.text.regexp(r'\/event_[0-9]+'))
async def event_info_handler(msg: Message):
    event_id = int(msg.text.split('/event_')[1])
    event_info, kbd = get_event_info(event_id)
    await msg.answer(event_info, reply_markup=kbd)
    make_log(msg.from_user.id, msg.message_id, msg.text, event_info)


@router.message(Command("start"))  # при /start проверяем есть ли чел в базе данных
async def start_handler(msg: Message, state: FSMContext):
    print('start')
    # check user
    try:
        is_enable = check_user(msg.from_user.id)
        print(is_enable)
        if is_enable is None:  # если юзера нет в БД
            await state.set_state(states.Registration.phone_number)
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
        await msg.answer(text.Er.error_db)
        print(excp)
        make_log(msg.from_user.id, msg.message_id, msg.text, text.Er.error_db, excp)


"""------- SECRET HANDLER -----"""


@router.message(F.text.lower().contains('мяу'))
async def myau_handler(msg: Message):
    await msg.answer("гав")
    make_log(msg.from_user.id, msg.message_id, msg.text, 'гав')


"""------- OTHER HANDLERS ------"""


@router.message()  # любое другое сообщение
async def start_handler(msg: Message, state: FSMContext):
    print('start')
    # check user
    try:
        is_enable = check_user(msg.from_user.id)
        print(is_enable)
        if is_enable is None:  # если юзера нет в БД
            await state.set_state(states.Registration.phone_number)
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
        await msg.answer(text.Er.error_db)
        print(excp)
        make_log(msg.from_user.id, msg.message_id, msg.text, text.Er.error_db, excp)
