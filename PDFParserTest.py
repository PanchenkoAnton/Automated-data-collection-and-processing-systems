#! /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from Document_Parser import PDFParser
from fpdf import FPDF


def get_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    return pdf


class PDFParserGetTextTest(unittest.TestCase):

    def test_empty_file(self):
        pdf = get_pdf()
        pdf.cell(0, txt="1")
        pdf.output(".data/empty.pdf")
        parser = PDFParser.PDFParser(".data/empty.pdf")
        text = parser.get_text()
        self.assertEqual(["1"], text)

    def test_simple_text(self):
        pdf = get_pdf()
        pdf.cell(0, txt="Hello World!")
        pdf.output(".data/hello_world.pdf")
        parser = PDFParser.PDFParser(".data/hello_world.pdf")
        text = parser.get_text()
        self.assertEqual(['Hello World!'], text)

    def test_russian(self):
        pdf = get_pdf()
        pdf.cell(0, txt="Привет")
        pdf.output(".data/russian.pdf")
        parser = PDFParser.PDFParser(".data/russian.pdf")
        text = parser.get_text()
        self.assertEqual(['Привет'], text)

    def test_multiple_lines(self):
        pdf = get_pdf()
        pdf.cell(200, 10, txt="Hello", ln=1, align="L")
        pdf.cell(200, 10, txt="World", ln=1, align="R")
        pdf.cell(200, 10, txt="", ln=1, align="с")
        pdf.cell(200, 10, txt="!", ln=1, align="C")
        pdf.output(".data/multiple_lines.pdf")
        parser = PDFParser.PDFParser(".data/multiple_lines.pdf")
        text = parser.get_text()
        self.assertEqual(['HelloWorld!'], text)

    def test_special_symbols(self):
        pdf = get_pdf()
        test_text = "`@#$%^&*()_+-=[]{}:;\"|\\'<,>.?/"
        pdf.cell(200, 10, txt=test_text)
        pdf.output(".data/special_symbols.pdf")
        parser = PDFParser.PDFParser(".data/special_symbols.pdf")
        text = parser.get_text()
        self.assertEqual([test_text], text)

    def test_with_image(self):
        pdf = get_pdf()
        pdf.cell(200, 10, txt="Hello")
        pdf.image(".data/korablik-parusnik-model.jpg", x=10, y=8, w=100)
        pdf.cell(200, 10, txt="World")
        pdf.output(".data/with_image.pdf")
        parser = PDFParser.PDFParser(".data/with_image.pdf")
        text = parser.get_text()
        self.assertEqual(["HelloWorld"], text)

    def test_multiple_pages(self):
        pdf = get_pdf()
        pdf.cell(200, 10, txt="Hello")
        pdf.add_page()
        pdf.cell(200, 10, txt="World", ln=2)
        pdf.output(".data/multiple_pages.pdf")
        parser = PDFParser.PDFParser(".data/multiple_pages.pdf")
        text = parser.get_text()
        self.assertEqual(["Hello", "World"], text)

    def test_link(self):
        pdf = get_pdf()
        pdf.cell(0, txt="Hello")
        pdf.link(x=5, y=0, w=10, h=10, link="spbu.ru")
        pdf.cell(0, txt="World")
        pdf.output(".data/link.pdf")
        parser = PDFParser.PDFParser(".data/link.pdf")
        text = parser.get_text()
        links = parser.get_links()
        self.assertEqual(["HelloWorld"], text)
        self.assertEqual(["spbu.ru"], links)

    def test_multiple_links(self):
        pdf = get_pdf()
        pdf.cell(0, txt="Hello")
        pdf.link(x=5, y=0, w=10, h=10, link="spbu.ru")
        pdf.link(x=5, y=0, w=10, h=10, link="http://www.apmath.spbu.ru")
        pdf.cell(0, txt="World")
        pdf.output(".data/multiple_links.pdf")
        parser = PDFParser.PDFParser(".data/multiple_links.pdf")
        text = parser.get_text()
        links = parser.get_links()
        self.assertEqual(["HelloWorld"], text)
        self.assertEqual(["spbu.ru", "http://www.apmath.spbu.ru"], links)


if __name__ == '__main__':
    unittest.main()
