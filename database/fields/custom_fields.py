from database.fields.base_fields import Field


class ImageColumn(Field):
    text_size = 16

    def get_column_data(self):
        return f'VARCHAR ({self.text_size}) NOT NULL'
