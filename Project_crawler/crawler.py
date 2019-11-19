# -*- coding: utf-8 -*-

import scrapy
import tldextract
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from Project_crawler.scraper_item import ScraperItem


def get_domain(link):
    return tldextract.extract(link).domain


def compare_domains(link1, link2):
    return get_domain(link1) == get_domain(link2)


class Purumpurum(CrawlSpider):
    internal_urls = set()

    external_urls = set()

    subdomains_urls = set()

    files_urls = set()

    stats = {"count": 0, "statuses": {200: [0]}}

    name = "purumpurum"

    allowed_domains = ["http://titan.dcs.bbk.ac.uk/"]

    start_urls = ["http://titan.dcs.bbk.ac.uk/~kikpef01/testpage.html"]

    rules = (Rule(LinkExtractor(allow=()), callback='start_requests', follow=True),)

    custom_settings = {'FEED_URI': "test.json",
                       'FEED_FORMAT': 'json'}

    def parse(self, response):
        self.statistics(response.url, response.status)
        if response.status != 200: return
        item = ScraperItem()
        item['url'] = response.url
        item['external_links'] = []
        item['internal_links'] = []
        item['subdomains_links'] = []
        try:
            for link in LinkExtractor().extract_links(response):
                for allowed_domain in self.allowed_domains:

                    if compare_domains(allowed_domain, link.url):

                        if tldextract.extract(link.url).subdomain:
                            item['subdomains_links'].append(link.url)
                            self.subdomains_urls.add(link.url)
                            continue

                        item['internal_links'].append(link.url)

                        if link.url not in self.internal_urls:
                            self.internal_urls.add(link.url)
                            yield scrapy.Request(link.url, callback=self.parse, dont_filter=True)

                    else:
                        item['external_links'].append(link.url)
                        self.external_urls.add(link.url)
        except Exception as e:
            self.files_urls.add(response.url)
        return item

    def statistics(self, url, status):
        self.stats['count'] += 1
        if status == 200:
            self.stats['statuses'][status][0] += 1
            return
        if status in self.stats['statuses']:
            self.stats['statuses'][status][0] += 1
            self.stats['statuses'][status][1].add(url)
        else:
            self.stats['statuses'][status] = [1, set([url])]

        print(self.stats)


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,'
                      ' like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'HTTPCACHE_ENABLED': True,
        'AUTOTHROTTLE_ENABLED': True,
        'HTTPERROR_ALLOWED_CODES': [404, 403, 504, 503, 301],
        'HTTPERROR_ALLOW_ALL': True,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 2.0,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 33,
        'CONCURRENT_REQUESTS': 33,
        'LOG_LEVEL': 'DEBUG'

    })
    process.crawl(Purumpurum)
    process.start()
