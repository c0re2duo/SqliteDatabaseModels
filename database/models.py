from database.types import Model, TitleColumn, TextColumn, CountColumn, ImageColumn, IdColumn, StaticModel, DynamicModel


# Simple custom model like in Django
# If there is no IdField column, script automatically creates IdField id
class Shop(StaticModel):
    table_name = 'shops'

    name = TitleColumn()
    desc = TextColumn()


class Category(DynamicModel):
    table_name = "products_in_category_{}"

    # There are custom id column, that id will not create
    some_other_id = IdColumn()
    name = TitleColumn()
    some_count = CountColumn()
