import asyncio
import json
import unittest

from motor.motor_asyncio import AsyncIOMotorClient
from scrapy.crawler import CrawlerProcess

from Project_crawler.crawler import insert
from Project_crawler.crawlers_for_testing import BrokenLinksInternalCrawler, \
    BrokenLinksExternalCrawler, MaxExternalLinksCrawler


class MyTestCase(unittest.TestCase):
    consistency = {
        'test_broken_links_internal': BrokenLinksInternalCrawler,
        'test_broken_links_external': BrokenLinksExternalCrawler,
        'test_max_external_links': MaxExternalLinksCrawler,
    }

    @classmethod
    def setUpClass(cls):
        internal_urls = set()
        external_urls = set()
        subdomains_urls = set()
        files_urls = set()
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
            'FEED_URI': 'results.json'
        })
        # a = self.id()
        # 'CrawlerTest.MyTestCase.test_broken_links_external'
        cls.broken_links_external_crawler = \
            process.create_crawler(BrokenLinksExternalCrawler)
        process.crawl(cls.broken_links_external_crawler)
        # process.crawl(BrokenLinksInternalCrawler)
        # process.crawl(BrokenLinksExternalCrawler)
        # process.crawl(MaxExternalLinksCrawler)
        process.start()
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        db = AsyncIOMotorClient('localhost', 27017)['crawler']
        cls.db = db
        loop.run_until_complete(insert(db['Unique links'], {
            'name': 'insert domain name',
            'internal_urls': list(internal_urls),
            'external_urls': list(external_urls),
            'subdomain_urls': list(subdomains_urls),
            'files_urls': list(files_urls)
        }))

    def test_broken_links_internal(self):
        test_page = None
        with open('output.json') as file:
            for line in file:
                page = json.loads(line)
                for key in page:
                    if "https://crawler-test.com/links/broken_links_internal" in key:
                        test_page = page[key]
        if not test_page:
            self.fail()
        self.assertEqual(test_page['links'], 1)


        # a = self.db["https://crawler-test.com/links/broken_links_internal"]['internal_urls']
        # self.assertEqual(self.broken_links_external_crawler.stats, 0)

    def test_broken_links_external(self):
        pass

    def test_max_external_links(self):
        pass


if __name__ == '__main__':
    unittest.main()
