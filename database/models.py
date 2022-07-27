from database.types import Model, TitleColumn, TextColumn, CountColumn, ImageColumn, IdColumn, StaticModel, DynamicModel


# Simple custom model like in Django
class Shop(StaticModel):
    table_name = 'shops'

    asda_id = IdColumn()
    name = TitleColumn()
    desc = TextColumn()


class Category(DynamicModel):
    table_name = "products_in_category_{}"

    # category_id = IdColumn()
    name = TitleColumn()
    count = CountColumn()
