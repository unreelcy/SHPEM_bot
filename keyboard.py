from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from text import Btns


class CallbackData:
    event_list = 'event_list'
    my_events = 'my_events'
    about_us = 'about_us'
    gift = 'gift'
    help = 'help'
    main_menu = 'main_menu'
    last_page = 'last_page+'
    next_page = 'next_page+'
    tag_sort = 'tag'
    make_book = 'make_book+'


event_list_bt = InlineKeyboardButton(text=Btns.event_list, callback_data=CallbackData.event_list)
main_menu_bt = InlineKeyboardButton(text=Btns.main_menu, callback_data=CallbackData.main_menu)


def event_info_sample(event_id=0):
    if event_id > 0:
        return InlineKeyboardMarkup(inline_keyboard=[
            [event_list_bt, main_menu_bt],
            [InlineKeyboardButton(text=Btns.make_book, callback_data=CallbackData.make_book + str(event_id))]])
    return InlineKeyboardMarkup(inline_keyboard=[[event_list_bt, main_menu_bt]])


def event_list_or_group(last_page_data='', next_page_data=''):
    pages = []
    if last_page_data:
        pages.append(InlineKeyboardButton(text=Btns.last_page, callback_data=CallbackData.last_page + last_page_data))
    if next_page_data:
        pages.append(InlineKeyboardButton(text=Btns.next_page, callback_data=CallbackData.next_page + next_page_data))
    return InlineKeyboardMarkup(inline_keyboard=[pages, [event_list_bt, main_menu_bt]])


contact_send_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=Btns.send_number, request_contact=True)]
    ],
    one_time_keyboard=True)


main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            event_list_bt,
            InlineKeyboardButton(text=Btns.my_books, callback_data=CallbackData.my_events)
        ],
        [
            InlineKeyboardButton(text=Btns.about_us, url='https://integred.ru/'),
            InlineKeyboardButton(text=Btns.gift, callback_data=CallbackData.gift),
            InlineKeyboardButton(text=Btns.help, callback_data=CallbackData.help)
        ]
    ])

event_list_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=Btns.last_page, callback_data=CallbackData.last_page),
            InlineKeyboardButton(text=Btns.next_page, callback_data=CallbackData.next_page)
        ],
        [
            InlineKeyboardButton(text=Btns.tag_sort, callback_data=CallbackData.tag_sort),
            main_menu_bt
        ]
    ])
my_events_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=Btns.about_us, url='https://integred.ru/')
        ]
    ]
)

to_main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            main_menu_bt
        ]
    ]
)
