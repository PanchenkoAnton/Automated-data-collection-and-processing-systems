#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from Project_index.create_index import Index
import pymongo


class IndexTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["test_index"]

    def test_empty_doc(self):
        test_name = 'test_empty_doc'
        if test_name in db.list_collection_names():
            db[test_name].drop()
        db[test_name].insert_one({"url": link1, "data": ""})

        index = InvertedIndex(test_name)
        index.create()
        handmade_index = {}
        self.assertEqual(index.global_index, handmade_index)

    def test_empty_docs(self):
        test_name = 'test_empty_docs'
        if test_name in db.list_collection_names():
            db[test_name].drop()
        db[test_name].insert_one({"url": link1, "data": ""})
        db[test_name].insert_one({"url": link2, "data": ""})

        index = InvertedIndex(test_name)
        index.create()
        handmade_index = {}
        self.assertEqual(index.global_index, handmade_index)

    def test_one_doc_only_punctuation(self):
        test_name = 'test_one_doc_only_punctuation'
        if test_name in db.list_collection_names():
            db[test_name].drop()
        db[test_name].insert_one({"url": link1, "data": ", :'\"\\|/&   !"})

        index = InvertedIndex(test_name)
        index.create()
        handmade_index = {}
        self.assertEqual(index.global_index, handmade_index)

    # def test_one_doc_stopwords_and_punctuation(self):
    #     test_name = 'test_one_doc_stopwords_and_punctuation'
    #     if test_name in db.list_collection_names():
    #         db[test_name].drop()
    #     db[test_name].insert_one({"url": link1, "data": "and,  :'\"\\|/by&   !or"})
    #
    #     index = InvertedIndex(test_name)
    #     index.create()
    #     handmade_index = {}
    #     self.assertEqual(index.global_index, handmade_index)
    #
    # def test_one_doc_only_stopwords(self):
    #     test_name = 'test_one_doc_only_stopwords'
    #     if test_name in db.list_collection_names():
    #         db[test_name].drop()
    #     db[test_name].insert_one({"url": link1, "data": " and by or"})
    #
    #     index = InvertedIndex(test_name)
    #     index.create()
    #     handmade_index = {}
    #     self.assertEqual(index.global_index, handmade_index)
    #
    # def test_one_doc_lemmas(self):
    #     test_name = 'test_one_doc_lemmas'
    #     if test_name in db.list_collection_names():
    #         db[test_name].drop()
    #     db[test_name].insert_one({"url": link1, "data": "swim swam swimming"})
    #
    #     index = InvertedIndex(test_name)
    #     index.create()
    #     handmade_index = {'swim': [(index.doc_ids['link1'], 3)]}
    #     self.assertEqual(index.global_index, handmade_index)
    #
    # def test_one_doc_lemmas_russian(self):
    #     test_name = 'test_one_doc_lemmas_russian'
    #     if test_name in db.list_collection_names():
    #         db[test_name].drop()
    #     db[test_name].insert_one({"url": link1, "data": "экзамен экзамены экзамену экзаменов"})
    #
    #     index = InvertedIndex(test_name)
    #     index.create()
    #     handmade_index = {'экзамен': [(index.doc_ids['link1'], 4)]}
    #     self.assertEqual(index.global_index, handmade_index)

    def test_one_doc_lowercase(self):
        test_name = 'test_one_doc_lowercase'
        if test_name in db.list_collection_names():
            db[test_name].drop()
        db[test_name].insert_one({"url": link1, "data": "WORD Word wORD word"})

        index = InvertedIndex(test_name)
        index.create()
        handmade_index = {'word': [(index.doc_ids['link1'], 4)]}
        self.assertEqual(index.global_index, handmade_index)

    def test_one_doc_one_word(self):
        test_name = 'test_one_doc_one_word'
        if test_name in db.list_collection_names():
            db[test_name].drop()
        db[test_name].insert_one({"url": link1, "data": "word"})

        index = InvertedIndex(test_name)
        index.create()
        handmade_index = {'word': [(index.doc_ids['link1'], 1)]}
        self.assertEqual(index.global_index, handmade_index)

    def test_one_doc_many_words(self):
        test_name = 'test_one_doc_many_words'
        if test_name in db.list_collection_names():
            db[test_name].drop()
        db[test_name].insert_one({"url": link1, "data": "  word1    word2 "})

        index = InvertedIndex(test_name)
        index.create()
        handmade_index = {'word1': [(index.doc_ids['link1'], 1)], 'word2': [(index.doc_ids['link1'], 1)]}
        self.assertEqual(index.global_index, handmade_index)

    def test_one_doc_repeated_words(self):
        test_name = 'test_one_doc_repeated_words'
        if test_name in db.list_collection_names():
            db[test_name].drop()
        db[test_name].insert_one({"url": link1, "data": " word1 word2 word1 word2 word1 word2 word1 "})

        index = InvertedIndex(test_name)
        index.create()
        handmade_index = {'word1': [(index.doc_ids['link1'], 5)], 'word2': [(index.doc_ids['link1'], 3)]}
        self.assertEqual(index.global_index, handmade_index)

    def test_many_docs_one_word(self):
        test_name = 'test_many_docs_one_word'
        if test_name in db.list_collection_names():
            db[test_name].drop()
        db[test_name].insert_one({"url": link1, "data": "word"})
        db[test_name].insert_one({"url": link2, "data": "word"})

        index = InvertedIndex(test_name)
        index.create()
        handmade_index = {'word': [(index.doc_ids['link1'], 1), (index.doc_ids['link2'], 1)]}
        self.assertEqual(index.global_index, handmade_index)

    def test_many_docs_many_words(self):
        test_name = 'test_many_docs_many_words'
        if test_name in db.list_collection_names():
            db[test_name].drop()
        db[test_name].insert_one({"url": link1, "data": "word1 word2"})
        db[test_name].insert_one({"url": link2, "data": "word2 word1"})

        index = InvertedIndex(test_name)
        index.create()
        handmade_index = {'word1': [(index.doc_ids['link1'], 1), (index.doc_ids['link2'], 1)],
                          'word2': [(index.doc_ids['link1'], 1), (index.doc_ids['link2'], 1)]}
        self.assertEqual(index.global_index, handmade_index)

    def test_many_docs_repeated_words(self):
        test_name = 'test_many_docs_repeated_words'
        if test_name in db.list_collection_names():
            db[test_name].drop()
        db[test_name].insert_one({"url": link1, "data": " word1 word2 word1 word2 word1 word2 word1 "})
        db[test_name].insert_one({"url": link2, "data": " word2 word1 word2 word1 word2 word1 word2 "})

        index = InvertedIndex(test_name)
        index.create()
        handmade_index = {'word1': [(index.doc_ids['link1'], 5), (index.doc_ids['link2'], 3)],
                          'word2': [(index.doc_ids['link1'], 3), (index.doc_ids['link2'], 5)]}
        self.assertEqual(index.global_index, handmade_index)

    def test_many_docs_repeated_words_stopwords_and_punctuation(self):
        test_name = 'test_many_docs_repeated_words_stopwords_and_punctuation'
        if test_name in db.list_collection_names():
            db[test_name].drop()
        db[test_name].insert_one({"url": link1, "data": " word1 and word2 or word1 by word2 word1 word2 word1 "})
        db[test_name].insert_one({"url": link2, "data": " word2; word1, word2 . word1 .word2 word1. \"word2\" "})

        index = InvertedIndex(test_name)
        index.create()
        handmade_index = {'word1': [(index.doc_ids['link1'], 5), (index.doc_ids['link2'], 3)],
                          'word2': [(index.doc_ids['link1'], 3), (index.doc_ids['link2'], 5)]}
        self.assertEqual(index.global_index, handmade_index)


if __name__ == '__main__':
    unittest.main()
