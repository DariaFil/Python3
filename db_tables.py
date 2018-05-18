from peewee import Model, SqliteDatabase, CharField, \
    DateTimeField, ForeignKeyField
import dateparser

# Соединение с базой данных, назначение дефолтных дат

db = SqliteDatabase('news.db')
# База данных новостей
today = dateparser.parse('today')
# Дефолтная текущая дата


class Topic(Model):
    """
    Таблица тем
    Поля: название темы
          адрес темы
          описание темы
          последнее время обновления темы
    """
    name = CharField(null='')
    url = CharField(null='')
    description = CharField(null='', default='Описание отсутствует')
    last_update_time = DateTimeField(null='')

    class Meta:
        database = db


class Document(Model):
    """
    Таблица статей
    Поля: тема, к которой относится статья
          название статьи
          адрес статьи
          последнее время обновления статьи
          текст статьи
    """
    topic = ForeignKeyField(Topic, related_name='documents')
    name = CharField(null='')
    url = CharField(null='')
    last_update_time = DateTimeField(null=today)
    text = CharField(null='')

    class Meta:
        database = db


class Tag(Model):
    """
    Таблица связи стати и тэга
    Поля: название тэга
          статья, к которой он был прикреплён
    """
    name = CharField(null='')
    document = ForeignKeyField(Document, related_name='tags')

    class Meta:
        database = db

db.create_tables([Topic, Document, Tag])
db.close()
