import json
import os
import unittest

from scrapy.crawler import CrawlerProcess

from Project_crawler.crawlers_for_testing import BrokenLinksInternalCrawler, \
    BrokenLinksExternalCrawler, MaxExternalLinksCrawler, SubdomainCrawler, \
    RepeatedExternalLinksCrawler, RepeatedInternalLinksCrawler, \
    ExternalLinksToDisallowedCrawler, NonStandardLinksCrawler, \
    WhitespaceInLinksCrawler, InfiniteRedirectCrawler


class CrawlerLinksTestCase(unittest.TestCase):

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
        process.crawl(RepeatedExternalLinksCrawler)
        process.crawl(RepeatedInternalLinksCrawler)
        process.crawl(ExternalLinksToDisallowedCrawler)
        process.crawl(NonStandardLinksCrawler)
        process.crawl(WhitespaceInLinksCrawler)
        process.crawl(InfiniteRedirectCrawler)
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
                    self.assertEqual(len(line['external_links']), 13)
                    self.assertEqual(len(line['internal_links']), 1)
                    self.assertEqual(len(line['subdomains_links']), 0)
                    self.assertEqual(len(line['files_links']), 0)

    def test_subdomain_links(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == SubdomainCrawler.start_urls[0]:
                    self.assertEqual(len(line['external_links']), 0)
                    self.assertEqual(len(line['internal_links']), 0)
                    self.assertEqual(len(line['subdomains_links']), 1)
                    self.assertEqual(len(line['files_links']), 0)

    def test_repeated_external_links(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == RepeatedExternalLinksCrawler.start_urls[0]:
                    self.assertEqual(len(line['external_links']), 3)
                    self.assertEqual(len(line['internal_links']), 1)
                    self.assertEqual(len(line['subdomains_links']), 0)
                    self.assertEqual(len(line['files_links']), 0)

    def test_repeated_internal_links(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == RepeatedInternalLinksCrawler.start_urls[0]:
                    self.assertEqual(len(line['external_links']), 0)
                    self.assertEqual(len(line['internal_links']), 1)
                    self.assertEqual(len(line['subdomains_links']), 0)
                    self.assertEqual(len(line['files_links']), 0)

    def test_external_links_to_disallowed(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == ExternalLinksToDisallowedCrawler.start_urls[0]:
                    self.assertEqual(len(line['external_links']), 4)
                    self.assertEqual(len(line['internal_links']), 1)
                    self.assertEqual(len(line['subdomains_links']), 0)
                    self.assertEqual(len(line['files_links']), 0)

    def test_non_standard_links(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == NonStandardLinksCrawler.start_urls[0]:
                    self.assertEqual(len(line['external_links']), 2)
                    self.assertEqual(len(line['internal_links']), 1)
                    self.assertEqual(len(line['subdomains_links']), 0)
                    self.assertEqual(len(line['files_links']), 0)

    def test_whitespace_in_links(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == WhitespaceInLinksCrawler.start_urls[0]:
                    self.assertEqual(len(line['external_links']), 3)
                    self.assertEqual(len(line['internal_links']), 1)
                    self.assertEqual(len(line['subdomains_links']), 0)
                    self.assertEqual(len(line['files_links']), 0)

    def test_infinite_redirect(self):
        with open('output.json') as file:
            for line in file:
                line = json.loads(line)
                if line['url'] == InfiniteRedirectCrawler.start_urls[0]:
                    self.assertEqual(len(line['external_links']), 0)
                    self.assertEqual(len(line['internal_links']), 0)
                    self.assertEqual(len(line['subdomains_links']), 0)
                    self.assertEqual(len(line['files_links']), 0)


if __name__ == '__main__':
    unittest.main()
