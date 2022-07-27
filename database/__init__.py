import os

from . import database_handler as db_handler

from .types import Model, extract_column_data
from .models import *


def connect_database():
    # print('connect')
    return db_handler.connect_database()


def disconnect_database():
    # print('disconnect')
    db_handler.disconnect_database()


def register_models():
    static_models_classes_names = [cls.__name__ for cls in StaticModel.__subclasses__()]
    dynamic_models_classes_names = [cls.__name__ for cls in DynamicModel.__subclasses__()]
    for model_class_name in static_models_classes_names:
        model_class = globals()[model_class_name]
        models_classes.append(model_class)
        model_class.get_table_columns()
    for model_class_name in dynamic_models_classes_names:
        model_class = globals()[model_class_name]
        model_class.get_table_columns()


# Coming soon
def migrate():
    pass


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
        db_handler.create_table(model.table_name, extract_column_data(model))
    disconnect_database()


# if __name__ != '__main__':
models_classes = []
register_models()
if not connect_database():
    regenerate_database()
    connect_database()
