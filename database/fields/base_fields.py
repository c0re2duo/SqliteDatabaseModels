
# DatabaseField parent class
# In child class you need to setting field_create_data for get right data in generate table
class Field:
    primary_key: bool = False
    field_create_date: str = ''

    def get_field_create_data(self) -> str:
        if self.primary_key:
            self.field_create_date += ' PRIMARY KEY AUTOINCREMENT'
        return self.field_create_date


# Class extends Field
class IdField(Field):
    primary_key = True
    field_create_date = 'INTEGER NOT NULL'


class SmallTextField(Field):
    # You can set custom settings for Field
    field_create_date = 'VARCHAR (?1?) NOT NULL'

    def __init__(self, max_text_len=32):
        self.max_text_len = max_text_len
        self.field_create_date = self.field_create_date.replace('?1?', str(self.max_text_len))


class BigTextField(Field):
    field_create_date = 'VARCHAR (1000) NOT NULL'


class IntegerField(Field):
    field_create_date = 'INTEGER'


class BoolField(Field):
    field_create_date = 'BOOL NOT NULL'


class DateTimeField(Field):
    field_create_date = 'DATETIME NOT NULL'
