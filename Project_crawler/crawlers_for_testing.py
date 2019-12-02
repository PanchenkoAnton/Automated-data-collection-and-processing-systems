from Project_crawler.crawler import Purumpurum


class BrokenLinksInternalCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/broken_links_internal"]


class BrokenLinksExternalCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/broken_links_external"]
