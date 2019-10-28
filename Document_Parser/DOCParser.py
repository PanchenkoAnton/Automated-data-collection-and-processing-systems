from Document_Parser import Parser

import textract


class DOCParser(Parser):
    """
    Parses all text and links from PDF files
    """
    def __init__(self, filepath):
        self.filepath = filepath

    def get_text(self):
        return textract.process(self.filepath)

    def get_links(self):
        links = []
        text = self.get_text()
        return links


parser = DOCParser('test.doc')
print(parser.get_text())
