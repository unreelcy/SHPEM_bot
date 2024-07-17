from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

import text


class CallbackData:
    event_list = 'event_list'
    my_events = 'my_events'
    about_us = 'about_us'
    gift = 'gift'
    help = 'help'
    main_menu = 'main_menu'
    last_page = 'last_page'
    next_page = 'next_page'
    tag_sort = 'tag'
    make_book = 'make_book'


event_list_bt = InlineKeyboardButton(text=text.Bts.event_list, callback_data=CallbackData.event_list)
about_bt = InlineKeyboardButton(text=text.Bts.about, url='https://integred.ru/')
main_menu_bt = InlineKeyboardButton(text=text.Bts.main_menu, callback_data=CallbackData.main_menu)


contact_send_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text.Bts.send_contact, request_contact=True)]
    ],
    one_time_keyboard=True)


main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            event_list_bt,
            InlineKeyboardButton(text=text.Bts.my_books, callback_data=CallbackData.my_events)
        ],
        [
            about_bt,
            InlineKeyboardButton(text=text.Bts.gift, callback_data=CallbackData.gift),
            InlineKeyboardButton(text=text.Bts.help, callback_data=CallbackData.help)
        ]
    ])


def make_event_list_kb(last_page_data, next_page_data):
    pages = []
    if last_page_data:
        pages.append(InlineKeyboardButton(text=text.Bts.last_page,
                                          callback_data=f'CallbackData.last_page+{last_page_data}'))
    if next_page_data:
        pages.append(InlineKeyboardButton(text=text.Bts.next_page,
                                          callback_data=f'CallbackData.next_page+{next_page_data}'))
    return InlineKeyboardMarkup(
        inline_keyboard=[
            pages,
            [
                InlineKeyboardButton(text=text.Bts.tag_sort, callback_data=CallbackData.tag_sort),
                main_menu_bt
            ]
        ])


def make_my_events_kb(last_page_data, next_page_data):
    pages = []
    if last_page_data:
        pages.append(InlineKeyboardButton(text=text.Bts.last_page,
                                          callback_data=f'CallbackData.last_page+{last_page_data}'))
    if next_page_data:
        pages.append(InlineKeyboardButton(text=text.Bts.next_page,
                                          callback_data=f'CallbackData.next_page+{next_page_data}'))
    return InlineKeyboardMarkup(inline_keyboard=
                                [
                                    pages,
                                    [event_list_bt, main_menu_bt]

                                ])


to_main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            main_menu_bt
        ]
    ]
)

