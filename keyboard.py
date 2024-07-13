from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


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


contact_send_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Отправить номер телефона 📱", request_contact=True)]
    ],
    one_time_keyboard=True)


main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Список мероприятий 🗓️', callback_data=CallbackData.event_list),
            InlineKeyboardButton(text='Мои брони 📋', callback_data=CallbackData.my_events)
        ],
        [
            InlineKeyboardButton(text='О Школе ℹ️', url='https://integred.ru/'),
            InlineKeyboardButton(text='Подарок 🎁', callback_data=CallbackData.gift),
            InlineKeyboardButton(text='Помощь ❓', callback_data=CallbackData.help)
        ]
    ])

event_list_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='⬅️ Предыдущяя страница', callback_data=CallbackData.last_page),
            InlineKeyboardButton(text='Cлеудущая страница ➡️', callback_data=CallbackData.next_page)
        ],
        [
            InlineKeyboardButton(text='Сортировка по тегам', callback_data=CallbackData.tag_sort),
            InlineKeyboardButton(text='Основное меню', callback_data=CallbackData.main_menu)
        ]
    ])
my_events_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='О Школе ℹ️', url='https://integred.ru/')
        ]
    ]
)

to_main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Основное Меню', callback_data=CallbackData.main_menu)
        ]
    ]
)