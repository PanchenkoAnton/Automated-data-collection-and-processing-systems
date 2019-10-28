#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest


class HTMLParserTest(unittest.TestCase):

    def empty_file(self):
        text = HTMLParser.get_text('../empty.html')
        self.assertEqual(text, '')


if __name__ == '__main__':
    unittest.main()