from Project_crawler.crawler import Purumpurum


class BrokenLinksInternalCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/broken_links_internal"]


class BrokenLinksExternalCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/broken_links_external"]


class MaxExternalLinksCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/max_external_links"]


class RepeatedExternalLinksCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/page_with_external_links"]


class RepeatedInternalLinksCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/repeated_internal_links"]


class ExternalLinksToDisallowedCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = \
        ["https://crawler-test.com/links/external_links_to_disallwed_urls"]


class NonStandardLinksCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/non_standard_links"]
