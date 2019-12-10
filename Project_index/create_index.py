import asyncio

from motor.motor_asyncio import AsyncIOMotorClient
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from spacy.lang.ru import Russian

from Project_parser.parsers.HTMLParser import HTMLParser


class Index:

    def __init__(self, collection, db='crawler', db_host='localhost', db_port=27017):
        self.db = AsyncIOMotorClient(db_host, db_port)[db]
        self.collection = collection
        self.create_index()

    def create_index(self):
        self.loop = asyncio.get_event_loop()
        self.documents_count = self.loop.run_until_complete(self.do_count())
        self.loop.run_until_complete(self.create())

    async def do_count(self):
        return await self.db[self.collection].count_documents({})

    async def create(self):
        self.global_tf = {}
        async for document in self.db[self.collection].find():
            self.global_tf = self.merge_tf(self.global_tf, self.make_document_tf(document))
            # print(self.global_tf)

    def make_document_tf(self, document):
        tf = {}
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

        # TODO most_common -> all
        for k, v in freq.most_common(10):
            tf = self.update_tf(tf, k, document['url'], v)

        return tf

    def update_tf(self, d, k, document, count):
        if k in d:
            d[k].append((document, count))
        else:
            d[k] = [(count, document)]
        return d

    def merge_tf(self, global_tf, local_tf):
        for key in local_tf.keys():
            if key in global_tf:
                global_tf[key].extend(local_tf[key])
            else:
                global_tf[key] = local_tf[key]
        return global_tf


if __name__ == "__main__":
    index = Index('msu', db_port=27000)
    print(index.global_tf)
