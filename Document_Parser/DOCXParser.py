from Document_Parser.Parser import Parser

import docxpy


class DOCXParser(Parser):
    """
    Parses all text and links from PDF files
    """

    def __init__(self, filepath):
        self.filepath = filepath

    def get_text(self):
        return docxpy.process(self.filepath)

    def get_links(self):
        doc = docxpy.DOCReader(self.filepath)
        doc.process()
        links = []
        for pair in doc.data['links']:
            links.append(pair[1])
        return links
