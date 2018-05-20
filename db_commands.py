from db_tables import Topic, Document, Tag
import pandas
import matplotlib.pyplot
import re
import dateparser

# Установка дефолтных параметров

default_date = dateparser.parse('1000-01-01')
# Дефолтная дата
last_topic_docs = 5
# Число последних документов в теме по умолчанию
popular_tags = 5
# Количество популяных тэгов
freq_dict_len = 10
# Длина словаря максимальных по встечаемости слов


def clean_quotes(text):
    """
    Замена кавычек
    :param text: текст с книжными кавычками
    :return: текст с традиционными кавычками
    """
    text = text.replace('«', '"')
    text = text.replace('»', '"')
    return text


def add_topic(topic, url, desc):
    """
    Добавление темы в базу данных
    :param topic: название темы
    :param url: адрес темы
    :param desc: описание темы
    :return: тама, созданная в базе данных
    """
    new_topic = Topic.create(name=topic, url=url,
                             description=desc,
                             last_update_time=default_date)
    # Новая тема в базе данных
    new_topic.save()
    return new_topic


def add_document(topic, doc_name, url, time, text):
    """
    Добавление статьи в базу данных
    :param topic: тема, к которой статья относится
    :param doc_name: название статьи
    :param url: адрес статьи
    :param time: время публикации статьи
    :param text: текст статьи
    :return: добавленная в базу данных статья
    """
    new_doc = Document.create(topic=topic, name=doc_name,
                              url=url, last_update_time=time, text=text)
    # Новая статья в базе данных
    new_doc.save()
    return new_doc


def add_tag(doc, tag):
    """
    Добавление тэга в базу данных
    :param doc: статья, к которой прикреплён тэг
    :param tag: название тэга
    """
    new_tag = Tag.create(name=tag, document=doc)
    # Новый тэг в базе данных
    new_tag.save()


def search_topic(topic):
    """
    Поиск темы по названию
    :param topic: название темы
    :return: тема из базы данных, если она в ней есть, иначе None
    """
    exist_topic = Topic.select().\
        where(Topic.name == topic).get()
    # Тема из базы данных, если она там есть
    return exist_topic


def search_doc(doc):
    """
    Поиск статьи по названию
    :param doc: название статьи
    :return: статья из базы данных, если она в ней есть, иначе None
    """
    exist_doc = Document.select().\
        where(Document.name == doc).get()
    # Статья из базы данных, если она там есть
    return exist_doc


def search_tag(doc, tag):
    """
    Название тэга в статье
    :param doc: статья из базы данных
    :param tag: название тэга
    :return:
    """
    exist_tag = Tag.select().\
        where(Tag.name == tag and Tag.document == doc).get()
    # Тэг из базы данных, если он там есть
    return exist_tag


def search_last_topic(n):
    """
    Поиск последних обновлённых тем
    :param n: количество необходимых тем
    :return: список последних тем
    """
    topics = []
    # Список последних обновлённых тем
    for topic in Topic.select().\
            order_by(Topic.last_update_time.desc()).\
            limit(n):
        topics.append(topic)
    return topics


def search_last_docs(n):
    """
    Поиск последних добавленных статей
    :param n: количество необходимых статей
    :return: список последних статей
    """
    docs = []
    # Список последних добавленных статей
    for doc in Document.select().\
            order_by(Document.last_update_time.desc()).\
            limit(n):
        docs.append(doc)
    return docs


def search_last_topic_docs(topic):
    """
    Поиск последних добавленных в тему статей
    :param topic: название темы
    :return:
    """
    docs = []
    # Список последних добавленных в тему статей
    topic = Topic.select().\
        where(Topic.name == topic)
    # Тема из базы данных
    for doc in Document.select().where(Document.topic == topic).\
            order_by(Document.last_update_time.desc()).\
            limit(last_topic_docs):
        docs.append(doc)
    return docs


def search_topic_tags(topic):
    """
    Поиск самых популярных тэгов в теме
    :param topic: тема из базы данных
    :return: список самых популярных тэгов
    """
    tag_dict = {}
    # Словарь тэгов и их количества в теме
    tag_list = [''] * popular_tags
    # Спикок названий самых популярных тэгов
    count_list = [0] * popular_tags
    # Спикок количества самых популярных тэгов
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


def topic_word_statistics(topic):
    """
    Подсчёт частот встречаемости слов в теме
    :param topic: тема из базы данных
    :return: словарь слов и их частот
    """
    topic_stat = {}
    # Словарь частот слов по теме
    for doc in topic.documents:
        doc_stat = doc_word_statistics(doc)
        # Словарь частот слов по статье
        for word in doc_stat.keys():
            if topic_stat.get(word) is None:
                topic_stat.update({word: doc_stat[word]})
            else:
                topic_stat[word] += doc_stat[word]
    return topic_stat


def doc_word_statistics(doc):
    """
    Подсчёт частот встречаемости слов в статье
    :param doc: статья из базы данных
    :return: словарь слов и их частот
    """
    statistics = {}
    # Словарь частот слов по статье
    words = re.findall(r'\w+', doc.text)
    # Все слова статьи
    for word in words:
        if statistics.get(word) is None:
            statistics.update({word: 1})
        else:
            statistics[word] += 1
    return statistics


def length_statistics(word_dict):
    """
    Подсчёт частот встречаемости слов определённой длины
    :param word_dict: словарь слов и их частот
    :return: словарь длин слов и их частот
    """
    length = {}
    # Словарь частот длин слов
    for word in word_dict.keys():
        if length.get(len(word)) is None:
            length.update({len(word): word_dict[word]})
        else:
            length[len(word)] += word_dict[word]
    return length


def do_plot(data, title, x_label, y_label, kind):
    """
    Создание конкретного графика
    :param data: данные, из которых строится график
    :param title: название графика
    :param x_label: название х-координаты графика
    :param y_label: название у-координаты графика
    :param kind: вид графика (обычный график или груговая диаграмма)
    :return: готовый график
    """
    if kind == 'bar':
        data_frame = pandas.DataFrame(data)
        # frame данных
        plot = data_frame.plot(kind=kind, title=title)
        # График данных
        plot.set_xlabel(x_label)
        plot.set_ylabel(y_label)
        matplotlib.pyplot.legend('')
    else:
        data_series = pandas.Series(data, name=' ')
        # frame данных
        plot = data_series.plot.pie(title=title)
        # График данных
    return plot


def words_plot(file, word_dict, len_dict):
    """
    Создание графиков частот слов и частот их длин
    :param file: название файла для сохранения
    :param word_dict: словарь частот слов
    :param len_dict: словарь частот длин слов
    :return: два графика, для частот длин слов и частот слов
    """
    len_max = max(len_dict.keys())
    # Максимальная длина слова по словарю длин
    count_len = [0]*(len_max + 1)
    # Список длин слов и их частота
    for word_length in range(1, len_max + 1):
        if word_length in len_dict.keys():
            count_len[word_length] = len_dict[word_length]
    freq_dict = {}
    # Словарь частых слов и их частот
    required_len = min(int(len(word_dict) / 50), 6)
    # Необходимая длина слова для попадания в этот список
    required_freq = int(len(word_dict) / 100)
    # Необходимая частота слова для попадания в этот список
    if len(word_dict) > 1000:
        required_freq = int(required_freq / 2)
    for word in word_dict.keys():
        if word_dict[word] > required_freq \
                and len(word) > required_len \
                and len(freq_dict) < freq_dict_len:
            freq_dict.update({word: word_dict[word]})
    len_file = file + '-1.png'
    # Файл с графиков частот длин слов
    freq_file = file + '-2.png'
    # Файл с графиков частот популярных слов
    do_plot(count_len,
            'Распределение длин слов',
            'Длина слова',
            'Количество слов с этой длиной',
            'bar')
    matplotlib.pyplot.savefig(len_file)
    matplotlib.pyplot.close()
    do_plot(freq_dict,
            'Распределение популярных слов',
            'Частота возникновения слова',
            'Количество слов',
            'pie')
    matplotlib.pyplot.savefig(freq_file)
    matplotlib.pyplot.close()
    return len_file, freq_file
