import scrapy


class ScraperItem(scrapy.Item):
    url_from = scrapy.Field()
    url_to = scrapy.Field()
