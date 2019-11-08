#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from Project_parser.parsers import DOCParser


class DocParserGetTextTest(unittest.TestCase):

    def test_empty_file(self):
        parser = DOCParser.DOCParser("../.data/empty.doc")
        text = parser.get_text()
        self.assertEqual("", text)

    def test_simple_text(self):
        parser = DOCParser.DOCParser("../.data/hello_world.doc")
        text = parser.get_text()
        self.assertEqual('Hello, world!', text)

    def test_ascii_text(self):
        parser = DOCParser.DOCParser("../.data/ascii.doc")
        text = parser.get_text()
        self.assertEqual('╚◙Ї§○ї', text)

    def test_russian(self):
        parser = DOCParser.DOCParser("../.data/russian.doc")
        text = parser.get_text()
        self.assertEqual('Привет, мир!', text)

    def test_multiple_lines(self):
        parser = DOCParser.DOCParser("../.data/multiple_lines.doc")
        text = parser.get_text()
        self.assertEqual('Document Title\n\nExample bold and some italic.\n\nHeading, level 1\n\nIntense quote', text)

    def test_special_symbols(self):
        test_text = "`@#$%^&*()_+-=[]{}:;\"|\\'<,>.?/"
        parser = DOCParser.DOCParser("../.data/special_symbols.doc")
        text = parser.get_text()
        self.assertEqual(test_text, text)

    def test_with_image(self):
        parser = DOCParser.DOCParser("../.data/with_image.doc")
        text = parser.get_text()
        self.assertEqual('Hello, world!\n\n\n\nHello!', text)

    def test_link(self):
        parser = DOCParser.DOCParser("../.data/link.doc")
        text = parser.get_text()
        link = parser.get_links()
        self.assertEqual('Hello, world!\n\nHello! Link', text)
        self.assertEqual(['spbu.ru'], link)

    def test_multiple_links(self):
        parser = DOCParser.DOCParser("../.data/multiple_links.doc")
        link = parser.get_links()
        text = parser.get_text()
        self.assertEqual(["spbu.ru", "http://www.apmath.spbu.ru"], link)
        self.assertEqual('Hello, world!\n\nHello! Link1\n\n\n\nParagraph with another link Link2', text)

    def test_links_in_text(self):
        parser = DOCParser.DOCParser("../.data/links_in_text.doc")
        link = parser.get_links()
        text = parser.get_text()
        self.assertEqual(["spbu.ru"], link)
        self.assertEqual('Hello, world!\n\nHello! Link1\n\nParagraph with link (http://www.apmath.spbu.ru) in text', text)


if __name__ == '__main__':
    unittest.main()
