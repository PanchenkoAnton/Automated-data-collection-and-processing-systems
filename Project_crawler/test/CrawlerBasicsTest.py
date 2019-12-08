import json
import unittest

from scrapy.crawler import CrawlerProcess

from Project_crawler.crawlers_for_testing import BasicsSinglePageCrawler, \
    BasicsTwoPagesCrawler, BasicsManyPagesCrawler, BasicsLoopPagesCrawler, \
    DoubleSlashDisallowedStartCrawler, DoubleSlashDisallowedMiddleCrawler, \
    DoubleSlashDisallowedEndCrawler, HTTPNonWWWCrawler, HTTPCrawler, \
    HTTPSCrawler, URLWithForeignCharactersCrawler, \
    ForeignCharacterDomainCrawler


class CrawlerBasicsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                          '(KHTML,'
                          ' like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            'HTTPCACHE_ENABLED': True,
            'AUTOTHROTTLE_ENABLED': True,
            'HTTPERROR_ALLOWED_CODES': [404, 403, 504, 503, 301],
            'HTTPERROR_ALLOW_ALL': True,
            'AUTOTHROTTLE_TARGET_CONCURRENCY': 2.0,
            'CONCURRENT_REQUESTS_PER_DOMAIN': 33,
            'CONCURRENT_REQUESTS': 33,
            'LOG_LEVEL': 'INFO',
            'FEED_FORMAT': 'jsonlines',
            'FEED_URI': 'output.json'
        })
        process.crawl(BasicsSinglePageCrawler)
        process.crawl(BasicsTwoPagesCrawler)
        process.crawl(BasicsManyPagesCrawler)
        process.crawl(BasicsLoopPagesCrawler)
        process.crawl(DoubleSlashDisallowedStartCrawler)
        process.crawl(DoubleSlashDisallowedMiddleCrawler)
        process.crawl(DoubleSlashDisallowedEndCrawler)
        process.crawl(HTTPNonWWWCrawler)
        process.crawl(HTTPCrawler)
        process.crawl(HTTPSCrawler)
        process.crawl(URLWithForeignCharactersCrawler)
        process.crawl(ForeignCharacterDomainCrawler)
        process.start()

    def test_basics_single_page(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == BasicsSinglePageCrawler.start_urls[0]:
                    self.assertEqual(line['stats']['statuses']['200'][0], 1)

    def test_basics_two_pages(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == BasicsSinglePageCrawler.start_urls[0]:
                    self.assertEqual(line['stats']['statuses']['200'][0], 2)

    def test_basics_many_pages(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == BasicsManyPagesCrawler.start_urls[0]:
                    self.assertEqual(line['stats']['statuses']['200'][0], 5)

    def test_basics_loop_pages(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == BasicsLoopPagesCrawler.start_urls[0]:
                    self.assertEqual(line['stats']['statuses']['200'][0], 3)

    def test_double_slash_disallowed_start(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == DoubleSlashDisallowedStartCrawler.start_urls[0]:
                    self.assertEqual(line['stats']['statuses']['200'][0], 1)

    def test_double_slash_disallowed_middle(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == DoubleSlashDisallowedMiddleCrawler.start_urls[0]:
                    self.assertEqual(line['stats']['statuses']['200'][0], 1)

    def test_double_slash_disallowed_end(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == DoubleSlashDisallowedEndCrawler.start_urls[0]:
                    self.assertEqual(line['stats']['statuses']['200'][0], 1)

    def test_http_non_www(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == HTTPNonWWWCrawler.start_urls[0]:
                    self.assertEqual(line['stats']['statuses']['200'][0], 1)

    def test_http(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == HTTPCrawler.start_urls[0]:
                    self.assertEqual(line['stats']['statuses']['200'][0], 1)

    def test_https(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == HTTPSCrawler.start_urls[0]:
                    self.assertEqual(line['stats']['statuses']['200'][0], 1)

    def test_url_with_foreign_characters(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == URLWithForeignCharactersCrawler.start_urls[0]:
                    self.assertEqual(line['stats']['statuses']['200'][0], 1)

    def test_foreign_characters_domain(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == ForeignCharacterDomainCrawler.start_urls[0]:
                    self.assertEqual(line['stats']['statuses']['200'][0], 1)


if __name__ == '__main__':
    unittest.main()
