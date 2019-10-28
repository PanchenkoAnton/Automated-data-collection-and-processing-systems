from Document_Parser import Parser
from PyPDF2 import PdfFileReader

import textract


class PDFParser(Parser):
    """
    Parses all text and links from PDF files
    """
    def __init__(self, filepath):
        self.filepath = filepath

    def get_text(self):
        # return textract.process(self.filepath)
        with open(self.filepath, 'rb') as file:
            pdf = PdfFileReader(file)
            info = pdf.getDocumentInfo()
            pages_num = pdf.getNumPages()
            print(info)
            print(f'There are {pages_num} pages in that file')
            for i in range(pages_num):
                page = pdf.getPage(i)
                print(f'This is the text extracted from page #{i+1}:')
                print(page.extractText())

    def get_links(self):
        links = []
        text = self.get_text()
        return links


parser = PDFParser('test.pdf')
print(parser.get_text())
