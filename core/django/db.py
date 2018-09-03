from enum import Enum
from django.db import connection


class DATABASE(Enum):
    MYSQL = 'mysql'
    POSTGRES = 'postgresql'


def get_next_id(model_class):
    MYSQL = "SELECT Auto_increment FROM information_schema.tables WHERE table_name='%s'"
    POSTGRES = "Select nextval(pg_get_serial_sequence('%s', 'id')) as new_id;"

    if connection.vendor == DATABASE.POSTGRES.value:
        sql = POSTGRES % model_class._meta.db_table
    elif connection.vendor == DATABASE.MYSQL.value:
        sql = MYSQL % model_class._meta.db_table
    else:
        raise NotImplemented

    cursor = connection.cursor()
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()
    return row[0]
