#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from parsers import PDFParser
from fpdf import FPDF


def get_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    return pdf


class PDFParserGetTextTest(unittest.TestCase):

    def test_empty_file(self):
        filename = "../.data/empty.pdf"
        pdf = get_pdf()
        pdf.cell(0, txt="")
        pdf.output(filename)
        parser = PDFParser.PDFParser(filename)
        text = parser.get_text()
        self.assertEqual([""], text)

    def test_simple_text(self):
        filename = "../.data/hello_world.pdf"
        pdf = get_pdf()
        pdf.cell(0, txt="Hello World!")
        pdf.output(filename)
        parser = PDFParser.PDFParser(filename)
        text = parser.get_text()
        self.assertEqual(['Hello World!'], text)

    def test_ascii_text(self):
        filename = "../.data/ascii.pdf"
        parser = PDFParser.PDFParser(filename)
        text = parser.get_text()
        self.assertEqual('', text)

    def test_russian(self):
        filename = "../.data/russian.pdf"
        parser = PDFParser.PDFParser(filename)
        text = parser.get_text()
        self.assertEqual(['Привет, мир!'], text)

    def test_multiple_lines(self):
        filename = "../.data/multiple_lines.pdf"
        pdf = get_pdf()
        pdf.cell(200, 10, txt="Hello", ln=1, align="L")
        pdf.cell(200, 10, txt="World", ln=1, align="R")
        pdf.cell(200, 10, txt="", ln=1, align="с")
        pdf.cell(200, 10, txt="!", ln=1, align="C")
        pdf.output(filename)
        parser = PDFParser.PDFParser(filename)
        text = parser.get_text()
        self.assertEqual(['HelloWorld!'], text)

    def test_special_symbols(self):
        filename = "../.data/special_symbols.pdf"
        pdf = get_pdf()
        test_text = "`@#$%^&*()_+-=[]{}:;\"|\\'<,>.?/"
        pdf.cell(200, 10, txt=test_text)
        pdf.output(filename)
        parser = PDFParser.PDFParser(filename)
        text = parser.get_text()
        self.assertEqual([test_text], text)

    def test_with_image(self):
        filename = "../.data/with_image.pdf"
        pdf = get_pdf()
        pdf.cell(200, 10, txt="Hello")
        pdf.image("../.data/korablik-parusnik-model.jpg", x=10, y=8, w=100)
        pdf.cell(200, 10, txt="World")
        pdf.output(filename)
        parser = PDFParser.PDFParser(filename)
        text = parser.get_text()
        self.assertEqual(["HelloWorld"], text)

    def test_multiple_pages(self):
        filename = "../.data/multiple_pages.pdf"
        pdf = get_pdf()
        pdf.cell(200, 10, txt="Hello")
        pdf.add_page()
        pdf.cell(200, 10, txt="World", ln=2)
        pdf.output(filename)
        parser = PDFParser.PDFParser(filename)
        text = parser.get_text()
        self.assertEqual(["Hello", "World"], text)

    def test_link(self):
        filename = "../.data/link.pdf"
        pdf = get_pdf()
        pdf.cell(0, txt="Hello")
        pdf.link(x=5, y=0, w=10, h=10, link="spbu.ru")
        pdf.cell(0, txt="World")
        pdf.output(filename)
        parser = PDFParser.PDFParser(filename)
        text = parser.get_text()
        links = parser.get_links()
        self.assertEqual(["HelloWorld"], text)
        self.assertEqual(["spbu.ru"], links)

    def test_multiple_links(self):
        filename = "../.data/multiple_links.pdf"
        pdf = get_pdf()
        pdf.cell(0, txt="Hello")
        pdf.link(x=5, y=0, w=10, h=10, link="spbu.ru")
        pdf.link(x=5, y=0, w=10, h=10, link="http://www.apmath.spbu.ru")
        pdf.cell(0, txt="World")
        pdf.output(filename)
        parser = PDFParser.PDFParser(filename)
        text = parser.get_text()
        links = parser.get_links()
        self.assertEqual(["HelloWorld"], text)
        self.assertEqual(["spbu.ru", "http://www.apmath.spbu.ru"], links)

    def test_links_in_text(self):
        filename = "../.data/links_in_text.pdf"
        pdf = get_pdf()
        pdf.cell(0, txt="Hello http://www.spbu.ru World")
        pdf.link(x=5, y=0, w=10, h=10, link="http://www.apmath.spbu.ru")
        pdf.output(filename)
        parser = PDFParser.PDFParser(filename)
        text = parser.get_text()
        links = parser.get_links()
        self.assertEqual(["Hello http://www.spbu.ru World"], text)
        self.assertEqual(["http://www.apmath.spbu.ru"], links)


if __name__ == '__main__':
    unittest.main()
