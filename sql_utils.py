from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime, BigInteger, SmallInteger, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import JSONB
from os import getenv
from dotenv import load_dotenv


DeclBase = declarative_base()


# def create_event_table(tablename):
#     class Event_Table(DeclBase):
#         __tablename__ = tablename
#         id = Column(Integer, primary_key=True)
#         book_count = Column(Integer)
#         booking_date = Column(DateTime)
#
#     load_dotenv()
#     BOT_TOKEN = getenv('BOT_TOKEN')  # берем api токен из .env файла



#
# try:  # пробуем подключиться к бд
#     load_dotenv()
#     host = getenv('DATA_BASE_HOST')
#     user = getenv('DATA_BASE_USER')
#     password = getenv('DATA_BASE_PASSWORD')
#     database = getenv('DATA_BASE_DBNAME_USERLIST')
#
#     connection = psycopg2.connect(
#         host=host,
#         user=user,
#         password=password,
#         database=database
#     )
# except Exception as _ex:  # если ошибка то выводим ее в консоль
#     print(" --- [INFO] Error while connecting to database", _ex)
#
#
# def find_user(tg_userid: str):
#     pass