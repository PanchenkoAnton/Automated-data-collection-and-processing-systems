# -*- coding: utf-8 -*-
import asyncio
import json

import scrapy
import tldextract
from motor.motor_asyncio import AsyncIOMotorClient
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from Project_crawler.scraper_item import ScraperItem

db = AsyncIOMotorClient('localhost', 27017)['crawler']


def get_domain(link):
    return tldextract.extract(link).domain


def compare_domains(link1, link2):
    return get_domain(link1) == get_domain(link2)


async def insert(collection, document):
    await collection.insert_one(dict(document))


internal_urls = set()

external_urls = set()

subdomains_urls = set()

files_urls = set()

loop = asyncio.get_event_loop()


class Purumpurum(CrawlSpider):
    stats = {"count": 0, "statuses": {200: [0]}}

    name = "purumpurum"

    allowed_domains = ["msu.ru"]

    start_urls = ["https://msu.ru/"]

    rules = (Rule(LinkExtractor(allow=()), callback='start_requests', follow=True),)

    collection = get_domain(start_urls[0])
    collection = db[collection]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        self.statistics(response.url, response.status)
        item = ScraperItem()
        item['url'] = response.url
        if response.status != 200:
            item['data'] = json.dumps(str(response.body))
            return
        item['data'] = json.dumps(str(response.body))
        item['external_links'] = []
        item['internal_links'] = []
        item['subdomains_links'] = []
        item['files_links'] = []
        try:
            for link in LinkExtractor().extract_links(response):
                for allowed_domain in self.allowed_domains:

                    if compare_domains(allowed_domain, link.url):

                        if tldextract.extract(link.url).subdomain and tldextract.extract(link.url).subdomain != 'www':
                            item['subdomains_links'].append(link.url)
                            subdomains_urls.add(link.url)
                            continue

                        item['internal_links'].append(link.url)

                        if link.url not in internal_urls:
                            internal_urls.add(link.url)
                            yield scrapy.Request(link.url, callback=self.parse, dont_filter=True)

                    else:
                        item['external_links'].append(link.url)
                        external_urls.add(link.url)
        except Exception:
            item['files_links'].append(response.url)
            files_urls.add(response.url)

        asyncio.set_event_loop(asyncio.new_event_loop())
        loop.run_until_complete(insert(self.collection, item))
        yield item

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
        'LOG_LEVEL': 'INFO'

    })
    process.crawl(Purumpurum)
    process.start()
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop.run_until_complete(insert(db['Unique links'], {"name": "insert domain name",
                                                        "internal_urls": list(internal_urls),
                                                        "external_urls": list(external_urls),
                                                        "subdomains_urls": list(subdomains_urls),
                                                        "files_urls": list(files_urls)}))
    loop.close()
