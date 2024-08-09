# База aiogram
from aiogram import Router, F  # обработчики
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton  # типы
from aiogram.filters import Command  # фильтры


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


@router.message(states.Banned.banned)
async def banned_handler(msg: Message):
    await msg.answer(text.Greet.banned_user % {'username': msg.from_user.username})
    make_log(msg.from_user.id, msg.message_id, msg.text, text.Greet.banned_user % {'username': msg.from_user.username})


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
        data = await state.get_data()
        if data['max_seats'] == -1 or data['max_seats'] >= int(n):
            data['num_seats'] = int(n)
            make_book(data, msg.from_user.id)
            await msg.answer(text.succefull_book(data['num_seats']), reply_markup=keyboard.event_info_sample())
            make_log(msg.from_user.id, msg.message_id, msg.text, text.succefull_book(data['num_seats']))
        else:
            await state.set_state(states.Booking.event_id)
            await state.update_data(event_id=data['event_id'], book_type=data['book_type'], max_seats=data['max_seats'])
            await state.set_state(states.Booking.num_seats)
            await msg.answer(text.Booking.retry_num_seats, reply_markup=keyboard.event_info_sample())
            make_log(msg.from_user.id, msg.message_id, msg.text, text.Booking.retry_num_seats)
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
    event_list_text, next_page_data = check_events()
    await callback_query.message.edit_text(event_list_text,
                                           reply_markup=keyboard.event_list_or_group(next_page_data=next_page_data))


@router.callback_query(F.data.startswith('make_book+'))
async def book_step_one(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.set_state(states.Booking.event_id)
    await state.update_data(event_id=int(callback_query.data.split('+')[1]))
    await state.set_state(states.Booking.book_type)
    await callback_query.message.edit_text(text=text.book_type(callback_query.data),
                                           reply_markup=keyboard.book_type_kb(callback_query.data))


@router.callback_query(F.data.startswith('book_type+'))
async def book_step_one_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.update_data(book_type=callback_query.data.split('+')[1])
    await state.update_data(max_seats=int(callback_query.data.split('+')[2]))
    await state.set_state(states.Booking.num_seats)
    await callback_query.message.edit_text(text=text.num_seats(callback_query.data.split('+')[2]),
                                           reply_markup=keyboard.event_info_sample())


@router.callback_query(F.data == 'my_events')
async def book_step_one_handler(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(text=text.Er.error_db,
                                           reply_markup=keyboard.event_info_sample())


@router.callback_query(F.data.startswith('last_page+'))
@router.callback_query(F.data.startswith('next_page+'))
async def last_page_handler(callback_query: CallbackQuery):
    await callback_query.answer()
    edit_text, kb = next_or_last_page(callback_query.data.split('+')[1])
    await callback_query.message.edit_text(text=edit_text, reply_markup=kb)


@router.callback_query(F.data == 'help')
async def book_step_one_handler(callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(text=text.Menus.help,
                                           reply_markup=keyboard.event_info_sample())


""" - - - - COMMAND HANDLERS - - - - - - """


@router.message(F.text.regexp(r'\/event_[0-9]+'))
async def event_info_handler(msg: Message):
    event_id = int(msg.text.split('/event_')[1])
    event_info, kbd = get_event_info(event_id)
    await msg.answer(event_info, reply_markup=kbd)
    make_log(msg.from_user.id, msg.message_id, msg.text, event_info)


@router.message(Command("start"))  # при /start проверяем есть ли чел в базе данных
async def start_handler(msg: Message, state: FSMContext):
    # check user
    try:
        is_enable = check_user(msg.from_user.id)
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
            await state.set_state(states.Banned.banned)
            await msg.answer(text.Greet.banned_user % {'username': msg.from_user.username})
            make_log(msg.from_user.id, msg.message_id, msg.text,
                     text.Greet.banned_user % {'username': msg.from_user.username})

    except Exception as excp:
        await msg.answer(text.Er.error_db)
        make_log(msg.from_user.id, msg.message_id, msg.text, text.Er.error_db, excp)


@router.callback_query(Command("menu"))
async def command_menu_handler(msg: Message, state: FSMContext):
    await state.clear()
    is_enable = check_user(msg.from_user.id)
    if is_enable is None:  # если юзера нет в БД
        await state.set_state(states.Registration.phone_number)
        await msg.answer(text.Greet.unknown_user % {'username': msg.from_user.username},
                         reply_markup=keyboard.contact_send_kb)
        make_log(msg.from_user.id, msg.message_id, msg.text, text.Greet.unknown_user)

    elif is_enable:  # если он есть и активен
        await msg.answer(text.Btns.main_menu, reply_markup=keyboard.main_menu_kb)
        make_log(msg.from_user.id, msg.message_id, msg.text,
                 text.Btns.main_menu)

    else:  # если есть и забанен
        await state.set_state(states.Banned.banned)
        await msg.answer(text.Greet.banned_user % {'username': msg.from_user.username})
        make_log(msg.from_user.id, msg.message_id, msg.text,
                 text.Greet.banned_user % {'username': msg.from_user.username})


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
