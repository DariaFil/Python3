import telebot
import db_commands


class User:
    def __init__(self, id):
        self.id = id
        self.status = 'start'


users = dict()
bot = telebot.TeleBot('521302347:AAFWdv5Udnk8Iz6_SvaoyoIscwwinvJd1qk')
bot_activity = { "commands": {
    "/start": "Hello! I am ready to show you recent news",
    "/help": "/help - list of commands\n \
             /start - start bot\n \
             /stop - stop current command\n \
             /new_docs - show last articles\n \
             /new_topics - show last topics\n \
             /topic - show description of topic\n \
             /doc - show text of article \n \
             /words - show main words of topic\n \
             /describe_doc - show statistics about article\n \
             /describe_topic - show statistics about topic",
    "/stop": "OK, I stop"
  }
}


def set_user(id):
    if id not in users:
        users[id] = User(id)


@bot.message_handler(commands=['start', 'help', 'stop'])
def handle_standard(message):
    set_user(message.chat.id)
    print(message.text, message.chat.first_name, message.chat.last_name)
    bot.send_message(message.chat.id, bot_activity['commands'][message.text])
    users[message.chat.id].status = 'start'


@bot.message_handler(commands=['new_docs'])
def new_docs(message):
    set_user(message.chat.id)
    print(message.text, message.chat.first_name, message.chat.last_name)
    users[message.chat.id].status = 'new_docs'
    bot.send_message(message.chat.id, 'How many?')


@bot.message_handler(commands=['new_topics'])
def new_topics(message):
    set_user(message.chat.id)
    print(message.text, message.chat.first_name, message.chat.last_name)
    users[message.chat.id].status = 'new_topics'
    bot.send_message(message.chat.id, 'How many?')


@bot.message_handler(commands=['topic'])
def topic(message):
    set_user(message.chat.id)
    print(message.text, message.chat.first_name, message.chat.last_name)
    users[message.chat.id].status = 'topic'
    bot.send_message(message.chat.id, 'Which topic?')


@bot.message_handler(commands=['doc'])
def doc(message):
    set_user(message.chat.id)
    print(message.text, message.chat.first_name, message.chat.last_name)
    users[message.chat.id].status = 'doc'
    bot.send_message(message.chat.id, 'Which article?')


@bot.message_handler(commands=['words'])
def words(message):
    set_user(message.chat.id)
    print(message.text, message.chat.first_name, message.chat.last_name)
    users[message.chat.id].status = 'words'
    bot.send_message(message.chat.id, 'Which topic?')


@bot.message_handler(commands=['describe_doc'])
def describe_doc(message):
    set_user(message.chat.id)
    print(message.text, message.chat.first_name, message.chat.last_name)
    users[message.chat.id].status = 'describe_doc'
    bot.send_message(message.chat.id, 'Which article?')


@bot.message_handler(commands=['describe_topic'])
def describe_topic(message):
    set_user(message.chat.id)
    print(message.text, message.chat.first_name, message.chat.last_name)
    users[message.chat.id].status = 'describe_topic'
    bot.send_message(message.chat.id, 'Which topic?')


@bot.message_handler(content_types=['text'])
def get_message(message):
    print(message.text, message.chat.first_name, message.chat.last_name)
    if users[message.chat.id].status == 'start':
        bot.send_message(message.chat.id, 'What do you want? Use commands, please')
    if users[message.chat.id].status == 'topic':
        topic_name = message.text
        topic = db_commands.search_topic(topic_name)
        bot.send_message(message.chat.id, topic.description)
        docs_list = db_commands.search_last_topic_docs(topic.name)
        for doc in docs_list:
            bot.send_message(message.chat.id, doc.name + '\n' + doc.url)
        users[message.chat.id].status = 'start'
    if users[message.chat.id].status == 'doc':
        doc_name = message.text
        doc = db_commands.search_doc(doc_name)
        bot.send_message(message.chat.id, doc.text)
        users[message.chat.id].status = 'start'
    if users[message.chat.id].status == 'new_docs':
        user_text = message.text
        number = int(user_text)
        docs = db_commands.search_last_docs(number)
        for doc in docs:
            bot.send_message(message.chat.id, doc.name + '\n' + doc.url)
        users[message.chat.id].status = 'start'
    if users[message.chat.id].status == 'new_topics':
        user_text = message.text
        number = int(user_text)
        topics = db_commands.search_last_topic(number)
        for topic in topics:
            bot.send_message(message.chat.id, topic.name + '\n' + 
                             topic.description + '\n' + topic.url)
        users[message.chat.id].status = 'start'
    if users[message.chat.id].status == 'words':
        topic_name = message.text
        topic = db_commands.search_topic(topic_name)
        if topic is not None:
            tags = db_commands.search_topic_tags(topic)
            for tag in tags:
                bot.send_message(message.chat.id, tag.name)
        users[message.chat.id].status = 'start'
    if users[message.chat.id].status == 'describe_doc':
        doc_name = message.text
        doc = db_commands.search_doc(doc_name)
        if doc is not None:
            word_statistics = db_commands.doc_word_statistics(doc)
            length_statistics = db_commands.length_statistics(word_statistics)
            files = db_commands.word_stat_plot('doc' + str(message.chat.id), word_statistics, length_statistics)
            with open(files[0], 'rb') as plot1:
                bot.send_photo(message.chat.id, plot1)
            with open(files[1], 'rb') as plot1:
                bot.send_photo(message.chat.id, plot1)
        else:
            bot.send_message(message.chat.id, 'No such article in database')
        users[message.chat.id].status = 'start'
    if users[message.chat.id].status == 'describe_doc':
        topic_name = message.text
        topic = db_commands.search_topic(topic_name)
        if topic is not None:
            doc_count = 0
            docs_len = 0
            for doc in topic.documents:
                doc_count += 1
                docs_len += len(doc.text)
            avg_doc_len = docs_len / doc_count
            bot.send_message(message.chat.id, doc_count)
            bot.send_message(message.chat.id, avg_doc_len)
            word_statistics = db_commands.topic_statistics(topic)
            length_statistics = db_commands.length_statistics(word_statistics)
            files = db_commands.word_stat_plot('doc' + str(message.chat.id), word_statistics, length_statistics)
            with open(files[0], 'rb') as plot1:
                bot.send_photo(message.chat.id, plot1)
            with open(files[1], 'rb') as plot1:
                bot.send_photo(message.chat.id, plot1)
        users[message.chat.id].status = 'start'
