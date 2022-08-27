import os.path
import sqlite3
from enum import Enum


# This script is database handing methods


# connection to sqlite
connection: sqlite3.Connection
cursor: sqlite3.Cursor


def connect_database():
    if os.path.exists('database/database.db'):
        global connection, cursor
        connection = sqlite3.connect('database/database.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        return True
    else:
        return False


def disconnect_database():
    connection.close()


# Enum for select how many writes sqlite must return
class CursorReturnEnum(Enum):
    ONE_VALUE = -1
    ALL_WRITES = 0
    ALL_FIELDS = 1
    ONE_WRITE = 2


# This exception appear when sqlite cursor don't find any values in request
class NoValueError(Exception):
    def __init__(self, **kwargs):
        self.params = kwargs

    def __str__(self):
        return f'Не получилось получить значение из базы данных {self.params}'


# Method for extract dict from sqlite row type
def dict_factory(row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Basic function for make get requests
def request_get(request: str, values: tuple = (), return_values_count: int | CursorReturnEnum = CursorReturnEnum.ALL_WRITES):
    cursor.execute(request, values)
    if return_values_count == CursorReturnEnum.ONE_VALUE:
        value = cursor.fetchone()
        if value is None:
            raise NoValueError
        else:
            return value[0]
    elif return_values_count == CursorReturnEnum.ALL_WRITES:
        return list(map(dict_factory, cursor.fetchall()))
    elif return_values_count == CursorReturnEnum.ONE_WRITE:
        value = cursor.fetchone()
        if value is None:
            raise NoValueError
        else:
            return dict_factory(value)
    elif return_values_count == CursorReturnEnum.ALL_FIELDS:
        row_values = cursor.fetchall()
        values = []
        for value in row_values:
            values.append(value[0])
        return values
    else:
        return cursor.fetchmany(return_values_count)


# The same function but in the end makes commit
def request_set(request: str, values: tuple = ()):
    cursor.execute(request, values)
    connection.commit()


# Next you see the basic functions for handing database
def check_table(table: str):
    if request_get(f'''
    SELECT name
    FROM sqlite_master
    WHERE type='table' AND name="{table}"'''):
        return True
    return False


def create_table(table_name: str, columns: tuple = ()):
    request = f'''
    CREATE TABLE `{table_name}` (
    {", ".join(columns)}
    );
    '''
    request_set(request)


def delete_table(table_name: str):
    request_set(f'''
    DROP TABLE {table_name}
''')


def get_field(table: str, field_name: str, key_name: str, key_value):
    return request_get(f'''
    SELECT {field_name}
    FROM {table}
    WHERE {key_name} = ?
    ''', (key_value,), CursorReturnEnum.ONE_VALUE)


def set_field(table: str, field_name: str, value, key_name: str, key_value):
    request_set(f'''
    UPDATE {table}
    SET {field_name} = ?
    WHERE {key_name} = ?
    ''', (value, key_value,))


def get_column(table: str, column_name: str, duplicates: bool = True):
    return [value[column_name] for value in request_get(f'''
    SELECT {"DISTINCT" if not duplicates else ""} {column_name}
    FROM {table}
    ''')]


def get_columns(table: str, *columns_names):
    columns = ', '.join(columns_names)
    return request_get(f'''
    SELECT {columns}
    FROM {table}
    ''')


def get_write(table: str, key_name: str, key_value) -> sqlite3.Row:
    return request_get(f'''
    SELECT *
    FROM {table}
    WHERE {key_name} = ?
    ''', (key_value,), CursorReturnEnum.ONE_WRITE)


def get_last_writes(table: str, row: int):
    return request_get(f'''
    SELECT *
    FROM {table}
    ''', (), row)


def get_all_writes(table: str, order_by: str | None = None) -> sqlite3.Row:
    return request_get(f'''
    SELECT *
    FROM {table}
    {f"ORDER BY {order_by}" if order_by else ""}
    ''', (), CursorReturnEnum.ALL_WRITES)


def get_fields_with_condition(table: str, field_name, key_name: str, key_value):
    return request_get(f'''
    SELECT {field_name}
    FROM {table}
    WHERE {key_name} = ?
    ''', (key_value,), CursorReturnEnum.ALL_FIELDS)


def get_writes_with_condition(table: str, key_name: str, key_value):
    return request_get(f'''
    SELECT *
    FROM {table}
    WHERE {key_name} = ?
    ''', (key_value,), CursorReturnEnum.ALL_WRITES)


def add_write(table: str, values: tuple):
    request_set(f'''
    INSERT INTO {table}
    VALUES (?{", ?" * (len(values)-1)})
    ''', values)


def delete_write(table: str, key_name: str, key_value):
    request_set(f'''
    DELETE FROM {table}
    WHERE {key_name} = ?
    ''', (key_value,))


def check_write(table: str, key_name: str, key_value):
    try:
        if get_write(table, key_name, key_value) is None:
            return False
        return True
    except NoValueError:
        return False


def get_last_rowid():
    return cursor.lastrowid
