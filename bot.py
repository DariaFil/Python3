from telebot import TeleBot
import bot_commands
import re

# Установка дефолтных значений и настроек

DEFAULT_NEW_NUMBER = '5'
# Число выводимых последних тем/статей по умолчанию
COMMANDS_LIST = ['start', 'help', 'topic', 'doc', 'words', 'new_docs',
                 'new_topics', 'describe_topic', 'describe_doc']
# Список команд, принимаемых ботом
GREETING = '''Привет! Я новостной бот и готов показать свежие новости.
Чтобы прочесть список команд, введите /help'''
# Приветствие при начале использования бота
HELP_LIST = '''/help - список команд
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
Параметр - название статьи'''
# Справка
DOC_NOT_EXIST = 'Статья отсутствует в моей базе данных'
# Сообщение при отсутствии статьи в базе
TOPIC_NOT_EXIST = 'Тема отсутствует в моей базе данных'
# Сообщение при отсутствии темы в базе
WRONG_NUMBER = 'Некорректно указано число'
# Сообщение при некоректном вводе числа

users = dict()
bot = TeleBot('521302347:AAFWdv5Udnk8Iz6_SvaoyoIscwwinvJd1qk')
# Бот


class User:
    """
    Класс, хранящий идентификатор и
    текущее состояние (последнюю команду) пользователя
    """
    def __init__(self, user_id):
        self.id = user_id
        self.action = 'start'


def set_user(user_id):
    """
    Добавление нового пользователя
    :param user_id: идентификатор пользователя
    """
    if user_id not in users:
        users[user_id] = User(user_id)


def bot_start(chat_id, user_text):
    """
    Функция начала работы бота
    Также вызывается при вводе пользователем текста без команды
    :param chat_id: идентификатор чата
    :param user_text: текст пользователя
    :return: посылает текстовое сообщение
    """
    if user_text == 'Привет':
        bot.send_message(chat_id, 'Рад снова вас видеть')
    else:
        bot.send_message(chat_id, 'Введите команду')


def bot_doc(chat_id, user_text):
    """
    Функция отправки текста статьи
    :param chat_id: идентификатор чата
    :param user_text: текст пользователя
    :return: посылает текст статьи
    """
    doc_text = bot_commands.doc(user_text)
    # Текст статьи
    if doc_text is None:
        bot.send_message(chat_id, DOC_NOT_EXIST)
    else:
        bot.send_message(chat_id, doc_text)


def bot_topic(chat_id, user_text):
    """
    Функция отправки описания темы
    :param chat_id: идентификатор чата
    :param user_text: текст пользователя
    :return: посылает описание темы и несколько последних статей из неё
    """
    description, docs_list = bot_commands.topic(user_text)
    # Описание и последние статьи в теме
    if description is None:
        bot.send_message(chat_id, TOPIC_NOT_EXIST)
    else:
        bot.send_message(chat_id, description)
        for current_doc in docs_list:
            bot.send_message(chat_id, current_doc)


def bot_new_docs(chat_id, user_text):
    """
    Функция отправки последних опубликованных статей
    :param chat_id: идентификатор чата
    :param user_text: текст пользователя
    :return: посылает последние опубликованные статьи
    """
    docs_list = bot_commands.new_docs(user_text)
    # Последние опубликованные статьи
    if docs_list is None:
        bot.send_message(chat_id, WRONG_NUMBER)
    else:
        for current_doc in docs_list:
            bot.send_message(chat_id, current_doc)


def bot_new_topics(chat_id, user_text):
    """
    Функция отправки последних обновлённых тем
    :param chat_id: идентификатор чата
    :param user_text: текст пользователя
    :return: посылает последние обновлённые темы
    """
    topics_list = bot_commands.new_topics(user_text)
    # Последние обновлённые темы
    if topics_list is None:
        bot.send_message(chat_id, WRONG_NUMBER)
    else:
        for current_topic in topics_list:
            bot.send_message(chat_id, current_topic)


def bot_words(chat_id, user_text):
    """
    Функция отправки популярных тэгов из темы
    :param chat_id: идентификатор чата
    :param user_text: текст пользователя
    :return: посылает популярные тэги темы
    """
    tags_list = bot_commands.tags(user_text)
    # Самые популярные тэги по теме
    if tags_list is not None:
        for tag in tags_list:
            bot.send_message(chat_id, tag)
    else:
        bot.send_message(chat_id, TOPIC_NOT_EXIST)


def bot_describe_doc(chat_id, user_text):
    """
    Функция отправки статистики по статье
    :param chat_id: идентификатор чата
    :param user_text: текст пользователя
    :return: посылает графики частот слов и длин слов в статье
    """
    doc_info = bot_commands.describe_doc(user_text, chat_id)
    # Описание статьи
    if doc_info is not None:
        with open(doc_info[0], 'rb') as plot1:
            bot.send_photo(chat_id, plot1)
        with open(doc_info[1], 'rb') as plot1:
            bot.send_photo(chat_id, plot1)
    else:
        bot.send_message(chat_id, DOC_NOT_EXIST)


def bot_describe_topic(chat_id, user_text):
    """
    Функция отправки статистики по теме
    :param chat_id: идентификатор чата
    :param user_text: текст пользователя
    :return: посылает количество статей в теме,
    среднюю длину статьей темы в словах,
    графики частот слов и длин слов в теме
    """
    topic_info = bot_commands.describe_topic(user_text, chat_id)
    # Описание темы
    if topic_info is not None:
        bot.send_message(chat_id,
                         'Количество статей по данной теме в базе: '
                         + str(topic_info[0]))
        bot.send_message(chat_id,
                         'Средняя длина документа: '
                         + str(topic_info[1]) + ' слов')
        with open(topic_info[2][0], 'rb') as plot1:
            bot.send_photo(chat_id, plot1)
        with open(topic_info[2][1], 'rb') as plot1:
            bot.send_photo(chat_id, plot1)
    else:
        bot.send_message(chat_id, TOPIC_NOT_EXIST)


@bot.message_handler(commands=COMMANDS_LIST, content_types=['text'])
def get_command(message):
    """
    Получение команды от пользователя и её предварительная обработка
    :param message: текст пользователя с командой
    :return: устанавливает состояние пользователя на стартовое
    """
    set_user(message.chat.id)
    user_command = re.findall(r'\w+', message.text)[0]
    # Команда пользователя
    user_text = message.text.replace('/' + user_command, '').strip()
    # Сообщение пользователя помимо команды
    print(user_command, user_text, message.chat.first_name, message.chat.last_name)
    users[message.chat.id].action = user_command
    if user_text == '':
        if user_command == 'start':
            bot.send_message(message.chat.id, GREETING)
        elif user_command == 'help':
            bot.send_message(message.chat.id, HELP_LIST)
        elif user_command == 'new_topics' or user_command == 'new_docs':
            message.text = DEFAULT_NEW_NUMBER
            get_message(message)
        else:
            bot.send_message(message.chat.id, 'Введите параметр команды')
    else:
        exec('bot_' + user_command + '(message.chat.id, user_text)')
    users[message.chat.id].action = 'start'


@bot.message_handler(content_types=['text'])
def get_message(message):
    """
    Получение текста без команды от пользователя и её обработка
    :param message: текст пользователя без команд
    :return: устанавливает состояние пользователя на стартовое
    """
    set_user(message.chat.id)
    user_text = message.text
    # Сообщение пользователя
    print(user_text, message.chat.first_name, message.chat.last_name)
    user_command = users[message.chat.id].action
    # Команда, ранее посланная пользователем
    exec('bot_' + user_command + '(message.chat.id, user_text)')
    users[message.chat.id].action = 'start'

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except RuntimeError:
            pass
