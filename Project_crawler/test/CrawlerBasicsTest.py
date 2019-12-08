import json
import unittest

from scrapy.crawler import CrawlerProcess

from Project_crawler.crawlers_for_testing import BasicsSinglePageCrawler, \
    BasicsTwoPagesCrawler, BasicsManyPagesCrawler, BasicsLoopPagesCrawler


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
        process.start()

    def test_basics_single_page(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == BasicsSinglePageCrawler.start_urls[0]:
                    self.assertEqual(line['stats']['count'], 1)

    def test_basics_two_pages(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == BasicsSinglePageCrawler.start_urls[0]:
                    self.assertEqual(line['stats']['count'], 2)

    def test_basics_many_pages(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == BasicsManyPagesCrawler.start_urls[0]:
                    self.assertEqual(line['stats']['count'], 5)

    def test_basics_loop_pages(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == BasicsLoopPagesCrawler.start_urls[0]:
                    self.assertEqual(line['stats']['count'], 3)


if __name__ == '__main__':
    unittest.main()
