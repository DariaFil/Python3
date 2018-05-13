from db_tables import Topic, Document, Tag
import pandas
import matplotlib.pyplot
import dateparser
import re


def add_topic(topic, url, desc):
    new_topic = Topic.create(name=topic, url=url, description=desc,
                             last_update_time=dateparser.parse('1000-01-01'))
    new_topic.save()
    return new_topic


def search_topic(topic):
    exist_topic = Topic.select().where(Topic.name == topic)
    if len(exist_topic) == 0:
        return None
    return exist_topic[0]


def search_last_topic(n):
    topics = []
    for topic in Topic.select().order_by(Topic.last_update_time.desc()).limit(n):
        topics.append(topic)
    return topics


def topic_statistics(topic):
    topic_stat = {}
    for doc in topic.documents:
        doc_stat = doc_word_statistics(doc)
        for word in doc_stat.keys():
            if topic_stat.get(word) is None:
                topic_stat.update({word: doc_stat[word]})
            else:
                topic_stat[word] += doc_stat[word]
    return topic_stat


def add_document(topic, doc_name, url, time, text):
    new_doc = Document.create(topic=topic, name=doc_name,
                              url=url, last_update_time=time, text=text)
    new_doc.save()
    return new_doc


def search_doc(doc):
    exist_doc = Document.select().where(Document.name == doc)
    if len(exist_doc) == 0:
        return None
    return exist_doc


def search_last_docs(n):
    docs = []
    for doc in Document.select().\
            order_by(Document.last_update_time.desc()).limit(n):
        docs.append(doc)
    return docs


def search_last_topic_docs(topic):
    docs = []
    topic = Topic.select().where(Topic.name == topic)
    for doc in Document.select().where(Document.topic == topic).\
            order_by(Document.last_update_time.desc()).limit(5):
        docs.append(doc)
    return docs


def doc_word_statistics(doc):
    statistics = {}
    words = re.findall(r'\w+', doc.text)
    for word in words:
        if statistics.get(word) is None:
            statistics.update({word: 1})
        else:
            statistics[word] += 1
    return statistics


def length_statistics(word_dict):
    length = {}
    for word in word_dict.keys():
        if length.get(len(word)) is None:
            length.update({len(word): word_dict[word]})
        else:
            length[len(word)] += word_dict[word]
    return length


def add_tag(doc, tag):
    new_tag = Tag.create(name=tag, document=doc)
    new_tag.save()


def search_tag(doc, tag):
    exist_tag = Tag.select().where(Tag.name == tag and Tag.document == doc)
    if len(exist_tag) == 0:
        return None
    return exist_tag


def search_topic_tags(topic):
    tag_dict = {}
    tag_list = ['' for i in range(5)]
    count_list = [0 for i in range(5)]
    for doc in topic.documents:
        for tag in doc.tags:
            if tag_dict.get(tag.name) is None:
                tag_dict.update({tag.name: 1})
            else:
                tag_dict[tag.name] += 1
            if not(tag.name in tag_list):
                for i in range(5):
                    if tag_dict[tag.name] > count_list[i]:
                        for j in range(3, i, -1):
                            count_list[i + 1] = count_list[i]
                            tag_list[i + 1] = tag_list[i]
                        count_list[i] = tag_dict[tag.name]
                        tag_list[i] = tag.name
                        break
    return tag_list


def do_plot(data, title, x_label, y_label):
    data_frame = pandas.DataFrame(data)
    plot = data_frame.plot(kind='line', title=title)
    plot.set_xlabel(x_label)
    plot.set_ylabel(y_label)
    return plot


def word_stat_plot(file, word_dict, len_dict):
    len_max = max(len_dict.keys())
    count_len = [0 for i in range(len_max + 1)]
    for i in range(1, len_max + 1):
        if i in len_dict.keys():
            count_len[i] = len_dict[i]
        else:
            count_len[i] = 0
    max_freq = max(word_dict.values())
    count_freq = [0 for i in range(max_freq + 1)]
    for words in word_dict.values():
        count_freq[words] += 1
    file1 = file + '-1.png'
    file2 = file + '-2.png'
    do_plot(count_len,
            'Распределение длин слов',
            'Длина слова',
            'Количество слов с этой длиной')
    matplotlib.pyplot.savefig(file1)
    matplotlib.pyplot.close()
    do_plot(count_freq,
            'Распределение слов',
            'Частота возникновения слова',
            'Количество слов')
    matplotlib.pyplot.savefig(file2)
    matplotlib.pyplot.close()
    return file1, file2
