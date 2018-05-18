import requests
from bs4 import BeautifulSoup
import db_commands
import dateparser

# Значения классов для объектов, которые мы будем парсить

default_date = dateparser.parse('1000-01-01')
# Дефолтная дата
website = "https://www.rbc.ru/story/"
# Главная страница сайта
topic_class = 'item item_story js-story-item'
# Класс тем новостей
topic_docs = 'item item_story-single js-story-item'
# Класс статей из темы
topic_url_class = 'item__link no-injects'
# Класс адреса темы
doc_url_class = 'item__link no-injects js-yandex-counter'
# Класс адреса статьи
title_class = 'item__title'
# Класс заголовка
text_class = 'item__text'
# Класс текста статьи
time_class = 'item__info'
# Класс времени добавления
tags_class = 'article__tags'
# Класс блока тэгов статьи
tag_class = 'article__tags__link'
# Класс тэга


def parse_topics(topic):
    """
    Функция, производящая парсинг темы
    :param topic: тема, взятая непосредственно с сайта
    :return: флаг, является ли тема новой в базе данных;
        эта тема, добавленная в базу данных
    """
    title = topic.find('span', {'class': title_class}).text.strip()
    # Заголовок темы
    title = db_commands.clean_quotes(title)
    real_topic = db_commands.search_topic(title)
    # Результат поиска в базе данных по названию
    if real_topic is None:
        url = topic.find('a', {'class': topic_url_class})['href'].strip()
        # Адрес темы
        description = topic.find('span', {'class': text_class}).text.strip()
        # Описание темы
        description = db_commands.clean_quotes(description)
        return True, db_commands.add_topic(title, url, description)
    return False, real_topic


def parse_doc(topic, doc, is_new_topic):
    """
    Функция, производящая парсинг статьи
    :param topic: тема, в которую входит эта статья
    :param doc: статья, взятая непосредственно с сайта
    :param is_new_topic: флаг, отмечающий, является ли эта тема новой в базе
    :return: время публикации статьи;
        эта статья, добавленная в базу данных
    """
    title = doc.find('span', {'class': title_class}).text.strip()
    # Заголовок статьи
    title = db_commands.clean_quotes(title)
    time = doc.find('span', {'class': time_class}).text.strip()
    # Время публикации статьи
    update_time = dateparser.parse(time)
    # Вермя публикации статьи в удобном формате
    print('doc', topic.name, title, time)
    real_doc = db_commands.search_doc(title)
    # Результат поиска статьи в базе данных по названию
    if real_doc is None:
        url = doc.find('a', {'class': doc_url_class})['href'].strip()
        # Адрес статьи
        print(url)
        doc_text = BeautifulSoup(requests.get(url).text, 'lxml')
        # Необработанный текст статьи
        text = parse_text(doc_text)
        # Обработанный текст статьи
        real_doc = db_commands.add_document(topic, title, url,
                                            update_time, text)
        # Добавленная в базу данных статья
        tag_data = BeautifulSoup(requests.get(real_doc.url).text, 'lxml')
        # Страница статьи
        tags_block = tag_data.find('div', {'class': tags_class})
        # Блок тэгов статьи
        if tags_block is not None:
            parse_tag(real_doc, tags_block)
    if is_new_topic:
        update_topic_time(topic, update_time)
        return '', real_doc
    else:
        return update_time, real_doc


def update_topic_time(topic, time):
    """
    Функция, обновляющая время темы
    :param topic: тема
    :param time: новое время
    :return: сохраняет тему с новым временем
    """
    if topic.last_update_time < time:
        topic.last_update_time = time
        topic.save()


def parse_text(doc_text):
    """
    Функция, производящая парсинг текста статьи
    :param doc_text: изначальный текст, вынутый со страницы сайта
    :return: готовый чистый текст
    """
    text = doc_text.find_all('p')
    # Абзацы текста
    for i in range(len(text)):
        text[i] = text[i].text
    real_text = '\n'.join(text)
    # Полный текст статьи
    return real_text


def parse_tag(doc, tags_block):
    """
    Функция, производящая парсинг тэгов
    :param doc: документ, к которому относятся тэги
    :param tags_block: блок тэгов этого документа
    :return: добавляет тэги в базу данных
    """
    tags = tags_block.find_all('a', {'class': tag_class})
    # Список тэгов в статье
    for tag in tags:
        tag_name = tag.text.strip()
        # Название тэга
        print('tag', tag_name)
        if db_commands.search_tag(doc, tag_name) is None:
            db_commands.add_tag(doc, tag_name)


def parse():
    """
    Функция, производящая парсинг сайта
    """
    data = BeautifulSoup(requests.get(website).text, 'lxml')
    # Полные данные с страницы со статьями
    topics = data.find_all('div', {'class': topic_class})
    # Список тем на странице
    print(len(topics))
    for topic in topics:
        is_new, real_topic = parse_topics(topic)
        # Флаг, является ли тема новой, и сама тема
        if is_new:
            print('new_topic', real_topic.name)
        else:
            print(real_topic.name)
        new_upd_time = default_date
        # Вермя для обновления времени обновления темы
        top = BeautifulSoup(requests.get(real_topic.url).text, 'lxml')
        # Страница темы
        docs = top.find_all('div', {'class': topic_docs})
        # Все статьи со страницы темы
        print(len(docs))
        for doc in docs:
            new_time, db_doc = parse_doc(real_topic, doc, is_new)
            # Время публикации статьи и сама статья
            if not is_new:
                if new_upd_time < new_time:
                    new_upd_time = new_time
                if new_time <= real_topic.last_update_time:
                    update_topic_time(real_topic, new_upd_time)
                    print('updated topic time', new_upd_time)
                    break

if __name__ == '__main__':
    session = requests.Session()
    session.max_redirects = 100
    parse()
