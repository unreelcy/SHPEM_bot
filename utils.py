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
        if not event[8]:
            online, offline, marker, time = generate_online_offline_marker_time(event)

            descript = f'{marker} {str(event[1])} 📅 {time} \n {offline} {online} \nПодробнее - /event_{event[0]}'

        elif event[9] is None:
            descript = f'▫️ {str(event[1])} 📅 {event[7]} \nПодробнее - /event_{event[0]}'
        else:
            continue
        output.append(descript)

    sql_utils.close_connect(connection, cursor)

    if len(output) > 10:
        event_list_text = '\n\n'.join(output[:10])
        next_page_data = '\n\n'.join(output[10:])
        return event_list_text, next_page_data

    return '\n\n'.join(output), ''


def get_event_info(event_id):
    connection = sql_utils.open_connect()
    cursor = connection.cursor()
    records = sql_utils.get_one_event(cursor, event_id)

    if records:  # если что-то нашлось с таким id
        event = records[0]

        if not event[8] or (event[8] and event[9] is not None):  # если событие без группы или отдельное в группе
            sql_utils.close_connect(connection, cursor)
            status = 'single'
            online, offline, marker, time = generate_online_offline_marker_time(event)
            descript = f'{marker} {str(event[1])} 📅 {time} \n {offline} {online}\n\nОписание:\n{event[6]}'
            if marker == '🟩':
                return descript, status, keyboard.event_info_sample(event_id)
            return descript, status, keyboard.event_info_sample()

        else:  # если событие - заголовок группы
            status = 'group'
            other_events = sql_utils.get_event_group(cursor, event_id)
            sql_utils.close_connect(connection, cursor)
            output = []
            descript = f'▫️ {str(event[1])}\n\n'

            for small_event in other_events:
                online, offline, marker, time = generate_online_offline_marker_time(small_event)
                small_descript = f'{marker} 📅 {time} \n {offline} {online} \nПодробнее - /event_{small_event[0]}'
                output.append(small_descript)
            descript += '\n\n'.join(output)

    return text.Er.no_event, keyboard.event_info_sample(event_id)


def make_book():
    connection = sql_utils.open_connect()
    cursor = connection.cursor()
