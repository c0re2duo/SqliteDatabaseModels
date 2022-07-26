import os

from . import database_handler as db_handler

from .types import Model
from .models import *


def connect_database():
    # print('connect')
    return db_handler.connect_database()


def disconnect_database():
    # print('disconnect')
    db_handler.disconnect_database()


def register_models():
    models_classes_names = [cls.__name__ for cls in Model.__subclasses__()]
    for model_class_name in models_classes_names:
        model_obj = globals()[model_class_name]
        models_classes.append(model_obj)
        model_obj.get_fields()


# Coming soon
def migrate():
    pass


def get_columns(model: Model) -> tuple:
    fields = model.get_fields()
    columns: tuple = ()
    for field in fields:
        columns += (f'{field} {fields[field].get_column_data()}',)
    return columns


# This method calling from ititializing if database file not exist
def regenerate_database():
    # print('regenerate')
    try:
        os.remove('database/database.db')
    except FileNotFoundError:
        pass
    with open('database/database.db', 'w'):
        pass
    connect_database()
    for model in models_classes:
        # print(get_columns(model))
        db_handler.create_table(model.table_name, get_columns(model))
    disconnect_database()


# if __name__ != '__main__':
models_classes = []
register_models()
if not connect_database():
    regenerate_database()
    connect_database()
