import spacy
import asyncio
import string

from motor.motor_asyncio import AsyncIOMotorClient
import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from spacy.lang.ru import Russian

from Project_parser.parsers.HTMLParser import HTMLParser


async def do_find_one():
    nltk.download('stopwords')
    nltk.download('wordnet')
    db = AsyncIOMotorClient('localhost', 27017)['crawler']
    collection_msu = db.msu
    document = await collection_msu.find_one({"url": "https://www.msu.ru/"})
    parser = HTMLParser(text=document['data'])
    text = parser.get_text()
    # nlp = Russian()

    tmp_text = 'Здравствуйте, как у вас дела? Сегодня чудесная погодка у нас ' \
               'выдалась'

    nlp = spacy.load('ru2')
    # nlp = spacy.load('ru2', disable=['tagger', 'parser', 'NER'])
    # nlp.add_pipe(nlp.create_pipe('sentencizer'), first=True)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(tmp_text)
    tmp_text = ' '.join(tokens)
    doc_text = nlp(tmp_text)
    lemmas = []
    for s in doc_text:
        if s.lemma_ not in set(stopwords.words('russian')) \
                and s.lemma_ not in set(stopwords.words('english')):
            print(s.lemma_)
            lemmas.append(s.lemma_)
        # print(list(['lemma "{}" from text "{}"'.format(t.lemma_, t.text)
        #             for t in s]))
    freq = FreqDist(lemmas)
    print(freq.most_common(10))

    # text = text.lower()
    #
    # tokens = [word for word in tokens if
    #           word not in string.punctuation]
    # tokens = [word for word in tokens if word not in set(stopwords.words('russian'))]
    # tokens = [word for word in tokens if word not in set(stopwords.words('english'))]
    # wordnet_lemmatizer = WordNetLemmatizer()
    # print(tokens)
    # tokens = [wordnet_lemmatizer.lemmatize(word) for word in tokens]
    # print(tokens)
    # freq = FreqDist(tokens)
    # print(freq.most_common(5))
    return text


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(do_find_one())
