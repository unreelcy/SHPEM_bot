import datetime
import sql_utils


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
