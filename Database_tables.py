from peewee import Model, SqliteDatabase, CharField, \
    DateTimeField, ForeignKeyField

db = SqliteDatabase('news.db')


class Topic(Model):
    name = CharField()
    url = CharField()
    description = CharField()
    last_update_time = DateTimeField()

    class Meta:
        database = db


class Document(Model):
    topic = ForeignKeyField(Topic, related_name='documents')
    name = CharField()
    url = CharField()
    last_update_time = DateTimeField()
    text = CharField()

    class Meta:
        database = db


class Tag(Model):
    name = CharField()
    document = ForeignKeyField(Document, related_name='tags')

    class Meta:
        database = db

db.create_tables([Topic, Document, Tag])
db.close()
