import scrapy


class MagazineluizaSpider(scrapy.Spider):
    name = "magazineluiza"
    allowed_domains = ["www.magazineluiza.com.br"]
    start_urls = ["https://www.magazineluiza.com.br/busca/headphone/?from=submit"]

    def parse(self, response):
        products_list = response.css('li.sc-kTbCBX.ciMFyT')
        for product in products_list:
            
            yield {
                'brand' : product.css("a::attr(data-brand)").get()
            }

