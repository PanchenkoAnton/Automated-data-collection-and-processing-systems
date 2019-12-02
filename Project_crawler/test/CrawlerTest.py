import asyncio
import unittest

from motor.motor_asyncio import AsyncIOMotorClient
from scrapy.crawler import CrawlerProcess

from Project_crawler.crawler import insert
from Project_crawler.crawlers_for_testing import BrokenLinksInternalCrawler, \
    BrokenLinksExternalCrawler


class MyTestCase(unittest.TestCase):
    def setUp(self):
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
            'LOG_LEVEL': 'INFO'

        })
        process.crawl(BrokenLinksInternalCrawler)
        process.crawl(BrokenLinksExternalCrawler)
        process.start()
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        db = AsyncIOMotorClient('localhost', 27017)['crawler']
        loop.run_until_complete(insert(db['Unique links'], {
            'name': 'insert domain name',
            'internal_urls': list(internal_urls),
            'external_urls': list(external_urls),
            'subdomain_urls': list(subdomains_urls),
            'files_urls': list(files_urls)
        }))

    def test_broken_links_internal(self):
        # self.assertEqual()
        pass

    def test_broken_links_external(self):
        pass

if __name__ == '__main__':
    unittest.main()
