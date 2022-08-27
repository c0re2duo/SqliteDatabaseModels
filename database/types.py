from abc import abstractmethod
from typing import Type

from . import database_handler as db_handler


# Parent class for all Models
from .exceptions import IdIsAlreadyAdded
from .fields.base_fields import IdField, Field


class Model:
    # table_name is necesarry parameter of all models
    table_name: str = None
    primary_key_field: str | None = None

    # id is IdField by default
    # If you set your IdField in custom model, this IdField don't use
    # key_column is id by default
    # Same, if you set custom IdField, key_column sets your key column

    # key_column: str = 'id'

    @classmethod
    def get_table_fields(cls):
        class_dict = cls.__dict__
        fields: dict[str: Field] = {}

        used_custom_id_field: bool = False
        for field in class_dict:
            if isinstance(class_dict[field], Field):
                fields[field] = class_dict[field]
                if isinstance(class_dict[field], IdField):
                    used_custom_id_field = True

        if not used_custom_id_field:
            if cls.primary_key_field and cls.primary_key_field != 'id':
                fields[cls.primary_key_field].primary_key = True
            else:
                fields = {'id': IdField()} | fields
                if cls.primary_key_field == 'id':
                    raise IdIsAlreadyAdded
        return fields


def extract_field_create_data(model: Type[Model]) -> tuple:
    fields = model.get_table_fields()
    # print(fields)
    field_create_data: tuple = ()
    for field in fields:
        field_create_data += (f'{field} {fields[field].get_field_create_data()}',)
    # print(field_create_data)
    return field_create_data


class StaticModel(Model):
    # methods for simple handing database
    @classmethod
    def get_write(cls, key_id: int):
        return db_handler.get_write(cls.table_name, cls.primary_key_field, key_id)

    @classmethod
    def get_key(cls, key_name: str, key_value):
        return db_handler.get_field(cls.table_name, cls.primary_key_field, key_name, key_value)

    @classmethod
    def get_field(cls, key_value, field_name):
        return db_handler.get_field(cls.table_name, field_name, cls.primary_key_field, key_value)

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
    def get_writes_with_condition(cls, key_name: str, key_value):
        return db_handler.get_writes_with_condition(cls.table_name, key_name, key_value)

    @classmethod
    def add_write(cls, *values):
        if cls.primary_key_field == 'id':
            db_handler.add_write(cls.table_name, (None,) + values)
        else:
            db_handler.add_write(cls.table_name, values)

    @classmethod
    def set_field(cls, key, field_name: str, value):
        db_handler.set_field(cls.table_name, field_name, value, cls.primary_key_field, key)

    @classmethod
    def delete_write(cls, key):
        db_handler.delete_write(cls.table_name, cls.primary_key_field, key)

    @classmethod
    def check_write(cls, key_value):
        return db_handler.check_write(cls.table_name, cls.primary_key_field, key_value)


class DynamicModel(Model):
    @classmethod
    def get_table_name(cls, table_param: str | int):
        return cls.table_name.format(table_param)

    @classmethod
    def create(cls, table_param: str | int):
        columns = extract_field_create_data(cls)
        db_handler.create_table(cls.get_table_name(table_param), columns)

    @classmethod
    def get_write(cls, table_param: str | int, key_id: int):
        return db_handler.get_write(cls.get_table_name(table_param), cls.primary_key_field, key_id)

    @classmethod
    def get_key(cls, table_param: str | int, key_name: str, key_value):
        return db_handler.get_field(cls.get_table_name(table_param), cls.primary_key_field, key_name, key_value)

    @classmethod
    def get_field(cls, table_param: str | int, key_value, field_name):
        return db_handler.get_field(cls.get_table_name(table_param), field_name, cls.primary_key_field, key_value)

    @classmethod
    def get_all_writes(cls, table_param: str | int, order_by: str | None = None):
        return db_handler.get_all_writes(cls.get_table_name(table_param), order_by)

    @classmethod
    def get_last_writes(cls, table_param: str | int, row):
        return db_handler.get_last_writes(cls.get_table_name(table_param), row)

    @classmethod
    def get_column(cls, table_param: str | int, field: str, duplicates: bool = True):
        return db_handler.get_column(cls.get_table_name(table_param), field, duplicates)

    @classmethod
    def get_columns(cls, table_param: str | int, *columns_names):
        return db_handler.get_columns(cls.get_table_name(table_param), *columns_names)

    @classmethod
    def get_writes_with_condition(cls, table_param: str | int, key_name: str, key_value):
        return db_handler.get_writes_with_condition(cls.get_table_name(table_param), key_name, key_value)

    @classmethod
    def get_fields_with_condition(cls, table_param: str | int, field_name: str, key_name: str, key_value):
        return db_handler.get_fields_with_condition(cls.get_table_name(table_param), field_name, key_name, key_value)

    @classmethod
    def add_write(cls, table_param: str | int, *values):
        if cls.primary_key_field == 'id':
            db_handler.add_write(cls.get_table_name(table_param), (None,) + values)
        else:
            db_handler.add_write(cls.get_table_name(table_param), values)

    @classmethod
    def set_field(cls, table_param: str | int, key, field_name: str, value):
        db_handler.set_field(cls.get_table_name(table_param), field_name, value, cls.primary_key_field, key)

    @classmethod
    def delete_write(cls, table_param: str | int, key):
        db_handler.delete_write(cls.get_table_name(table_param), cls.primary_key_field, key)

    @classmethod
    def check_write(cls, table_param: str | int, key_value):
        return db_handler.check_write(cls.get_table_name(table_param), cls.primary_key_field, key_value)

    @classmethod
    def drop(cls, table_param: str | int):
        db_handler.delete_table(cls.get_table_name(table_param))
