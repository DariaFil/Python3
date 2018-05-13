from telebot import TeleBot
import re
import db_commands


class User:
    def __init__(self, id):
        self.id = id
        self.status = 'start'


users = dict()
bot = TeleBot('521302347:AAFWdv5Udnk8Iz6_SvaoyoIscwwinvJd1qk')


def set_user(id):
    if id not in users:
        users[id] = User(id)


@bot.message_handler(commands=['start'])
def handle_start(message):
    set_user(message.chat.id)
    print(message.text, message.chat.first_name, message.chat.last_name)
    bot.send_message(message.chat.id, "Привет! Я новостной бот \
            и готов показать свежие новости. \
            Чтобы прочесть список команд, введите /help")
    users[message.chat.id].status = 'start'


@bot.message_handler(commands=['help'])
def handle_help(message):
    set_user(message.chat.id)
    print(message.text, message.chat.first_name, message.chat.last_name)
    bot.send_message(message.chat.id, "/help - список команд\n \
             /start - начать общение с ботом\n \
             /new_docs - показать последние новости\n \
             /new_topics - показать последние обновившиеся темы\n \
             /topic - показать описание темы\n \
             /doc - показать текст статьи \n \
             /words - показать главные слова темы\n \
             /describe_doc - показать статистику по документу\n \
             /describe_topic - показать статистику по теме")
    users[message.chat.id].status = 'start'


@bot.message_handler(commands=['new_docs'])
def new_docs(message):
    set_user(message.chat.id)
    print(message.text, message.chat.first_name, message.chat.last_name)
    users[message.chat.id].status = 'new_docs'
    bot.send_message(message.chat.id, 'Сколько?')


@bot.message_handler(commands=['new_topics'])
def new_topics(message):
    set_user(message.chat.id)
    print(message.text, message.chat.first_name, message.chat.last_name)
    users[message.chat.id].status = 'new_topics'
    bot.send_message(message.chat.id, 'Сколько?')


@bot.message_handler(commands=['topic'])
def topic(message):
    set_user(message.chat.id)
    print(message.text, message.chat.first_name, message.chat.last_name)
    users[message.chat.id].status = 'topic'
    bot.send_message(message.chat.id, 'Введите заголовок темы')


@bot.message_handler(commands=['doc'])
def doc(message):
    set_user(message.chat.id)
    print(message.text, message.chat.first_name, message.chat.last_name)
    users[message.chat.id].status = 'doc'
    bot.send_message(message.chat.id, 'Введите заголовок статьи')


@bot.message_handler(commands=['words'])
def words(message):
    set_user(message.chat.id)
    print(message.text, message.chat.first_name, message.chat.last_name)
    users[message.chat.id].status = 'words'
    bot.send_message(message.chat.id, 'Введите заголовок темы')


@bot.message_handler(commands=['describe_doc'])
def describe_doc(message):
    set_user(message.chat.id)
    print(message.text, message.chat.first_name, message.chat.last_name)
    users[message.chat.id].status = 'describe_doc'
    bot.send_message(message.chat.id, 'Введите заголовок статьи')


@bot.message_handler(commands=['describe_topic'])
def describe_topic(message):
    set_user(message.chat.id)
    print(message.text, message.chat.first_name, message.chat.last_name)
    users[message.chat.id].status = 'describe_topic'
    bot.send_message(message.chat.id, 'Введите заголовок темы')


@bot.message_handler(content_types=['text'])
def get_message(message):
    set_user(message.chat.id)
    print(message.text, message.chat.first_name, message.chat.last_name)
    if users[message.chat.id].status == 'start':
        bot.send_message(message.chat.id, 'Введите команду')
    if users[message.chat.id].status == 'topic':
        topic_name = message.text
        topic = db_commands.search_topic(topic_name)
        if topic is None:
            bot.send_message(message.chat.id, 'Тема отсутствует в моей базе данных')
        else:
            bot.send_message(message.chat.id, topic.description)
            docs_list = db_commands.search_last_topic_docs(topic.name)
            index = 1
            for doc in docs_list:
                bot.send_message(message.chat.id, str(index) + '. ' + doc.name + '\n' + doc.url)
                index += 1
        users[message.chat.id].status = 'start'
    if users[message.chat.id].status == 'doc':
        doc_name = message.text
        doc = db_commands.search_doc(doc_name)
        if doc is None:
            bot.send_message(message.chat.id, 'Статья отсутствует в моей базе данных')
        else:
            bot.send_message(message.chat.id, doc.text)
            users[message.chat.id].status = 'start'
    if users[message.chat.id].status == 'new_docs':
        user_text = message.text
        try:
            number = int(user_text)
        except ValueError:
            bot.send_message(message.chat.id, 'Неверный номер')
        else:
            if number < 1:
                bot.send_message(message.chat.id, 'Неверный номер')
            else:
                docs = db_commands.search_last_docs(number)
                index = 1
                for doc in docs:
                    bot.send_message(message.chat.id, str(index) + '. ' + doc.name + '\n' + doc.url)
                    index += 1
        finally:
            users[message.chat.id].status = 'start'
    if users[message.chat.id].status == 'new_topics':
        user_text = message.text
        try:
            number = int(user_text)
        except ValueError:
            bot.send_message(message.chat.id, 'Неверный номер')
        else:
            if number < 1:
                bot.send_message(message.chat.id, 'Неверный номер')
            else:
                topics = db_commands.search_last_topic(number)
                index = 1
                for topic in topics:
                    bot.send_message(message.chat.id, str(index) + '. ' + topic.name + '\n' +
                                     topic.description + '\n' + topic.url)
                    index += 1
        finally:
            users[message.chat.id].status = 'start'
    if users[message.chat.id].status == 'words':
        topic_name = message.text
        topic = db_commands.search_topic(topic_name)
        if topic is not None:
            tags = db_commands.search_topic_tags(topic)
            for tag in tags:
                bot.send_message(message.chat.id, tag)
        else:
            bot.send_message(message.chat.id, 'Тема отсутствует в моей базе данных')
        users[message.chat.id].status = 'start'
    if users[message.chat.id].status == 'describe_doc':
        doc_name = message.text
        doc = db_commands.search_doc(doc_name)
        if doc is not None:
            word_statistics = db_commands.doc_word_statistics(doc)
            length_statistics = db_commands.length_statistics(word_statistics)
            files = db_commands.word_stat_plot('doc' + str(message.chat.id),
                                               word_statistics, length_statistics)
            with open(files[0], 'rb') as plot1:
                bot.send_photo(message.chat.id, plot1)
            with open(files[1], 'rb') as plot1:
                bot.send_photo(message.chat.id, plot1)
        else:
            bot.send_message(message.chat.id, 'Статья отсутствует в моей базе данных')
        users[message.chat.id].status = 'start'
    if users[message.chat.id].status == 'describe_topic':
        topic_name = message.text
        topic = db_commands.search_topic(topic_name)
        if topic is not None:
            doc_count = 0
            docs_len = 0
            for doc in topic.documents:
                doc_count += 1
                docs_len += len(re.findall(r'\w+', doc.text))
            avg_doc_len = docs_len / doc_count
            bot.send_message(message.chat.id, 'Количество статей по данной теме в базе: ' + str(doc_count))
            bot.send_message(message.chat.id, 'Средняя длина документа: ' + str(avg_doc_len) + ' слов')
            word_statistics = db_commands.topic_statistics(topic)
            length_statistics = db_commands.length_statistics(word_statistics)
            files = db_commands.word_stat_plot('topic' + str(message.chat.id),
                                               word_statistics, length_statistics)
            with open(files[0], 'rb') as plot1:
                bot.send_photo(message.chat.id, plot1)
            with open(files[1], 'rb') as plot1:
                bot.send_photo(message.chat.id, plot1)
        else:
            bot.send_message(message.chat.id, 'Тема отсутствует в моей базе данных')
        users[message.chat.id].status = 'start'

if __name__ == '__main__':
    bot.polling(none_stop=True)
