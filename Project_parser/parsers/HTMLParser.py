from bs4 import BeautifulSoup
from Project_parser.parsers.Parser import Parser


class HTMLParser(Parser):
    """
    Parses all text and links from HTML.
    Constructor args: filepath.
    """
    def __init__(self, filepath=None, text=None):
        if filepath:
            with open(filepath, 'rb') as file:
                self.bs = BeautifulSoup(file.read(), 'html.parser')
        if text:
            self.bs = BeautifulSoup(text, 'html.parser')

    def get_text(self):
        # kill all script and style elements
        for script in self.bs(['script', 'style']):
            script.extract()
        text = self.bs.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in
                  line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    def get_links(self):
        links = []
        for link in self.bs.find_all('a'):
            links.append(link.get('href'))
        return links


if __name__ == '__main__':
    parser = HTMLParser(filepath='1.html')
    print(parser.get_text())
