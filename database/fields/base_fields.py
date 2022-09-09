import datetime
from enum import Enum


class FilterReturnValues(Enum):
    NOT_CHANGED = 0
    VALUE_ERROR = 1


class FilterValueError(Exception):
    def __str__(self):
        return 'An error occurred during the filter operation, possibly the data in the database is corrupted'


# DatabaseField parent class
# In child class you need to setting field_create_data for get right data in generate table
class Field:
    primary_key: bool = False
    field_create_date: str = ''

    def get_field_create_data(self) -> str:
        if self.primary_key:
            self.field_create_date += ' PRIMARY KEY AUTOINCREMENT'
        return self.field_create_date

    @staticmethod
    def filter_data_from_db(database_value):
        # NOT CHANGED means this filter don't change value from database
        return FilterReturnValues.NOT_CHANGED


# Class extends Field
class IdField(Field):
    primary_key = True
    field_create_date = 'INTEGER NOT NULL'


class SmallTextField(Field):
    # You can set custom settings for Field
    field_create_date = 'VARCHAR ({}) NOT NULL'

    def __init__(self, max_text_len=32):
        self.max_text_len = max_text_len
        self.field_create_date = self.field_create_date.format(str(self.max_text_len))


class BigTextField(Field):
    field_create_date = 'VARCHAR (1000) NOT NULL'


class IntegerField(Field):
    field_create_date = 'INTEGER'


class BoolField(Field):
    field_create_date = 'BOOL NOT NULL'


class DateTimeField(Field):
    field_create_date = 'DATETIME NOT NULL'

    @staticmethod
    def filter_data_from_db(database_value: str):
        try:
            date, time = database_value.split(' ')
            year, month, day = map(int, date.split('-'))
            hour, minute, seconds = time.split(':')
            hour, minute = map(int, (hour, minute))
            second = int(float(seconds))
            microsecond = int((float(seconds) % 1) * 1000000)
        except:
            return FilterReturnValues.VALUE_ERROR

        return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second, microsecond=microsecond)
