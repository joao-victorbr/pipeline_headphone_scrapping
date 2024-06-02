import scrapy


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["www.amazon.com.br"]
    start_urls = ["https://www.amazon.com.br/s?k=headphone"]

    def parse(self, response):
        pass
