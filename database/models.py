from database.fields.base_fields import BigTextField, SmallTextField, IntegerField, DateTimeField
from database.types import StaticModel, DynamicModel


# Simple custom static model
# If there is no IdField field, database automatically creates IdField "id"
class Article(StaticModel):
    # set the model table name
    table_name = 'articles'
    # we set custom primary key field
    primary_key_field = 'article_id'

    # fields
    article_id = IntegerField()
    title = SmallTextField(max_text_len=64)
    text = BigTextField()
    likes = IntegerField()
    create_datetime = DateTimeField()


# Simple dynamic model
# class Comment(DynamicModel):
#     # in this table name we use "{}" for indicate place for table parameter
#     table_name = 'commentaries_of_article_{}'
#
#     text = BigTextField()
#     chat_name = SmallTextField(max_text_len=32)
