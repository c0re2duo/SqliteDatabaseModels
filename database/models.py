from database.types import Model, TitleField, TextField, CountField, ImageField, IdField


# Simple custom model like in Django
class Product(Model):
    # table_name is important variable
    table_name = 'users'

    # fields
    user_id = IdField()
    name = TitleField(text_size=32)
    description = TextField()
