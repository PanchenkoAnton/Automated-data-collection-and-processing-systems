import asyncio

from motor.motor_asyncio import AsyncIOMotorClient
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from spacy.lang.ru import Russian

from Project_parser.parsers.HTMLParser import HTMLParser


def update_tf(d, k, document, count):
    if k in d:
        d[k].append((document, count))
    else:
        d[k] = [(count, document)]
    return d


def merge_tf(global_tf, local_tf):
    for key in local_tf.keys():
        if key in global_tf:
            global_tf[key].extend(local_tf[key])
        else:
            global_tf[key] = local_tf[key]
    return global_tf


async def do_find_one():
    tf = {}
    db = AsyncIOMotorClient('localhost', 27000)['crawler']
    collection_msu = db.msu
    document = await collection_msu.find_one({"url": "https://www.msu.ru/"})
    parser = HTMLParser(text=document['data'])
    text = parser.get_text()

    nlp = Russian()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    tmp_text = ' '.join(tokens)
    doc_text = nlp(tmp_text)
    lemmas = []
    for s in doc_text:
        if s.lemma_ not in set(stopwords.words('russian')) \
                and s.lemma_ not in set(stopwords.words('english')):
            lemmas.append(s.lemma_)
    freq = FreqDist(lemmas)
    print(freq.most_common(10))

    for k, v in freq.most_common(10):
        tf = update_tf(tf, k, "https://www.msu.ru/", v)

    return tf


async def do_find_another_one():
    tf = {}
    db = AsyncIOMotorClient('localhost', 27000)['crawler']
    collection_msu = db.msu
    document = await collection_msu.find_one({"url": "https://www.msu.ru/science/allevents.html"})
    parser = HTMLParser(text=document['data'])
    text = parser.get_text()

    nlp = Russian()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    tmp_text = ' '.join(tokens)
    doc_text = nlp(tmp_text)
    lemmas = []
    for s in doc_text:
        if s.lemma_ not in set(stopwords.words('russian')) \
                and s.lemma_ not in set(stopwords.words('english')):
            lemmas.append(s.lemma_)
    freq = FreqDist(lemmas)
    print(freq.most_common(10))

    for k, v in freq.most_common(10):
        tf = update_tf(tf, k, "https://www.msu.ru/science/allevents.html", v)

    return tf


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    l_tf = loop.run_until_complete(do_find_one())
    global_tf = {}
    global_tf = merge_tf(global_tf, l_tf)
    l_tf = loop.run_until_complete(do_find_another_one())
    global_tf = merge_tf(global_tf, l_tf)
    print(global_tf)
