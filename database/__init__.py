import os

from . import database_handler as db_handler

from .types import Model, extract_field_create_data, DynamicModel
from .models import *


static_models_classes = []
dynamic_models_classes = []


def connect_database():
    # print('connect')
    return db_handler.connect_database()


def disconnect_database():
    # print('disconnect')
    db_handler.disconnect_database()


def register_models():
    static_models_classes_names = [cls.__name__ for cls in StaticModel.__subclasses__()]
    dynamic_models_classes_names = [cls.__name__ for cls in DynamicModel.__subclasses__()]
    for model_class_name in static_models_classes_names + dynamic_models_classes_names:
        # print(model_class_name)
        model_class = globals()[model_class_name]
        model_class.register_fields()
        if model_class_name in static_models_classes_names:
            static_models_classes.append(model_class)
        elif model_class_name in dynamic_models_classes_names:
            dynamic_models_classes.append(model_class)


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
    for model in static_models_classes:
        db_handler.create_table(model.table_name, extract_field_create_data(model))
    disconnect_database()


def start_database():
    register_models()
    if not connect_database():
        regenerate_database()
        connect_database()
