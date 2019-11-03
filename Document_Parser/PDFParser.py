import re
#import textract

from Document_Parser.Parser import Parser
from PyPDF2 import PdfFileReader


class PDFParser(Parser):
    """
    Parses all text and links from PDF files
    """
    def __init__(self, filepath):
        self.filepath = filepath

    def get_text(self):
        # return textract.process(self.filepath)
        text = []
        with open(self.filepath, 'rb') as file:
            pdf = PdfFileReader(file)
            info = pdf.getDocumentInfo()
            pages_num = pdf.getNumPages()
            # print(info)
            # print(f'There are {pages_num} pages in that file')
            for i in range(pages_num):
                page = pdf.getPage(i)
                # print(f'This is the text extracted from page #{i+1}:')
                page_text = page.extractText()
                # print(page_text)
                text.append(page_text)
        return text

    def get_links(self):
        links = []
        link_re = re.compile(self.LINK_RE_PATTERN, (re.M | re.I))
        text = self.get_text()
        for page in text:
            for line in text:
                result = link_re.search(line)
                result_text = result.groups()
                # print(result)
                links.append(result_text)
        return links
