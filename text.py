class Greet:
    unknown_user = 'Приветствую, %(username)s, я бот для бронирования мест на мероприятия.\nВас нет в нашей базе, поэтому предлагаю познакомится, отправьте пожалуйста ваш номер телефона с помощью кнопки снизу.'
    greet_user = 'Здравствуйте, %(username)s, я вижу, что мы уже знакомы.\nВыберите из меню необходимые пункты.'
    banned_user = "Сожалеем, %(username)s, вы заблокированы администраторами бота, обратитесь в поддержку.\n\nАдмины:\n    @unrelcy\n    @aksikor"


class Er:
    error_db = "Сожалеем, у нас произошла ошибка при работе с Базой Данных, обратитесь в поддержку."
    no_event = 'Сожалем, такого мероприятия у нас пока нет.'


class Regis:
    name = 'Отлично, теперь нам нужно знать как вас зовут.\nНапишите, пожалуйста вашу фамилию и имя через пробел, вот пример:\n<i>Могилевская Елена</i>'
    retry_contact_send = "Что-то пошло не так, давайте вы еще раз попробуете нажать на кнопку у клавиатуры)"
    successful_name = "Поздравляю, мы успешно познакомились.\nДобавил вас в нашу Базу Данных, чтобы больше никогда вас не терять ;)"
    retry_name_send = "Неверный формат, возмножно вы указали только имя или фамилию.\nНапомню вам пример ввода данныx:\n<i>Могилевская Елена</i>"


class Booking:
    retry_num_seats = 'Недостоверный формат данных, напишите одно число.'


class Menus:
    main_menu = 'Основное меню'
    help = 'За помощью обращаться к админам:\n@AksiKor\n@mrtigerfox\n\n Создатель бота - @unrelcy'


class Btns:
    main_menu = 'Основное меню 🏠'
    event_list = 'Список мероприятий 🗓️'
    make_book = 'Забронировать место 🪑'
    send_number = "Отправить номер телефона 📱"
    last_page = '⬅️ Предыдущяя страница'
    next_page = 'Cледующая страница ➡️'
    tag_sort = 'Сортировка по тегам'
    my_books = 'Мои брони 📋'
    about_us = 'О Школе ℹ️'
    gift = 'Подарок 🎁'
    help = 'Помощь ❓'
    online_type = 'Онлайн место 🖥️'
    offline_type = 'Оффлайн место 🪑'


def succefull_book(num_seats):
    if num_seats % 10 == 1:
        say = f' {num_seats} место'
    elif 5 > num_seats % 10 > 1:
        say = f' {num_seats} места'
    else:
        say = f' {num_seats} мест'

    return 'Успешно забронировано' + say


def book_type(callback_data):
    data = callback_data.split('+')
    online, offline = int(data[2]), int(data[3])
    book_type = 'Выберите тип бронируемого места\n'

    if offline == -1:
        book_type += '\n<b>Оффлайн</b> - <i>Мест неограничено</i>'
    elif offline > 0:
        book_type += f'\n<b>Оффлайн</b> - Свободно {offline}'

    if online == -1:
        book_type += '\n<b>Онлайн</b> - <i>Мест неограничено</i>'
    elif online > 0:
        book_type += f'\n<b>Онлайн</b> - Свободно {offline}'

    return book_type


def num_seats(max_seats):
    base_message = 'Укажите количество бронируемых мест, напишите одно число.\n\nМаксимальное количество - '
    if max_seats == -1:
        return base_message + 'не ограничено.'
    return base_message + str(max_seats) + '.'
