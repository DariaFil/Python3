import requests
from bs4 import BeautifulSoup
import db_commands
import dateparser

default_date = '1000-01-01'
website = "https://www.rbc.ru/story/"
topic_class = 'item item_story js-story-item'
topic_docs = 'item item_story-single js-story-item'
topic_url_class = 'item__link no-injects'
doc_url_class = 'item__link no-injects js-yandex-counter'
title_class = 'item__title'
text_class = 'item__text'
time_class = 'item__info'
tags_class = 'article__tags'
tag_class = 'article__tags__link'


def parse_topics(topic):
    url = topic.find('a', {'class': topic_url_class})['href'].strip()
    title = topic.find('span', {'class': title_class}).text.strip()
    description = topic.find('span', {'class': text_class}).text.strip()
    real_topic = db_commands.search_topic(title)
    if real_topic is None:
        return True, db_commands.add_topic(title, url, description)
    return False, real_topic


def parse_doc(topic, doc, is_new_topic):
    url = doc.find('a', {'class': doc_url_class})['href'].strip()
    title = doc.find('span', {'class': title_class}).text.strip()
    time = doc.find('span', {'class': time_class}).text.strip()
    update_time = dateparser.parse(time)
    print('doc', topic.name, title, time)
    doc_text = BeautifulSoup(requests.get(url).text, 'lxml')
    text = parse_text(doc_text)
    real_doc = db_commands.search_doc(title)
    if real_doc is None:
        real_doc = db_commands.add_document(topic, title, url,
                                            update_time, text)
        tag_data = BeautifulSoup(requests.get(real_doc.url).text, 'lxml')
        tags_block = tag_data.find('div', {'class': tags_class})
        if tags_block is not None:
            parse_tag(real_doc, tags_block)
    if is_new_topic:
        update_topic_time(topic, update_time)
        return '', real_doc
    else:
        return update_time, real_doc


def update_topic_time(topic, time):
    if topic.last_update_time < time:
        topic.last_update_time = time
        topic.save()


def parse_text(doc_text):
    text = doc_text.find_all('p')
    for i in range(len(text)):
        text[i] = text[i].text
    real_text = '\n'.join(text)
    return real_text


def parse_tag(doc, tags_block):
    tags = tags_block.find_all('a', {'class': tag_class})
    for tag in tags:
        tag_name = tag.text.strip()
        print('tag', tag_name)
        if db_commands.search_tag(doc, tag_name) is None:
            db_commands.add_tag(doc, tag_name)


def parse():
    data = BeautifulSoup(requests.get(website).text, 'lxml')
    topics = data.find_all('div', {'class': topic_class})
    print(len(topics))
    for topic in topics:
        is_new, real_topic = parse_topics(topic)
        if is_new:
            print('new_topic', real_topic.name)
        else:
            print(real_topic.name)
        new_upd_time = dateparser.parse(default_date)
        top = BeautifulSoup(requests.get(real_topic.url).text, 'lxml')
        docs = top.find_all('div', {'class': topic_docs})
        print(len(docs))
        for doc in docs:
            new_time, db_doc = parse_doc(real_topic, doc, is_new)
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
