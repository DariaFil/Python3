import db_commands
import re


def topic(topic_name):
    """
    Вывод информации о теме
    :param topic_name: название темы
    :return: описание темы и 5 последних добавленных в неё статей;
    если тема отсутствует в базе данных, выводит None
    """
    current_topic = db_commands.search_topic(topic_name)
    # Тема из базы данных с данным заголовком
    if current_topic is None:
        return None, None
    else:
        description = current_topic.description
        # Описание темы
        docs_list = db_commands.search_last_topic_docs(current_topic.name)
        # Последние добавленные в тему статьи
        message_list = []
        # Информация для отправления боту
        index = 1
        # Номер статьи
        for current_doc in docs_list:
            messager_text = str(index) +\
                            '. ' + current_doc.name + \
                            '\n' + current_doc.url
            message_list.append(messager_text)
            index += 1
        return description, message_list


def doc(doc_name):
    """
    Вывод текста статьи
    :param doc_name: название статьи
    :return: текст статьи;
    если статья отсутствует в базе данных, выводит None
    """
    doc_name = db_commands.clean_quotes(doc_name)
    real_doc = db_commands.search_doc(doc_name)
    # Статья из базы данных с данным заголовком
    if real_doc is None:
        return real_doc
    else:
        return real_doc.text


def new_docs(str_number):
    """
    Вывод новых статей
    :param str_number: количество статей для вывода
    :return: список новых статей;
    в случае неверного ввода параметра выводит None
    """
    try:
        number = int(str_number)
        # Численное количество последних статей
    except ValueError:
        return None
    else:
        if number < 1:
            return None
        else:
            docs = db_commands.search_last_docs(number)
            # Последние опубликованные статьи
            index = 1
            # Номер статьи
            docs_list = []
            # Информация для отправления боту
            for current_doc in docs:
                messager_text = str(index) + \
                                '. ' + current_doc.name + \
                                '\n' + current_doc.url
                docs_list.append(messager_text)
                index += 1
            return docs_list


def new_topics(str_number):
    """
    Вывод последних обновлённых тем
    :param str_number: количество тем для вывода
    :return: список последних обновлённых тем;
    в случае неверного ввода параметра выводит None
    """
    try:
        number = int(str_number)
        # Численное количество последних тем
    except ValueError:
        return None
    else:
        if number < 1:
            return None
        else:
            last_topics = db_commands.search_last_topic(number)
            # Последние обновлённые темы
            index = 1
            # Номер темы
            topics_list = []
            # Информация для отправления боту
            for current_topic in last_topics:
                messager_text = str(index) + '. ' + \
                                current_topic.name + \
                                '\n' + current_topic.description + \
                                '\n' + current_topic.url
                topics_list.append(messager_text)
                index += 1
            return topics_list


def tags(topic_name):
    """
    Выводит самые популярные тэги темы
    :param topic_name: название темы
    :return: список самых популярных тэгов;
    если тема отсутствует в базе данных, выводит None
    """
    chosen_topic = db_commands.search_topic(topic_name)
    # Тема из базы данных с данным заголовком
    if chosen_topic is None:
        return None
    else:
        return db_commands.search_topic_tags(chosen_topic)


def describe_doc(doc_name, user_id):
    """
    Выводит описание статьи
    :param doc_name: название статьи
    :param user_id: идентификатор пользователя
    :return: два графика с описанием статьи;
    если статья отсутствует в базе данных, выводит None
    """
    chosen_doc = db_commands.search_doc(doc_name)
    # Статья из базы данных с данным заголовком
    if chosen_doc is None:
        return None
    else:
        word_statistics = db_commands.doc_word_statistics(chosen_doc)
        # Словарь частот слов в статье
        length_statistics = db_commands.length_statistics(word_statistics)
        # Словарь частот длин слов в статье
        files = db_commands.words_plot('doc' + str(user_id),
                                       word_statistics,
                                       length_statistics)
        # Графики, иллюстрирующие частоты слов и из длин в статье
        return files


def describe_topic(topic_name, user_id):
    """
    Выводит описание темы
    :param topic_name: название темы
    :param user_id: идентификатор пользователя
    :return: количество статей в теме, средняя длина статей в теме в словах,
    два графика с описанием темы;
    если статья отсутствует в базе данных, выводит None
    """
    chosen_topic = db_commands.search_topic(topic_name)
    # Тема из базы данных с данным заголовком
    if chosen_topic is None:
        return None, None, None
    else:
        doc_count = 0
        # Количество статей в теме
        docs_len = 0
        # Длина конкретной статьи в словах
        for current_doc in chosen_topic.documents:
            doc_count += 1
            docs_len += len(re.findall(r'\w+', current_doc.text))
        avg_doc_len = int(docs_len / doc_count)
        # Средняя длина статей в теме
        word_statistics = db_commands.topic_word_statistics(chosen_topic)
        # Словарь частот слов в теме
        length_statistics = db_commands.length_statistics(word_statistics)
        # Словарь частот длин слов в теме
        files = db_commands.words_plot('topic' + str(user_id),
                                       word_statistics,
                                       length_statistics)
        # Графики, иллюстрирующие частоты слов и из длин в теме
        return doc_count, avg_doc_len, files
