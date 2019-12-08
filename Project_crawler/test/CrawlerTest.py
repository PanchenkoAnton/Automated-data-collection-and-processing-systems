import asyncio
import json
import os
import unittest

from motor.motor_asyncio import AsyncIOMotorClient
from scrapy.crawler import CrawlerProcess

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
        if os.path.exists('output.json'):
            os.remove('output.json')
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
        process.crawl(BrokenLinksInternalCrawler)
        # process.crawl(BrokenLinksExternalCrawler)
        # process.crawl(MaxExternalLinksCrawler)
        process.start()

    def test_broken_links_internal(self):
        test_page = None
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == BrokenLinksInternalCrawler.start_urls[0]:
                    self.assertEqual(len(line['external_links']), 6)
                # page = json.loads(line)
                # page = line
                # for key in page:
                #     if "https://crawler-test.com/links/broken_links_internal" in key:
                #         test_page = page[key]
        # if not test_page:
        #     self.fail(msg='Failed')
        # links = test_page['links']
        # self.assertEqual(test_page['links'], 1)


        # a = self.db["https://crawler-test.com/links/broken_links_internal"]['internal_urls']
        # self.assertEqual(self.broken_links_external_crawler.stats, 0)

    def test_broken_links_external(self):
        pass

    def test_max_external_links(self):
        pass

    def test_repeated_external_links(self):
        pass

    def test_repeated_internal_links(self):
        pass

    def test_external_links_to_disallowed(self):
        pass

    def test_non_standard_links(self):
        pass

    def test_whitespace_in_links(self):
        pass

    def test_double_slash_disallowed_start(self):
        pass

    def test_double_slash_disallowed_middle(self):
        pass

    def test_double_slash_disallowed_end(self):
        pass

    def test_http_non_www(self):
        pass

    def test_http(self):
        pass

    def test_https(self):
        pass

    def test_non_head_tag_inside_head_tag(self):
        pass

    def test_infinite_redirect(self):
        pass

    def test_url_with_foreign_characters(self):
        pass

    def test_foreign_character_domain(self):
        pass


if __name__ == '__main__':
    unittest.main()
