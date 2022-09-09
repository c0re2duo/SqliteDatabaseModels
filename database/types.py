from abc import abstractmethod
from enum import Enum
from typing import Type

from . import database_handler as db_handler


# Parent class for all Models
from .exceptions import IdIsAlreadyAdded
from .fields.base_fields import IdField, Field, FilterReturnValues, FilterValueError


class Model:
    # table_name is necesarry parameter of all models
    table_name: str = None
    primary_key_field: str | None = 'id'
    fields: dict[str: Field] = {}
    # field_classes = {'title': Sma}

    # id is IdField by default
    # If you set your IdField in custom model, this IdField don't use
    # key_column is id by default
    # Same, if you set custom IdField, key_column sets your key column

    # key_column: str = 'id'

    @classmethod
    def skip_through_get_filter(cls, values: dict):
        for field_name in values:
            filtered_value = cls.fields[field_name].filter_data_from_db(values[field_name])
            match filtered_value:
                case FilterReturnValues.NOT_CHANGED:
                    pass
                case FilterReturnValues.VALUE_ERROR:
                    raise FilterValueError
                case _:
                    values[field_name] = filtered_value
        return values

    @classmethod
    def register_fields(cls):
        class_dict = cls.__dict__
        # print(cls)
        # print(cls.fields)
        cls.fields = {}
        used_custom_id_field: bool = False
        for field in class_dict:
            if isinstance(class_dict[field], Field):
                cls.fields[field] = class_dict[field]
                if isinstance(class_dict[field], IdField):
                    used_custom_id_field = True
        # print(cls.fields)

        if not used_custom_id_field:
            if cls.primary_key_field and cls.primary_key_field != 'id':
                cls.fields[cls.primary_key_field].primary_key = True
            else:
                cls.fields = {'id': IdField()} | cls.fields
                # if cls.primary_key_field == 'id':
                #     raise IdIsAlreadyAdded

        # print('load_fields ', cls.fields)
        # return fields


def extract_field_create_data(model: Type[Model]) -> tuple:
    # print('fields:', model.fields)
    fields = model.fields
    field_create_data: tuple = ()
    for field in fields:
        field_create_data += (f'{field} {fields[field].get_field_create_data()}',)
    # print(field_create_data)
    return field_create_data


class StaticModel(Model):
    # methods for simple handing database
    @classmethod
    def get_write(cls, key_id: int):
        # fields_names = list(cls.fields)
        database_values = db_handler.get_write(cls.table_name, cls.primary_key_field, key_id)
        # filtered_values = {}
        # for database_value in database_values:
        #     # print(fields_names[list(database_values).index(database_value)])
        #     filtered_values[database_value] = (cls.skip_through_get_filter(database_values[database_value], fields_names[list(database_values).index(database_value)]))
        # return filtered_values
        return cls.skip_through_get_filter(database_values)

    @classmethod
    def get_key(cls, key_name: str, key_value):
        return db_handler.get_field(cls.table_name, cls.primary_key_field, key_name, key_value)

    @classmethod
    def get_field(cls, key_value, field_name: str):
        return cls.skip_through_get_filter({field_name: db_handler.get_field(cls.table_name, field_name, cls.primary_key_field, key_value)})[field_name]

    @classmethod
    def get_all_writes(cls, order_by: str | None = None):
        # print(cls.fields)
        database_values = db_handler.get_all_writes(cls.table_name, order_by)
        for database_value in database_values:
            database_value = cls.skip_through_get_filter(database_value)
        return database_values

    @classmethod
    def get_last_writes(cls, row=1):
        database_values = db_handler.get_last_writes(cls.table_name, row)
        for database_value in database_values:
            database_value = cls.skip_through_get_filter(database_value)
        return database_values

    @classmethod
    def get_column(cls, field_name: str, duplicates: bool = True):
        database_values = db_handler.get_column(cls.table_name, field_name, duplicates)
        for index in range(len(database_values)):
            database_values[index] = cls.skip_through_get_filter({field_name: database_values[index]})[field_name]
        return database_values

    # @classmethod
    # def get_columns(cls, *columns_names):
    #     return db_handler.get_columns(cls.table_name, *columns_names)

    @classmethod
    def get_writes_with_condition(cls, key_name: str, key_value):
        database_values = db_handler.get_writes_with_condition(cls.table_name, key_name, key_value)
        for database_value in database_values:
            database_value = cls.skip_through_get_filter(database_value)
        return database_values

    @classmethod
    def get_fields_with_condition(cls, field_name: str, key_name: str, key_value):
        return cls.skip_through_get_filter({field_name: db_handler.get_fields_with_condition(cls.table_name, field_name, key_name, key_value)})[field_name]

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
        # print(columns)
        db_handler.create_table(cls.get_table_name(table_param), columns)

    @classmethod
    def get_write(cls, table_param: str | int, key_id: int):
        database_values = db_handler.get_write(cls.get_table_name(table_param), cls.primary_key_field, key_id)
        return cls.skip_through_get_filter(database_values)

    @classmethod
    def get_key(cls, table_param: str | int, key_name: str, key_value):
        return db_handler.get_field(cls.get_table_name(table_param), cls.primary_key_field, key_name, key_value)

    @classmethod
    def get_field(cls, table_param: str | int, key_value, field_name):
        database_value = db_handler.get_field(cls.get_table_name(table_param), field_name, cls.primary_key_field, key_value)
        return cls.skip_through_get_filter({field_name: database_value})[field_name]

    @classmethod
    def get_all_writes(cls, table_param: str | int, order_by: str | None = None):
        database_values = db_handler.get_all_writes(cls.get_table_name(table_param), order_by)
        for database_value in database_values:
            database_value = cls.skip_through_get_filter(database_value)
        return database_values

    @classmethod
    def get_last_writes(cls, table_param: str | int, row=1):
        database_values = db_handler.get_last_writes(cls.get_table_name(table_param), row)
        for database_value in database_values:
            database_value = cls.skip_through_get_filter(database_value)
        return database_values

    @classmethod
    def get_column(cls, table_param: str | int, field_name: str, duplicates: bool = True):
        database_values = db_handler.get_column(cls.get_table_name(table_param), field_name, duplicates)
        for index in range(len(database_values)):
            database_values[index] = cls.skip_through_get_filter({field_name: database_values[index]})[field_name]
        return database_values

    # @classmethod
    # def get_columns(cls, table_param: str | int, *columns_names):
    #     return db_handler.get_columns(cls.get_table_name(table_param), *columns_names)

    @classmethod
    def get_writes_with_condition(cls, table_param: str | int, key_name: str, key_value):
        database_values = db_handler.get_writes_with_condition(cls.get_table_name(table_param), key_name, key_value)
        for database_value in database_values:
            database_value = cls.skip_through_get_filter(database_value)
        return database_values

    @classmethod
    def get_fields_with_condition(cls, table_param: str | int, field_name: str, key_name: str, key_value):
        return cls.skip_through_get_filter(
            {field_name: db_handler.get_fields_with_condition(cls.get_table_name(table_param), field_name, key_name, key_value)})[
            field_name]

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
