from abc import abstractmethod
from typing import Type

from . import database_handler as db_handler


# DatabaseField parent class
# In daught class you need to setting get_column_data for get right data for generate table
class Column:
    def get_column_data(self) -> str:
        pass


# Class extends DatabaseField
class IdColumn(Column):
    def get_column_data(self):
        return 'INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT'


class TitleColumn(Column):
    # You can set custom settings for Field
    def __init__(self, text_size=32):
        self.text_size = text_size

    def get_column_data(self):
        return f'VARCHAR ({self.text_size}) NOT NULL'


class TextColumn(Column):
    def get_column_data(self):
        return f'VARCHAR (1000) NOT NULL'


class CountColumn(Column):
    def get_column_data(self):
        return f'INTEGER'


class BoolColumn(Column):
    def get_column_data(self):
        return f'BOOL NOT NULL'


class ImageColumn(Column):
    text_size = 16

    def get_column_data(self):
        return f'VARCHAR ({self.text_size}) NOT NULL'


class DateColumn(Column):
    def get_column_data(self):
        return f'DATETIME NOT NULL'


# Parent class for all Models
class Model:
    table_name: str = None

    # id is IdField by default
    # If you set your IdField in custom model, this IdField don't use
    # key_column is id by default
    # Same, if you set custom IdField, key_column sets your key column
    key_column: str = 'id'

    @classmethod
    def get_table_columns(cls):
        class_dict = cls.__dict__
        columns: dict[str: Column] = {}
        custom_key_column = None
        for column in class_dict:
            if isinstance(class_dict[column], Column):
                columns[column] = class_dict[column]
                if isinstance(class_dict[column], IdColumn):
                    custom_key_column = column
        if custom_key_column:
            cls.key_column = custom_key_column
            columns = {custom_key_column: IdColumn()} | columns
        else:
            columns = {'id': IdColumn()} | columns
        return columns

    # Next you see a default class methods for get data from database
    # @classmethod
    # @abstractmethod
    # def get_write(cls):
    #     pass
    #
    # @classmethod
    # def get_spec_write_key(cls, key_name: str, key_value):
    #     pass
    #
    # @classmethod
    # def get_field(cls, key_value, field_name):
    #     pass
    #
    # @classmethod
    # def get_all_writes(cls, order_by: str | None = None):
    #     pass
    #
    # @classmethod
    # def get_last_writes(cls, row):
    #     pass
    #
    # @classmethod
    # def get_column(cls, field: str, duplicates: bool = True):
    #     pass
    #
    # @classmethod
    # def get_columns(cls, *columns_names):
    #     pass
    #
    # @classmethod
    # def get_writes_with_condition(cls, field_name: str, key_name: str, key_value):
    #     pass
    #
    # @classmethod
    # def add_write(cls, *values):
    #     pass
    #
    # @classmethod
    # def set_field(cls, key, field_name: str, value):
    #     pass
    #
    # @classmethod
    # def delete_write(cls, key):
    #     pass
    #
    # @classmethod
    # def check_write(cls, key_value):
    #     pass


def extract_column_data(model: Type[Model]) -> tuple:
    fields = model.get_table_columns()
    columns: tuple = ()
    for field in fields:
        columns += (f'{field} {fields[field].get_column_data()}',)
    return columns


class StaticModel(Model):
    @classmethod
    def get_write(cls, key_id: int):
        return db_handler.get_write(cls.table_name, cls.key_column, key_id)

    @classmethod
    def get_key(cls, key_name: str, key_value):
        return db_handler.get_field(cls.table_name, cls.key_column, key_name, key_value)

    @classmethod
    def get_field(cls, key_value, field_name):
        return db_handler.get_field(cls.table_name, field_name, cls.key_column, key_value)

    @classmethod
    def get_all_writes(cls, order_by: str | None = None):
        return db_handler.get_all_writes(cls.table_name, order_by)

    @classmethod
    def get_last_writes(cls, row):
        return db_handler.get_last_writes(cls.table_name, row)

    @classmethod
    def get_column(cls, field: str, duplicates: bool = True):
        return db_handler.get_column(cls.table_name, field, duplicates)

    @classmethod
    def get_columns(cls, *columns_names):
        return db_handler.get_columns(cls.table_name, *columns_names)

    @classmethod
    def get_writes_with_condition(cls, field_name: str, key_name: str, key_value):
        return db_handler.get_writes_with_condition(cls.table_name, field_name, key_name, key_value)

    @classmethod
    def add_write(cls, *values):
        if cls.key_column == 'id':
            db_handler.add_write(cls.table_name, (None,) + values)
        else:
            db_handler.add_write(cls.table_name, values)

    @classmethod
    def set_field(cls, key, field_name: str, value):
        db_handler.set_field(cls.table_name, field_name, value, cls.key_column, key)

    @classmethod
    def delete_write(cls, key):
        db_handler.delete_write(cls.table_name, cls.key_column, key)

    @classmethod
    def check_write(cls, key_value):
        return db_handler.check_write(cls.table_name, cls.key_column, key_value)


class DynamicModel(Model):
    @classmethod
    def get_table_name(cls, table_param: str | int):
        return cls.table_name.format(table_param)

    @classmethod
    def create(cls, table_param: str | int):
        columns = extract_column_data(cls)
        db_handler.create_table(cls.get_table_name(table_param), columns)

    # asd
    @classmethod
    def get_write(cls, table_param: str | int, key_id: int):
        return db_handler.get_write(cls.get_table_name(table_param), cls.key_column, key_id)

    @classmethod
    def get_key(cls, key_name: str, key_value):
        return db_handler.get_field(cls.table_name, cls.key_column, key_name, key_value)

    @classmethod
    def get_field(cls, key_value, field_name):
        return db_handler.get_field(cls.table_name, field_name, cls.key_column, key_value)

    @classmethod
    def get_all_writes(cls, order_by: str | None = None):
        return db_handler.get_all_writes(cls.table_name, order_by)

    @classmethod
    def get_last_writes(cls, row):
        return db_handler.get_last_writes(cls.table_name, row)

    @classmethod
    def get_column(cls, field: str, duplicates: bool = True):
        return db_handler.get_column(cls.table_name, field, duplicates)

    @classmethod
    def get_columns(cls, *columns_names):
        return db_handler.get_columns(cls.table_name, *columns_names)

    @classmethod
    def get_writes_with_condition(cls, field_name: str, key_name: str, key_value):
        return db_handler.get_writes_with_condition(cls.table_name, field_name, key_name, key_value)

    @classmethod
    def add_write(cls, *values):
        if cls.key_column == 'id':
            db_handler.add_write(cls.table_name, (None,) + values)
        else:
            db_handler.add_write(cls.table_name, values)

    @classmethod
    def set_field(cls, key, field_name: str, value):
        db_handler.set_field(cls.table_name, field_name, value, cls.key_column, key)

    @classmethod
    def delete_write(cls, key):
        db_handler.delete_write(cls.table_name, cls.key_column, key)

    @classmethod
    def check_write(cls, key_value):
        return db_handler.check_write(cls.table_name, cls.key_column, key_value)
