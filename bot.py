from telebot import TeleBot
import bot_commands
import re

default_new_number = '5'
users = dict()
bot = TeleBot('521302347:AAFWdv5Udnk8Iz6_SvaoyoIscwwinvJd1qk')


class User:
    def __init__(self, user_id):
        self.id = user_id
        self.action = 'start'


def set_user(user_id):
    if user_id not in users:
        users[user_id] = User(user_id)


def do_command(message, user_text):
    if users[message.chat.id].action == 'start':
        bot.send_message(message.chat.id,
                         'Введите команду')
    if users[message.chat.id].action == 'doc':
        doc_name = message.text
        doc_text = bot_commands.doc(doc_name)
        if doc_text is None:
            bot.send_message(message.chat.id,
                             'Статья отсутствует в моей базе данных')
        else:
            bot.send_message(message.chat.id, doc_text)
    if users[message.chat.id].action == 'topic':
        description, docs_list = bot_commands.topic(user_text)
        if description is None:
            bot.send_message(message.chat.id,
                             'Тема отсутствует в моей базе данных')
        else:
            bot.send_message(message.chat.id, description)
            for current_doc in docs_list:
                bot.send_message(message.chat.id, current_doc)
    if users[message.chat.id].action == 'new_docs':
        docs_list = bot_commands.new_docs(user_text)
        if docs_list is None:
            bot.send_message(message.chat.id,
                             'Статья отсутствует в моей базе данных')
        else:
            for current_doc in docs_list:
                bot.send_message(message.chat.id, current_doc)
    if users[message.chat.id].action == 'new_topics':
        topics_list = bot_commands.new_topics(user_text)
        if topics_list is None:
            bot.send_message(message.chat.id,
                             'Тема отсутствует в моей базе данных')
        else:
            for current_topic in topics_list:
                bot.send_message(message.chat.id, current_topic)
    if users[message.chat.id].action == 'words':
        tags_list = bot_commands.tags(user_text)
        if tags_list is not None:
            for tag in tags_list:
                bot.send_message(message.chat.id, tag)
        else:
            bot.send_message(message.chat.id,
                             'Тема отсутствует в моей базе данных')
    if users[message.chat.id].action == 'describe_doc':
        doc_info = bot_commands.describe_doc(user_text, message.chat.id)
        if doc_info is not None:
            with open(doc_info[0], 'rb') as plot1:
                bot.send_photo(message.chat.id, plot1)
            with open(doc_info[1], 'rb') as plot1:
                bot.send_photo(message.chat.id, plot1)
        else:
            bot.send_message(message.chat.id,
                             'Статья отсутствует в моей базе данных')
    if users[message.chat.id].action == 'describe_topic':
        topic_info = bot_commands.describe_topic(user_text, message.chat.id)
        if topic_info is not None:
            bot.send_message(message.chat.id,
                             'Количество статей по данной теме в базе: '
                             + str(topic_info[0]))
            bot.send_message(message.chat.id,
                             'Средняя длина документа: '
                             + str(topic_info[1]) + ' слов')
            with open(topic_info[2][0], 'rb') as plot1:
                bot.send_photo(message.chat.id, plot1)
            with open(topic_info[2][1], 'rb') as plot1:
                bot.send_photo(message.chat.id, plot1)
        else:
            bot.send_message(message.chat.id,
                             'Тема отсутствует в моей базе данных')


@bot.message_handler(commands=['start', 'help',
                               'topic', 'doc', 'words',
                               'new_docs', 'new_topics',
                               'describe_topic', 'describe_doc'],
                     content_types=['text'])
def get_command(message):
    set_user(message.chat.id)
    user_command = re.findall(r'\w+', message.text)[0]
    user_text = message.text.replace('/' + user_command, '').strip()
    print(user_command, user_text, message.chat.first_name, message.chat.last_name)
    users[message.chat.id].action = user_command
    if user_text == '':
        users[message.chat.id].action = user_command
        if user_command == 'start':
            bot.send_message(message.chat.id,
                             '''Привет! Я новостной бот
                             и готов показать свежие новости.
                             Чтобы прочесть список команд, введите /help''')
        elif user_command == 'help':
            bot.send_message(message.chat.id,
                             '''/help - список команд
                                /start - начать общение с ботом
                                /new_docs - показать последние новости.
                                Параметр - количество статей.
                                По умолчанию выводится 5 самых новых статей
                                /new_topics - показать последние обновлённые темы.
                                Параметр - количество тем.
                                По умолчанию выводится 5 самых новых тем
                                /topic - показать описание темы.
                                Параметр - название темы
                                /doc - показать текст статьи.
                                Параметр - название статьи
                                /words - показать главные слова темы.
                                Параметр - название темы
                                /describe_topic - показать статистику по теме
                                Параметр - название темы
                                /describe_doc - показать статистику по статье.
                                Параметр - название статьи''')
        elif user_command == 'new_topics' or user_command == 'new_docs':
            message.text = default_new_number
            get_message(message)
        else:
            bot.send_message(message.chat.id, 'Введите параметр команды')
    else:
        do_command(message, user_text)
        users[message.chat.id].action = 'start'


@bot.message_handler(content_types=['text'])
def get_message(message):
    set_user(message.chat.id)
    user_text = message.text
    print(user_text, message.chat.first_name, message.chat.last_name)
    do_command(message, user_text)
    users[message.chat.id].action = 'start'

if __name__ == '__main__':
    bot.polling(none_stop=True)
