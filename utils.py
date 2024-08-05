from datetime import datetime

import keyboard
import sql_utils
import text


def add_user(tg_user_id, username, data):
    connection = sql_utils.open_connect()
    cursor = connection.cursor()

    sql_utils.add_user_in_db(cursor, tg_user_id, username, data)

    sql_utils.close_connect(connection, cursor)


def make_log(tg_user_id, msg_id, msg_text, bot_answer, error_text=''):
    connection = sql_utils.open_connect()
    cursor = connection.cursor()

    sql_utils.do_log(cursor, tg_user_id, msg_id, msg_text, bot_answer, error_text)

    sql_utils.close_connect(connection, cursor)


def check_user(tg_user_id):
    connection = sql_utils.open_connect()
    cursor = connection.cursor()

    is_enable = sql_utils.find_user(cursor, tg_user_id)
    sql_utils.close_connect(connection, cursor)

    return is_enable


def generate_online_offline_marker_time(event: list) -> tuple:
    if event[3] == 0:
        offline = ''
    elif event[3] == -1:
        offline = '<b>Оффлайн</b> - <i>Мест неограничено</i>'
    elif event[3] == event[5]:
        offline = '<b>Оффлайн</b> - <i>Мест нет</i>'
    else:
        offline = f'<b>Оффлайн</b> - Свободно {event[3] - event[5]}/{event[3]}'

    if event[2] == 0:
        online = ''
    elif event[2] == -1:
        online = '<b>Онлайн</b> - <i>Мест неограничено</i>'
    elif event[2] == event[4]:
        online = '<b>Онлайн</b> - <i>Мест нет</i>'
    else:
        online = f'<b>Онлайн</b> - Свободно {event[2] - event[4]}/{event[2]}'

    if ((event[2] == 0 or event[2] == event[4]) and (event[3] == 0 or event[3] == event[5])) and event[2] != -1 and event[3] != -1:
        marker = '🟥'
    else:
        marker = '🟩'

    from_table = event[7]
    time = datetime(year=int(from_table[:4]),
                    month=int(from_table[5:7]),
                    day=int(from_table[8:10]),
                    hour=int(from_table[11:13]),
                    minute=int(from_table[14:16]),
                    second=int(from_table[17:19]))

    return online, offline, marker, time.strftime("%d.%m в %H:%M")


def check_events() -> tuple:
    output = []

    connection = sql_utils.open_connect()
    cursor = connection.cursor()

    records = sql_utils.get_all_events(cursor)

    for event in records:
        if not event[8]:  # если is_group == False
            online, offline, marker, time = generate_online_offline_marker_time(event)

            descript = f'{marker} {str(event[1])} 📅 {time} \n {offline} {online} \nПодробнее - /event_{event[0]}'

        else:  # если is_group == True leader_event_id == NULL
            descript = f'▫️ {str(event[1])} 📅 {event[7]} \nПодробнее - /event_{event[0]}'

        output.append(descript)

    sql_utils.close_connect(connection, cursor)

    if len(output) > 10:
        event_list_text = '\n\n'.join(output[:10])
        next_page_data = '2'
        return event_list_text, next_page_data

    return '\n\n'.join(output), ''


def count_free_space(event: list):
    if event[2] == -1:
        online = -1
    else:
        online = max(0, event[2] - event[4])

    if event[3] == -1:
        offline = -1
    else:
        offline = max(0, event[3] - event[5])

    return str(online), str(offline)


def get_event_info(event_id):
    connection = sql_utils.open_connect()
    cursor = connection.cursor()
    records = sql_utils.get_one_event(cursor, event_id)

    if records:  # если что-то нашлось с таким id
        event = records[0]

        if not event[8] or (event[8] and event[9] is not None):  # если событие без группы или отдельное в группе
            sql_utils.close_connect(connection, cursor) # больше sql нам не нужен

            online_text, offline_text, marker, time = generate_online_offline_marker_time(event)
            descript = f'{marker} {str(event[1])} 📅 {time} \n {offline_text} {online_text}\n\nОписание:\n{event[6]}'

            online, offline = count_free_space(event)

            if marker == '🟩':
                return descript, keyboard.event_info_sample(event_id, online, offline)
            return descript, keyboard.event_info_sample()

        else:  # если событие - заголовок группы
            other_events = sql_utils.get_event_group(cursor, event_id)
            sql_utils.close_connect(connection, cursor)
            output = [f'▫️ {str(event[1])}\n\n']

            for small_event in other_events:
                online_text, offline_text, marker, time = generate_online_offline_marker_time(small_event)
                small_descript = f'{marker} 📅 {time} \n {offline_text} {online_text} \nПодробнее - /event_{small_event[0]}'
                output.append(small_descript)
            return

    return text.Er.no_event, keyboard.event_info_sample()


def make_book(data, tg_user_id):
    connection = sql_utils.open_connect()
    cursor = connection.cursor()
    sql_utils.insert_book_info(cursor, tg_user_id, data)
    sql_utils.close_connect(connection, cursor)
