# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from Project_crawler.scraper_item import ScraperItem


class Purumpurum(CrawlSpider):

    name = "purumpurum"

    allowed_domains = ["crawler-test.com/links", " http://robotto.org"]

    start_urls = ["https://crawler-test.com/links/max_external_links"]

    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse_items(self, response):

        items = []
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)

        for link in links:
            # print('link ', link)
            is_allowed = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = True
            if is_allowed:
                item = ScraperItem()
                item['url_from'] = response.url
                # print('response url', response.url)
                item['url_to'] = link.url
                # print('link url', link.url)
                items.append(item)
        # print(items)
        return items


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
