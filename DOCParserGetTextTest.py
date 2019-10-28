#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from Document_Parser import DOCParser


class DocParserGetTextTest(unittest.TestCase):

    def test_empty_file(self):
        parser = DOCParser.DOCParser("data/empty.html")
        text = parser.get_text()
        self.assertEqual(text, '')

    def test_empty_txt(self):
        parser = DOCParser.DOCParser("data/empty.txt")
        text = parser.get_text()
        self.assertEqual(text, '')

    def test_txt_page(self):
        parser = DOCParser.DOCParser("data/textLikeHTML.txt")
        text = parser.get_text()
        self.assertEqual(text, '\n\n\nMy First Heading\nMy first paragraph.\n\n')

    def test_html_page(self):
        parser = DOCParser.DOCParser("data/simple_page.html")
        text = parser.get_text()
        self.assertEqual(text, '\n\n\nMy First Heading\nMy first paragraph.\n\n')

    def test_russian(self):
        parser = DOCParser.DOCParser("data/russianSymbols")
        text = parser.get_text()
        self.assertEqual(text, 'Санкт-Петербургский государственный университет')


if __name__ == '__main__':
    unittest.main()
