import asyncio
import sqlite3
import time
# import pickle
import dill as pickle

import spacy
import stanfordnlp

from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from nltk import RegexpTokenizer, FreqDist
from nltk.corpus import stopwords
from spacy.lang.ru import Russian
from prefix_codes import gamma_coding as gamma, delta_coding as delta

# from Project_parser.parsers.HTMLParser import HTMLParser


class InvertedIndex:
    def __init__(self, data_collection, db_port=27017, data_db='crawler'):
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
        # print(time.time() - start_time)
        # self.create()
        # print(time.time() - start_time)
        # self.dump('uncompressed_index_full5.pickle')
        # print(time.time() - start_time)
        # self.search('санкт-петербург')
        # self.search('кропочев')
        # self.search('университет')
        # self.search('санкт-петербургский')
        # self.search('здравствуйте')
        # self.search('петросян')
        # print(time.time() - start_time)
        # self.dump_index('compressed_index.pickle')
        # self.search('Москва')

    def compress_gamma(self):
        for word in self.global_index:
            for pair in self.global_index[word]:
                pair = (bytes(gamma(pair[0]), 'utf-8'),
                        bytes(gamma(pair[1])), 'utf-8')

    def compress_delta(self):
        for word in self.global_index:
            for pair in self.global_index[word]:
                pair = (delta(pair[0]), delta(pair[1]))

    def dump(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.global_index, file)

    def load(self, filename):
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
            if self.doc_iter > 40000:
                return
            self.doc_urls[self.doc_iter] = document['url']
            self.doc_urls[document['url']] = self.doc_iter
            self.add_to_index(document, self.doc_iter)
            if i % 100 == 0:
                # print(self.global_index)
                print(i, time.time() - start_time)
            i += 1

    def add_to_index(self, document, doc_id):
        # parser = HTMLParser(text=document['data'])
        text = document['data']

        # print(1)

        nlp = Russian()
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(text)
        tokens = [token.lower() for token in tokens]
        tmp_text = ' '.join(tokens)
        if len(tokens) > 10e5:
            return
        self.doc_iter += 1
        nlp.max_length = 10e7
        doc_text = nlp(tmp_text, disable=['ner', 'parser'])
        lemmas = []
        # for lemma in tokens:
        for s in doc_text:
            lemma = s.lemma_
            lemmas.append(lemma)
            # if lemma not in set(stopwords.words('russian')) \
        #             and lemma not in set(stopwords.words('english')) \
        #             and len(lemma) > 1:
        #         lemmas.append(lemma)
        freq = FreqDist(lemmas)
        for k, v in freq.most_common():
            if k not in self.global_index:
                self.global_index[k] = []
            self.global_index[k].append((doc_id, v))

        # print(self.global_index)
        # input()

    async def count(self):
        return await self.db_data[self.collection].count_documents({})


if __name__ == '__main__':
    start_time = time.time()
    index = InvertedIndex('spbu.ru', 27017)
    # print(time.time() - start_time)
    # #index.load('uncompressed_index_full2.pickle')
    # index.create()
    # print(time.time() - start_time)
    # # index.compress_gamma()
    # #index.compress_delta()
    # print(time.time() - start_time)
    # index.dump('new_uncompressed_index2020.pickle')
    # print(time.time() - start_time)