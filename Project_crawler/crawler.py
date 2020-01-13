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
from Project_parser.parsers.HTMLParser import HTMLParser


class Purumpurum(CrawlSpider):

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(Purumpurum, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    handle_httpstatus_all = True

    name = "purumpurum"

    # allowed_domains = ["msu.ru", "www.msu.ru"]
    # custom = ["https://www.msu.ru/"]
    allowed_domains = ["spbu.ru"]
    custom = ["https://spbu.ru/sitemap.xml"]

    global_stats = GlobalCrawlerStats(name=allowed_domains[0])

    collection = global_stats.db[global_stats.name]

    def start_requests(self):
        for url in self.custom:
            yield scrapy.Request(url, callback=self.parse_custom)

    def response(self, response):
        try:
            response = response.body.decode('utf-8')
        except Exception:
            response = response.body.decode('latin-1')
        return response

    def parse_custom(self, response):
        self.global_stats.internal_urls.add(response.url)
        self.statistics(response.url, response.status)
        item = ScraperItem()
        item['url'] = response.url
        if response.status != 200:
            return
        try:
            item['data'] = HTMLParser(text=self.response(response)).get_text()
            item['external_links'] = []
            item['internal_links'] = []
            item['subdomains_links'] = []
            item['files_links'] = []
            links = LinkExtractor(unique=True).extract_links(response)
            self.global_stats.total_links += len(links)
            for link in links:
                for allowed_domain in self.allowed_domains:

                    if self.global_stats.compare_domains(allowed_domain, link.url):
                        if '/tel:' in link.url:
                            self.global_stats.total_links -= 1
                            continue
                        if tldextract.extract(link.url).subdomain and tldextract.extract(
                                link.url).subdomain != 'www':
                            item['subdomains_links'].append(link.url)
                            self.global_stats.subdomains_urls.add(link.url)
                            continue

                        item['internal_links'].append(link.url)

                        # if link.url not in self.global_stats.internal_urls:
                        yield scrapy.Request(link.url,
                                             callback=self.parse_custom)
                        # self.global_stats.internal_urls.add(link.url)
                    else:
                        item['external_links'].append(link.url)
                        self.global_stats.external_urls.add(link.url)
        except Exception:
            item['data'] = ''
            self.global_stats.files_urls.add(response.url)
            return

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
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/79.0.3945.117 Safari/537.36',
        'HTTPERROR_ALLOW_ALL': True,
        'DOWNLOAD_DELAY': 0.1,
        'LOG_LEVEL': 'INFO',
        'REDIRECT_ENABLED': True
    })
    process.crawl(Purumpurum)
    process.start()
