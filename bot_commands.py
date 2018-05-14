import db_commands
import re


def topic(topic_name):
    current_topic = db_commands.search_topic(topic_name)
    if current_topic is None:
        return None
    else:
        description = current_topic.description
        docs_list = db_commands.search_last_topic_docs(current_topic.name)
        message_list = []
        index = 1
        for current_doc in docs_list:
            messager_text = str(index) +\
                            '. ' + current_doc.name + \
                            '\n' + current_doc.url
            message_list.append(messager_text)
            index += 1
        return description, message_list


def doc(doc_name):
    return db_commands.search_doc(doc_name)


def new_docs(str_number):
    try:
        number = int(str_number)
    except ValueError:
        return None
    else:
        if number < 1:
            return None
        else:
            docs = db_commands.search_last_docs(number)
            index = 1
            docs_list = []
            for current_doc in docs:
                messager_text = str(index) + \
                                '. ' + current_doc.name + \
                                '\n' + current_doc.url
                docs_list.append(messager_text)
                index += 1
            return docs_list


def new_topics(str_number):
    try:
        number = int(str_number)
    except ValueError:
        return None
    else:
        if number < 1:
            return None
        else:
            last_topics = db_commands.search_last_topic(number)
            index = 1
            topics_list = []
            for current_topic in last_topics:
                messager_text = str(index) + '. ' + \
                                current_topic.name + \
                                '\n' + current_topic.description + \
                                '\n' + current_topic.url
                topics_list.append(messager_text)
                index += 1
            return topics_list


def tags(topic_name):
    chosen_topic = db_commands.search_topic(topic_name)
    if chosen_topic is None:
        return None
    else:
        return db_commands.search_topic_tags(chosen_topic)


def describe_doc(doc_name, user_id):
    chosen_doc = db_commands.search_doc(doc_name)
    if chosen_doc is None:
        return None
    else:
        word_statistics = db_commands.doc_word_statistics(chosen_doc)
        length_statistics = db_commands.length_statistics(word_statistics)
        files = db_commands.words_plot('doc' + str(user_id),
                                           word_statistics,
                                           length_statistics)
        return files


def describe_topic(topic_name, user_id):
    chosen_topic = db_commands.search_topic(topic_name)
    if chosen_topic is None:
        return None
    else:
        doc_count = 0
        docs_len = 0
        for current_doc in chosen_topic.documents:
            doc_count += 1
            docs_len += len(re.findall(r'\w+', current_doc.text))
        avg_doc_len = int(docs_len / doc_count)
        word_statistics = db_commands.topic_word_statistics(chosen_topic)
        length_statistics = db_commands.length_statistics(word_statistics)
        files = db_commands.words_plot('topic' + str(user_id),
                                           word_statistics,
                                           length_statistics)
        return doc_count, avg_doc_len, files
