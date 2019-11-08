#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from Project_parser.parsers import HTMLParser

from yattag import Doc


def create_html(html, name):
    with open('../.data/' + name + '.html', 'w') as file:
        file.write(html)


class HTMLTestGetText(unittest.TestCase):

    def test_empty(self):
        doc, tag, text = Doc().tagtext()
        with tag('html'):
            with tag('body'):
                with tag('p', id='main'):
                    pass
        result = doc.getvalue()
        create_html(result, 'empty')
        parser = HTMLParser.HTMLParser("../.data/empty.html")
        text = parser.get_text()
        self.assertEqual("", text)

    def test_simple_text(self):
        doc, tag, text = Doc().tagtext()
        with tag('html'):
            with tag('body'):
                with tag('p', id='main'):
                    text('Hello, world!')
        result = doc.getvalue()
        create_html(result, 'hello_world')
        parser = HTMLParser.HTMLParser("../.data/hello_world.html")
        text = parser.get_text()
        self.assertEqual('Hello, world!', text)

    def test_ascii_text(self):
        parser = HTMLParser.HTMLParser("../.data/ascii.html")
        text = parser.get_text()
        self.assertEqual('╚◙Ї§○ї', text)

    def test_russian(self):
        doc, tag, text = Doc().tagtext()
        with tag('html'):
            with tag('body'):
                with tag('p', id='main'):
                    text('Привет, мир!')
        result = doc.getvalue()
        create_html(result, 'russian')
        parser = HTMLParser.HTMLParser("../.data/russian.html")
        text = parser.get_text()
        self.assertEqual('Привет, мир!', text)

    def test_multiple_lines(self):
        doc, tag, text = Doc().tagtext()
        with tag('html'):
            with tag('body'):
                with tag('p', id='main'):
                    text('Hello, ')
                with tag('p', id='main'):
                    text('world')
                with tag('p'):
                    with tag('div'):
                        text('!')
        result = doc.getvalue()
        create_html(result, 'multiple_lines')
        parser = HTMLParser.HTMLParser("../.data/multiple_lines.html")
        text = parser.get_text()
        self.assertEqual('Hello, world!', text)

    def test_special_symbols(self):
        test_text = "`@#$%^&*()_+-=[]{}:;\"|\\'<,>.?/"
        doc, tag, text = Doc().tagtext()
        with tag('html'):
            with tag('body'):
                with tag('p', id='main'):
                    text(test_text)
        result = doc.getvalue()
        create_html(result, 'special_symbols')
        parser = HTMLParser.HTMLParser("../.data/special_symbols.html")
        text = parser.get_text()
        self.assertEqual(test_text, text)

    def test_with_image(self):
        doc, tag, text = Doc().tagtext()
        with tag('html'):
            with tag('body'):
                with tag('p', id='main'):
                    text('Hello, ')
                with tag('div', id='image', alt='img here'):
                    doc.stag('img', src='korablik-parusnik-model.jpg', klass="photo")
                with tag('p', id='main'):
                    text('world!')
        result = doc.getvalue()
        create_html(result, 'with_image')
        parser = HTMLParser.HTMLParser("../.data/with_image.html")
        text = parser.get_text()
        self.assertEqual('Hello, world!', text)

    def test_link(self):
        doc, tag, text = Doc().tagtext()
        with tag('html'):
            with tag('body'):
                with tag('a', href='spbu.ru'):
                    text('Hello, world!')
        result = doc.getvalue()
        create_html(result, 'link')
        parser = HTMLParser.HTMLParser("../.data/link.html")
        link = parser.get_links()
        text = parser.get_text()
        self.assertEqual(['spbu.ru'], link)
        self.assertEqual('Hello, world!', text)

    def test_multiple_links(self):
        doc, tag, text = Doc().tagtext()
        with tag('html'):
            with tag('body'):
                with tag('p', id='main'):
                    text('Hello, ')
                    with tag('p'):
                        with tag('a', href='spbu.ru'):
                            text('link1 ')
                with tag('a', href='http://www.apmath.spbu.ru'):
                    text('link2 ')
                with tag('p', id='main'):
                    text('world!')

        result = doc.getvalue()
        create_html(result, 'multiple_links')
        parser = HTMLParser.HTMLParser("../.data/multiple_links.html")
        link = parser.get_links()
        text = parser.get_text()
        self.assertEqual(["spbu.ru", "http://www.apmath.spbu.ru"], link)
        self.assertEqual('Hello, link1 link2 world!', text)

    def test_links_in_text(self):
        doc, tag, text = Doc().tagtext()
        with tag('html'):
            with tag('body'):
                with tag('p', id='main'):
                    text('Hello, http://www.apmath.spbu.ru ')
                    with tag('p'):
                        with tag('a', href='spbu.ru'):
                            text('link1 ')
                with tag('p', id='main'):
                    text('world!')

        result = doc.getvalue()
        create_html(result, 'links_in_text')
        parser = HTMLParser.HTMLParser("../.data/links_in_text.html")
        link = parser.get_links()
        text = parser.get_text()
        self.assertEqual(["spbu.ru"], link)
        self.assertEqual('Hello, http://www.apmath.spbu.ru link1 world!', text)


if __name__ == '__main__':
    unittest.main()
