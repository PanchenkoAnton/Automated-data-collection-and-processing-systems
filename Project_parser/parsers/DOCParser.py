import re
import textract

from Project_parser.parsers.Parser import Parser


class DOCParser(Parser):
    """
    Parses all text and links from PDF files
    """
    def __init__(self, filepath):
        self.filepath = filepath

    def get_text(self):
        return textract.process(self.filepath).decode()

    def get_links(self):
        links = []
        link_re = re.compile(self.LINK_RE_PATTERN, (re.M | re.I))
        text = self.get_text()
        for line in text:
            result = link_re.search(line)
            result_text = result.groups()
            links.append(result_text)
        return links
