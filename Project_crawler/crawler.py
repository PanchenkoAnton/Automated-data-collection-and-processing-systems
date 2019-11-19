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

    stats = {"count": 0, "statuses": {}}

    name = "purumpurum"

    allowed_domains = ["crawler-test.com"]

    start_urls = ["https://crawler-test.com/links/max_external_links"]

    rules = (Rule(LinkExtractor(allow=()), callback='start_requests', follow=True),)

    custom_settings = {'FEED_URI': "test.json",
                       'FEED_FORMAT': 'json'}

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        self.statistics(response)
        item = ScraperItem()
        item['url'] = response.url
        item['external_links'] = []
        item['internal_links'] = []
        item['subdomains_links'] = []
        for link in LinkExtractor().extract_links(response):
            for allowed_domain in self.allowed_domains:

                if compare_domains(allowed_domain, link.url):

                    if tldextract.extract(link.url).subdomain:
                        item['subdomains_links'].append(link.url)
                        continue

                    item['internal_links'].append(link.url)

                    if link.url not in self.internal_urls:
                        self.internal_urls.add(link.url)
                        yield scrapy.Request(link.url, callback=self.parse, dont_filter=True)
                else:
                    item['external_links'].append(link.url)
        return item

    def statistics(self, response):
        if response.status in self.stats['statuses']:
            self.stats['statuses'][response.status] += 1
        else:
            self.stats['statuses'][response.status] = 1
        self.stats['count'] += 1
        print(self.stats)


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,'
                      ' like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'HTTPCACHE_ENABLED': True,
        'AUTOTHROTTLE_ENABLED': True,
        'DOWNLOAD_DELAY': 1

    })
    process.crawl(Purumpurum)
    process.start()
