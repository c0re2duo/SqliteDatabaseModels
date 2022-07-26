from . import database_handler as db_handler


# DatabaseField parent class
# In daught class you need to setting get_column_data for get right data for generate table
class DatabaseField:
    def get_column_data(self) -> str:
        pass


# Class extends DatabaseField
class IdField(DatabaseField):
    def get_column_data(self):
        return 'INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT'


class TitleField(DatabaseField):
    # You can set custom settings for Field
    def __init__(self, text_size=32):
        self.text_size = text_size

    def get_column_data(self):
        return f'VARCHAR ({self.text_size}) NOT NULL'


class TextField(DatabaseField):
    def get_column_data(self):
        return f'VARCHAR (1000) NOT NULL'


class CountField(DatabaseField):
    def get_column_data(self):
        return f'INTEGER'


class BoolField(DatabaseField):
    def get_column_data(self):
        return f'BOOL NOT NULL'


class ImageField(DatabaseField):
    text_size = 16

    def get_column_data(self):
        return f'VARCHAR ({self.text_size}) NOT NULL'


class DateField(DatabaseField):
    def get_column_data(self):
        return f'DATETIME NOT NULL'


# Parent class for all Models
class Model:
    # def __init__(self, **values: dict):
    #     for value in values:
    #         self.values[value] = values[value]

    table_name: str = None

    # id is IdField by default
    # If you set your IdField in custom model, this IdField don't use
    id = IdField()
    # key_column is id by default
    # Same, if you set custom IdField, key_column sets your key column
    key_column: str = 'id'

    @classmethod
    def get_fields(cls):
        class_dict = Model.__dict__ | cls.__dict__
        fields: dict[str: DatabaseField] = {}
        for field in class_dict:
            if isinstance(class_dict[field], DatabaseField):
                if isinstance(class_dict[field], IdField) and 'id' in fields:
                    fields.pop('id')
                    cls.key_column = field
                fields[field] = class_dict[field]
        return fields

    # Next you see a default class methods for get data from database
    @classmethod
    def get_write(cls, key_id: int):
        return db_handler.get_write(cls.table_name, cls.key_column, key_id)

    @classmethod
    def get_spec_write(cls, key_name: str, key_value):
        return db_handler.get_write(cls.table_name, key_name, key_value)

    @classmethod
    def get_field(cls, key_value, field_name):
        return db_handler.get_field(cls.table_name, field_name, cls.key_column, key_value)

    @classmethod
    def get_spec_field(cls, field_name: str, key_name: str, key_value):
        return db_handler.get_field(cls.table_name, field_name, key_name, key_value)

    @classmethod
    def get_all_writes(cls):
        return db_handler.get_all_writes(cls.table_name)

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
    def set_spec_field(cls, key_name: str, key_value, field_name: str, value):
        db_handler.set_field(cls.table_name, field_name, value, key_name, key_value)

    @classmethod
    def delete_write(cls, key):
        db_handler.delete_write(cls.table_name, cls.key_column, key)

    @classmethod
    def delete_spec_write(cls, key_name, key):
        db_handler.delete_write(cls.table_name, key_name, key)

    @classmethod
    def check_write(cls, key_value):
        return db_handler.check_write(cls.table_name, cls.key_column, key_value)
