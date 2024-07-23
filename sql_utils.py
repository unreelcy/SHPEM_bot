from os import getenv
from dotenv import load_dotenv
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


load_dotenv()
db_user = str(getenv('DATA_BASE_USERNAME'))
db_pass = str(getenv('DATA_BASE_PASSWORD'))
db_host = str(getenv('DATA_BASE_HOST'))
db_name = str(getenv('DATA_BASE_NAME'))
db_port = int(getenv('DATA_BASE_PORT'))


def open_connect():
    ''' Подключение к базе данных '''
    try:
        connection = psycopg2.connect(user=db_user, password=db_pass, host=db_host, port=db_port, database=db_name)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return connection

    except (Exception, Error) as err:
        print(err)
        raise err


def close_connect(connection, cursor):
    if connection:
        cursor.close()
        connection.close()


class UsersOverlaps(Exception):
    def __init__(self, key, record):
        self.message = f'НАЙДЕНО НЕСКОЛЬКО ПОЛЬЗОВАТЕЛЕЙ по уникальному ключу = {key}\n лог: {record}'


def find_user(cursor, tg_user_id: int):
    ''' если пользователь есть в ДБ - вернуть "is_enabled" иначе None или ошибку'''
    try:
        cursor.execute(f"SELECT is_enable from tg_users WHERE tg_user_id = {tg_user_id}")
        record = cursor.fetchall()

        if record:
            if len(record) == 1:
                return record[0][0]
            else:
                raise UsersOverlaps(tg_user_id, record)

    except (Exception, Error) as err:
        raise err


def get_tg_id(cursor, user_id: int) -> int:
    ''' получить из ДБ "tg_user_id" с помощью "user_id" '''
    try:
        cursor.execute(f"SELECT tg_user_id from tg_users WHERE user_id = {user_id}")
        record = cursor.fetchall()

        if record:
            if len(record) == 1:
                return record[0][0]
            else:
                raise UsersOverlaps(user_id, record)

    except (Exception, Error) as err:
        print(err)


def get_user_id(cursor, tg_user_id: int) -> int:
    ''' получить из ДБ "user_id" с помощью "tg_user_id" '''
    try:
        cursor.execute(f"SELECT user_id from tg_users WHERE tg_user_id = {tg_user_id}")
        record = cursor.fetchall()

        if record:
            if len(record) == 1:
                return record[0][0]
            else:
                raise UsersOverlaps(tg_user_id, record)

    except (Exception, Error) as err:
        print(err)


def get_fio(cursor, user_id: int) -> str:
    ''' получить name из БД по user_id '''
    try:
        cursor.execute(f"SELECT name from tg_users WHERE user_id = {user_id}")
        record = cursor.fetchall()

        if record:
            if len(record) == 1:
                return record[0][0]
            else:
                raise UsersOverlaps(user_id, record)

    except (Exception, Error) as err:
        print(err)


def is_admin(cursor, user_id):
    try:
        cursor.execute(f"SELECT is_admin from tg_users WHERE user_id = {user_id}")
        record = cursor.fetchall()

        if record:
            if len(record) == 1:
                return record[0][0]
            else:
                raise UsersOverlaps(user_id, record)

    except (Exception, Error) as err:
        print(err)


def do_log(cursor,
           tg_user_id: int,
           msg_id: int,
           msg_text: str,
           bot_answer: str,
           error_text):
    try:
        cursor.execute(f"INSERT INTO logs VALUES ({tg_user_id}, {msg_id}, '{msg_text}', '{bot_answer}', '{error_text}');")

    except (Exception, Error) as err:
        print(err)


def get_all_users(cursor):
    cursor.execute('SELECT * FROM tg_users ORDER BY user_id')
    records = cursor.fetchall()
    return records


def add_user_in_db(cursor, tg_user_id, username, data):
    user_id = get_all_users(cursor)[-1][0] + 1

    cursor.execute(f"INSERT INTO tg_users VALUES ({user_id}, {tg_user_id}, '{username}', '{data['name']}', '{data['phone_number']}', true, false);")


def get_all_events(cursor):
    cursor.execute("SELECT * FROM events")
    records = cursor.fetchall()
    return records


def get_all_books(cursor):
    cursor.execute("SELECT * FROM events")
    records = cursor.fetchall()
    return records


def get_one_event(cursor, event_id):
    cursor.execute(f'SELECT * FROM events WHERE event_id = {event_id}')
    records = cursor.fetchall()
    return records


def get_event_group(cursor, leader_event_id):
    cursor.execute(f'SELECT * FROM events WHERE leader_event_id = {leader_event_id}')
    records = cursor.fetchall()
    return records


def insert_book_info(cursor, event_id, tg_user_id):
    book_id = get_all_events(cursor)[-1][0] + 1
    user_id = get_user_id(cursor, tg_user_id)
    cursor.execute(f"INSERT INTO books VALUES ({book_id}, ")
