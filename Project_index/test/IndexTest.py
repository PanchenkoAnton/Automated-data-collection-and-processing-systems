#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from Project_index.create_index import Index


class IndexTest(unittest.TestCase):

    def test_empty_doc(self):
        index = Index('test_empty_doc')
        test_tf = {}
        self.assertEqual(index.global_tf, test_tf)

    def test_empty_docs(self):
        index = Index('test_empty_docs')
        test_tf = {}
        self.assertEqual(index.global_tf, test_tf)

    def test_one_doc_only_stopwords(self):
        index = Index('test_one_doc_only_stopwords')
        test_tf = {}
        self.assertEqual(index.global_tf, test_tf)

    def test_one_doc_only_punctuation(self):
        index = Index('test_one_doc_only_punctuation')
        test_tf = {}
        self.assertEqual(index.global_tf, test_tf)

    def test_one_doc_stopwords_and_punctuation(self):
        index = Index('test_one_doc_stopwords_and_punctuation')
        test_tf = {}
        self.assertEqual(index.global_tf, test_tf)

    def test_one_doc_lemmas(self):
        index = Index('test_one_doc_lemmas')  # swim swam swimming
        test_tf = {'swim': [(3, 'link1')]}
        self.assertEqual(index.global_tf, test_tf)

    def test_one_doc_lemmas_russian(self):
        index = Index('test_one_doc_lemmas_russian')  # экзамен экзамены экзамену экзаменов
        test_tf = {'экзамен': [(4, 'link1')]}
        self.assertEqual(index.global_tf, test_tf)

    def test_one_doc_lowercase(self):
        index = Index('test_one_doc_lowercase')  # WORD Word wORD word
        test_tf = {'word': [(4, 'link1')]}
        self.assertEqual(index.global_tf, test_tf)

    def test_one_doc_one_word(self):
        index = Index('test_one_doc_one_word')
        test_tf = {'word': [(1, 'link1')]}
        self.assertEqual(index.global_tf, test_tf)

    def test_one_doc_many_words(self):
        index = Index('test_one_doc_many_words')
        test_tf = {'word1': [(1, 'link1')], 'word2': [(1, 'link1')]}
        self.assertEqual(index.global_tf, test_tf)

    def test_one_doc_repeated_words(self):
        index = Index('test_one_doc_repeated_word')
        test_tf = {'word1': [(5, 'link1')], 'word2': [(3, 'link1')]}
        self.assertEqual(index.global_tf, test_tf)

    def test_many_docs_one_word(self):
        index = Index('test_many_doc_one_word')
        test_tf = {'word': [(1, 'link1'), (1, 'link2')]}
        self.assertEqual(index.global_tf, test_tf)

    def test_many_docs_many_words(self):
        index = Index('test_many_docs_many_words')
        test_tf = {'word1': [(1, 'link1'), (1, 'link2')], 'word2': [(1, 'link1'), (1, 'link2')]}
        self.assertEqual(index.global_tf, test_tf)

    def test_many_docs_repeated_words(self):
        index = Index('test_many_docs_repeated_words')
        test_tf = {'word1': [(5, 'link1'), (3, 'link2')], 'word2': [(3, 'link1'), (5, 'link2')]}
        self.assertEqual(index.global_tf, test_tf)

    def test_many_docs_repeated_words_stopwords_and_punctuation(self):
        index = Index('test_many_docs_repeated_words_stopwords_and_punctuation')
        test_tf = {'word1': [(5, 'link1'), (3, 'link2')], 'word2': [(3, 'link1'), (5, 'link2')]}
        self.assertEqual(index.global_tf, test_tf)


if __name__ == '__main__':
    unittest.main()
