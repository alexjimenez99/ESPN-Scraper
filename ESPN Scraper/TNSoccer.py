import scrapy


class TnsoccerSpider(scrapy.Spider):
    name = 'TNSoccer'
    allowed_domains = ['www.tnsoccer.org']
    start_urls = ['http://www.tnsoccer.org/']

    def parse(self, response):
        pass
