#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from Project_index.index import InvertedIndex
import pymongo


class IndexTest(unittest.TestCase):

    def test_empty_doc(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["test_index"]
        test_name = 'test_empty_doc'
        if test_name in db.list_collection_names():
            db[test_name].drop()
        db[test_name].insert_one({"url": "link1", "data": ""})

        index = InvertedIndex(test_name, data_db="test_index")
        index.create()
        handmade_index = {}
        self.assertEqual(index.global_index, handmade_index)

    def test_empty_docs(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["test_index"]
        test_name = 'test_empty_docs'
        if test_name in db.list_collection_names():
            db[test_name].drop()
        db[test_name].insert_one({"url": "link1", "data": ""})
        db[test_name].insert_one({"url": "link2", "data": ""})

        index = InvertedIndex(test_name, data_db="test_index")
        index.create()
        handmade_index = {}
        self.assertEqual(index.global_index, handmade_index)

    def test_one_doc_only_punctuation(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["test_index"]
        test_name = 'test_one_doc_only_punctuation'
        if test_name in db.list_collection_names():
            db[test_name].drop()
        db[test_name].insert_one({"url": "link1", "data": ", :'\"\\|/&   !"})

        index = InvertedIndex(test_name, data_db="test_index")
        index.create()
        handmade_index = {}
        self.assertEqual(index.global_index, handmade_index)

    def test_one_doc_lowercase(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["test_index"]
        test_name = 'test_one_doc_lowercase'
        if test_name in db.list_collection_names():
            db[test_name].drop()
        db[test_name].insert_one({"url": "link1", "data": "WORD Word wORD word"})

        index = InvertedIndex(test_name, data_db="test_index")
        index.create()
        handmade_index = {'word': [(index.doc_urls['link1'], 4)]}
        self.assertEqual(index.global_index, handmade_index)

    def test_one_doc_one_word(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["test_index"]
        test_name = 'test_one_doc_one_word'
        if test_name in db.list_collection_names():
            db[test_name].drop()
        db[test_name].insert_one({"url": "link1", "data": "word"})

        index = InvertedIndex(test_name, data_db="test_index")
        index.create()
        handmade_index = {'word': [(index.doc_urls['link1'], 1)]}
        self.assertEqual(index.global_index, handmade_index)

    def test_one_doc_many_words(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["test_index"]
        test_name = 'test_one_doc_many_words'
        if test_name in db.list_collection_names():
            db[test_name].drop()
        db[test_name].insert_one({"url": "link1", "data": "  word1    word2 "})

        index = InvertedIndex(test_name, data_db="test_index")
        index.create()
        handmade_index = {'word1': [(index.doc_urls['link1'], 1)], 'word2': [(index.doc_urls['link1'], 1)]}
        self.assertEqual(index.global_index, handmade_index)

    def test_many_docs_one_word(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["test_index"]
        test_name = 'test_many_docs_one_word'
        if test_name in db.list_collection_names():
            db[test_name].drop()
        db[test_name].insert_one({"url": "link1", "data": "word"})
        db[test_name].insert_one({"url": "link2", "data": "word"})

        index = InvertedIndex(test_name, data_db="test_index")
        index.create()
        handmade_index = {'word': [(index.doc_urls['link1'], 1), (index.doc_urls['link2'], 1)]}
        self.assertEqual(index.global_index, handmade_index)

    def test_many_docs_many_words(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["test_index"]
        test_name = 'test_many_docs_many_words'
        if test_name in db.list_collection_names():
            db[test_name].drop()
        db[test_name].insert_one({"url": "link1", "data": "word1 word2"})
        db[test_name].insert_one({"url": "link2", "data": "word2 word1"})

        index = InvertedIndex(test_name, data_db="test_index")
        index.create()
        handmade_index = {'word1': [(index.doc_urls['link1'], 1), (index.doc_urls['link2'], 1)],
                          'word2': [(index.doc_urls['link1'], 1), (index.doc_urls['link2'], 1)]}
        self.assertEqual(index.global_index, handmade_index)


if __name__ == '__main__':
    unittest.main()
