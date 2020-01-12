# -*- coding: utf-8 -*-
import asyncio
import json

import scrapy
import tldextract
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider, Spider

from Project_crawler.GlobalCrawlerStats import GlobalCrawlerStats
from Project_crawler.scraper_item import ScraperItem


class Purumpurum(CrawlSpider):

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(Purumpurum, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    handle_httpstatus_all = True

    name = "purumpurum"

    # allowed_domains = ["msu"]
    # start_urls = ["https://www.msu.ru/"]
    allowed_domains = ["spbu"]
    start_urls = ["https://spbu.ru/"]

    global_stats = GlobalCrawlerStats(name=allowed_domains[0])

    rules = (Rule(LinkExtractor(allow=()), callback='start_requests', follow=True),)

    collection = global_stats.db[global_stats.name]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def response(self, response):
        try:
            response = response.body.decode('utf-8')
        except Exception:
            response = response.body.decode('latin-1')
        return response

    def parse(self, response):
        if response.url in self.global_stats.internal_urls \
                or response.url in self.global_stats.external_urls \
                or response.url in self.global_stats.files_urls:
            return
        self.statistics(response.url, response.status)
        item = ScraperItem()
        item['url'] = response.url
        if response.status != 200:
            item['data'] = self.response(response)
            return
        item['data'] = self.response(response)
        item['external_links'] = []
        item['internal_links'] = []
        item['subdomains_links'] = []
        item['files_links'] = []
        try:
            links = LinkExtractor().extract_links(response)
            self.global_stats.total_links += len(links)
            for link in links:
                for allowed_domain in self.allowed_domains:

                    if self.global_stats.compare_domains(allowed_domain, link.url):

                        if tldextract.extract(link.url).subdomain and tldextract.extract(
                                link.url).subdomain != 'www':
                            item['subdomains_links'].append(link.url)
                            self.global_stats.subdomains_urls.add(link.url)
                            continue

                        item['internal_links'].append(link.url)

                        if link.url not in self.global_stats.internal_urls:
                            self.global_stats.internal_urls.add(link.url)
                            yield scrapy.Request(link.url, callback=self.parse, dont_filter=True)

                    else:
                        item['external_links'].append(link.url)
                        self.global_stats.external_urls.add(link.url)
        except Exception:
            item['files_links'].append(response.url)
            self.global_stats.files_urls.add(response.url)

        asyncio.set_event_loop(asyncio.new_event_loop())
        self.global_stats.loop.run_until_complete(self.global_stats.insert(self.collection, item))
        yield item

    def statistics(self, url, status):
        status = str(status)
        self.global_stats.stats['count'] += 1
        if status == '200':
            self.global_stats.stats['statuses'][status][0] += 1
            return
        self.global_stats.broken_links += 1
        if status in self.global_stats.stats['statuses']:
            self.global_stats.stats['statuses'][status][0] += 1
            self.global_stats.stats['statuses'][status][1].add(url)
        else:
            self.global_stats.stats['statuses'][status] = [1, set([url])]

        print(self.global_stats.stats)

    def spider_closed(self, spider):
        spider.logger.info("Writing to database ...")
        self.global_stats.write_to_db()


if __name__ == "__main__":
    # process = CrawlerProcess({
    #     'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,'
    #                   ' like Gecko) Chrome/74.0.3729.157 Safari/537.36',
    #     'HTTPCACHE_ENABLED': True,
    #     'AUTOTHROTTLE_ENABLED': True,
    #     #'HTTPERROR_ALLOWED_CODES': [404, 403, 504, 503, 301],
    #     'HTTPERROR_ALLOW_ALL': True,
    #     'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
    #     'DOWNLOAD_DELAY': 3,
    #     'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    #     'CONCURRENT_REQUESTS': 1,
    #     'LOG_LEVEL': 'INFO',
    #     'REDIRECT_ENABLED': False,
    #     #'FEED_URI': "output.json",
    #     #'FEED_FORMAT': 'json'
    #
    # })
    process = CrawlerProcess({
        'HTTPERROR_ALLOW_ALL': True,
        'DOWNLOAD_DELAY': 0.25,
        'REDIRECT_ENABLED': False,
        'LOG_LEVEL': 'INFO',
        # 'FEED_URI': "output.json",
        # 'FEED_FORMAT': 'json'

    })
    process.crawl(Purumpurum)
    process.start()
