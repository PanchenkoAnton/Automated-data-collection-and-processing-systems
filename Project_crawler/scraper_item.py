import scrapy


class ScraperItem(scrapy.Item):

    url = scrapy.Field()
    data = scrapy.Field()
    external_links = scrapy.Field()
    internal_links = scrapy.Field()
    subdomains_links = scrapy.Field()
    files_links = scrapy.Field()

