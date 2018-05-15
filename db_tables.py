from peewee import Model, SqliteDatabase, CharField, \
    DateTimeField, ForeignKeyField
import dateparser

db = SqliteDatabase('news.db')
default_date = dateparser.parse('1000-01-01')
today = dateparser.parse('today')


class Topic(Model):
    name = CharField(null='')
    url = CharField(null='')
    description = CharField(null='', default='Описание отсутствует')
    last_update_time = DateTimeField(null=today,
                                     default=default_date)

    class Meta:
        database = db


class Document(Model):
    topic = ForeignKeyField(Topic, related_name='documents')
    name = CharField(null='')
    url = CharField(null='')
    last_update_time = DateTimeField(null=today,
                                     default=default_date)
    text = CharField(null='')

    class Meta:
        database = db


class Tag(Model):
    name = CharField(null='')
    document = ForeignKeyField(Document, related_name='tags')

    class Meta:
        database = db

db.create_tables([Topic, Document, Tag])
db.close()
