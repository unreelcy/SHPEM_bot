import psycopg2
from os import getenv
from dotenv import load_dotenv

try:  # пробуем подключиться к бд
    load_dotenv()
    host = getenv('DATA_BASE_HOST')
    user = getenv('DATA_BASE_USER')
    password = getenv('DATA_BASE_PASSWORD')
    database = getenv('DATA_BASE_DBNAME_USERLIST')

    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
except Exception as _ex:  # если ошибка
    print("[INFO] Error while connecting to database", _ex)


def find_user(tg_userid: str):
    pass