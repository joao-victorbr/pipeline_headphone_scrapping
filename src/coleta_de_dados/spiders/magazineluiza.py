import scrapy


class MagazineluizaSpider(scrapy.Spider):
    name = "magazineluiza"
    allowed_domains = ["www.magazineluiza.com.br"]
    start_urls = ["https://www.magazineluiza.com.br/busca/headphone/?from=submit"]
    page_count = 1
    max_page = 5

    def parse(self, response):
        products_list = response.css('a.sc-eBMEME.uPWog.sc-gZfzYS.lndZOc.sc-gZfzYS.lndZOc')
        for product in products_list:
            try:
                reviews_score = product.css("span.sc-epqpcT.jdMYPv::text").get().replace("(","").replace(")","").split(' ')[0]
            except:
                reviews_score = None
            try:
                reviews_quantity = product.css("span.sc-epqpcT.jdMYPv::text").get().replace("(","").replace(")","").split(' ')[1]
            except:
                reviews_score = None
            try:
                old_price = product.css("p.sc-kpDqfm.efxPhd.sc-gEkIjz.jmNQlo::text").get().replace('R$\xa0','')
            except:
                old_price = None

            yield {
                'product_brand':product.css("a::attr(data-brand)").get(),
                'product_name':product.css("h2.sc-dcjTxL.jXuKxj::text").get(),
                'reviews_score':reviews_score,
                'reviews_quantity':reviews_quantity if reviews_score else None,
                'old_price':old_price,
                'new_price':product.css("p.sc-kpDqfm.eCPtRw.sc-bOhtcR.dOwMgM::text").get().replace('R$\xa0','')
            }

        if self.page_count < self.max_page:

            self.page_count += 1
            page_number = str(self.page_count)
            next_page_url = 'https://www.magazineluiza.com.br/'+response.css('ul.sc-satoz.kbPvPg a::attr(href)').get()+'&page='+page_number
            print(f'\nScrapping da página {self.page_count-1} concluído.\nIniciando scrapping da página {self.page_count}. Link:',next_page_url)
            print('')
            if next_page_url:
                yield scrapy.Request(url=next_page_url, callback=self.parse)
