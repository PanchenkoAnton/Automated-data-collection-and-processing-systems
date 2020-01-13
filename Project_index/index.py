import asyncio
import sqlite3
import time
import pickle
import stanfordnlp

from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from nltk import RegexpTokenizer, FreqDist
from nltk.corpus import stopwords
from spacy.lang.ru import Russian
from prefix_codes import gamma_coding as gamma, delta_coding as delta

from Project_parser.parsers.HTMLParser import HTMLParser


class InvertedIndex:
    def __init__(self, data_collection, db_port, data_db='crawler'):
        self.client = MongoClient('localhost', db_port)
        self.db_data = self.client[data_db]
        self.collection = self.db_data[data_collection]
        # self.db_data = AsyncIOMotorClient('localhost', db_port)
        # self.collection = data_collection
        # self.loop = asyncio.get_event_loop()
        # self.documents_count = self.loop.run_until_complete(self.count())
        # self.loop.run_until_complete(self.create())
        self.global_index = {}
        self.doc_urls = {}
        self.doc_iter = 1
        self.create()
        self.dump_index('uncompressed_index.pickle')
        # self.compress_index()
        # self.dump_index('compressed_index.pickle')
        # self.search('Москва')

    def compress_index(self):
        for word in self.global_index:
            for pair in self.global_index[word]:
                pair = (gamma(pair[0]), gamma(pair[1]))

    def dump_index(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.global_index, file)

    def load_index(self, filename):
        with open(filename, 'rb') as file:
            self.global_index = pickle.load(file)

    def search(self, query):
        response = []
        if query in self.global_index:
            for pair in self.global_index[query]:
                doc_id, count = pair[0], pair[1]
                response.append(self.doc_urls[doc_id])
        else:
            print("Unfortunately there are no results for your query."
                  "Try another one.")
        print(response)

    def create(self):
        start_time = time.time()
        i = 1
        for document in self.collection.find():
            self.doc_urls[self.doc_iter] = document['url']
            self.doc_iter += 1
            self.add_to_index(document, self.doc_iter - 1)
            if i % 100 == 0:
                # print(self.global_index)
                print(i, time.time() - start_time)
            i += 1

    def add_to_index(self, document, doc_id):
        parser = HTMLParser(text=document['data'])
        text = parser.get_text()

        nlp = Russian()
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(text)
        # cleared_tokens = []
        # for token in tokens:
        #     if token not in set(stopwords.words('russian')) \
        #             and token not in set(stopwords.words('english')):
        #         cleared_tokens.append(token)
        # for token in cleared_tokens:
        #     if token in tf:
        #         pass
        #     else:
        #         tf[token] =
        tokens = [token.lower() for token in tokens]
        tmp_text = ' '.join(tokens)
        doc_text = nlp(tmp_text)
        lemmas = []
        for s in doc_text:
            lemma = s.lemma_
            if lemma not in set(stopwords.words('russian')) \
                    and lemma not in set(stopwords.words('english')) \
                    and len(lemma) > 1:
                lemmas.append(lemma)
        freq = FreqDist(lemmas)
        for k, v in freq.most_common():
            if k not in self.global_index:
                self.global_index[k] = []
            self.global_index[k].append((doc_id, v))

        # print(self.global_index)
        # input()

    async def count(self):
        return await self.db_data[self.collection].count_documents({})

    # async def create(self):
    #     # self.global_tf = {}
    #     async for document in self.db_data[self.collection].find():
    #         print(self.create_local_index(document))
    #         input()
    #         # self.global_index = self.merge_indexes(
    #         #     self.global_index, self.process_local_index(document)
    #         # )
    #         # self.global_tf = self.merge_tf(self.global_tf, self.make_document_tf(document))
    #         # print(self.global_tf)


if __name__ == '__main__':
    index = InvertedIndex('msu', 27017)
