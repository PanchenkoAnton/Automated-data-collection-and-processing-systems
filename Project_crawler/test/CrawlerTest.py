import json
import os
import unittest

from scrapy.crawler import CrawlerProcess

from Project_crawler.crawlers_for_testing import BrokenLinksInternalCrawler, \
    BrokenLinksExternalCrawler, MaxExternalLinksCrawler, SubdomainCrawler


class MyTestCase(unittest.TestCase):

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
        process.crawl(BrokenLinksExternalCrawler)
        process.crawl(MaxExternalLinksCrawler)
        process.crawl(SubdomainCrawler)
        process.start()

    def test_broken_links_internal(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == BrokenLinksInternalCrawler.start_urls[0]:
                    self.assertEqual(len(line['internal_links']), 6)

    def test_broken_links_external(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == BrokenLinksExternalCrawler.start_urls[0]:
                    self.assertEqual(len(line['internal_links']), 1)
                    self.assertEqual(len(line['external_links']), 5)

    def test_max_external_links(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == MaxExternalLinksCrawler.start_urls[0]:
                    self.assertEqual(len(line['internal_links']), 1)
                    self.assertEqual(len(line['external_links']), 13)

    def test_subdomain_links(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == SubdomainCrawler.start_urls[0]:
                    self.assertEqual(len(line['subdomain_links']), 1)

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
