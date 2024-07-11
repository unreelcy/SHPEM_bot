from os import getenv
from dotenv import load_dotenv
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


load_dotenv()
db_username = getenv('DATA_BASE_USERNAME')
db_pass = getenv('DATA_BASE_PASSWORD')
db_host = getenv('DATA_BASE_HOST')
db_name = getenv('DATA_BASE_NAME')
db_port = getenv('DATA_BASE_PORT')


class usersoverlaps(Exception):
    def __init__(self, key, record):
        self.message = f'НАЙДЕНО НЕСКОЛЬКО ПОЛЬЗОВАТЕЛЕЙ по уникальному ключу = {key}\n лог: {record}'


def manual_sql_query():
    try:
        connection = psycopg2.connect(user=db_username, password=db_pass, host=db_host, port=db_port, database=db_name)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        cursor.execute(f"update")
        record = cursor.fetchall()


        if record:
            if len(record) == 1:
                return record[0][0]
            else:
                raise usersoverlaps(tg_user_id, record)

    except (Exception, Error) as err:
        print(err)

    finally:
        if connection:
            cursor.close()
            connection.close()


def find_user(tg_user_id: int):
    ''' если пользователь есть в ДБ - вернуть "is_enabled" иначе None или ошибку'''

    try:
        # Подключение к базе данных
        connection = psycopg2.connect(user=db_username, password=db_pass, host=db_host, port=db_port, database=db_name)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        cursor.execute(f"SELECT is_enable from tg_users WHERE tg_user_id = {tg_user_id}")
        record = cursor.fetchall()


        if record:
            if len(record) == 1:
                return record[0][0]
            else:
                raise usersoverlaps(tg_user_id, record)

    except (Exception, Error) as err:
        raise err

    finally:
        if connection:
            cursor.close()
            connection.close()

def get_tg_id(user_id: int) -> int:
    ''' получить из ДБ "tg_user_id" с помощью "user_id" '''
    try:
        connection = psycopg2.connect(user=db_username, password=db_pass, host=db_host, port=db_port, database=db_name)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        cursor.execute(f"SELECT tg_user_id from tg_users WHERE user_id = {user_id}")
        record = cursor.fetchall()

        if record:
            if len(record) == 1:
                return record[0][0]
            else:
                raise usersoverlaps(user_id, record)

    except (Exception, Error) as err:
        print(err)

    finally:
        if connection:
            cursor.close()
            connection.close()


def get_user_id(tg_user_id: int) -> int:
    ''' получить из ДБ "user_id" с помощью "tg_user_id" '''
    try:
        connection = psycopg2.connect(user=db_username, password=db_pass, host=db_host, port=db_port, database=db_name)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        cursor.execute(f"SELECT user_id from tg_users WHERE tg_user_id = {tg_user_id}")
        record = cursor.fetchall()

        if record:
            if len(record) == 1:
                return record[0][0]
            else:
                raise usersoverlaps(tg_user_id, record)

    except (Exception, Error) as err:
        print(err)

    finally:
        if connection:
            cursor.close()
            connection.close()


def get_fio(user_id: int) -> str:
    ''' получить name из БД по user_id'''
    try:
        connection = psycopg2.connect(user=db_username, password=db_pass, host=db_host, port=db_port, database=db_name)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        cursor.execute(f"SELECT name from tg_users WHERE user_id = {user_id}")
        record = cursor.fetchall()

        if record:
            if len(record) == 1:
                return record[0][0]
            else:
                raise usersoverlaps(user_id, record)

    except (Exception, Error) as err:
        print(err)

    finally:
        if connection:
            cursor.close()
            connection.close()


def is_admin(user_id):
    try:
        connection = psycopg2.connect(user=db_username, password=db_pass, host=db_host, port=db_port, database=db_name)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        cursor.execute(f"SELECT is_admin from tg_users WHERE user_id = {user_id}")
        record = cursor.fetchall()

        if record:
            if len(record) == 1:
                return record[0][0]
            else:
                raise usersoverlaps(user_id, record)

    except (Exception, Error) as err:
        print(err)

    finally:
        if connection:
            cursor.close()
            connection.close()