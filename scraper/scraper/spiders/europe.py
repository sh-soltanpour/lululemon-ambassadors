import scrapy


class EuropeSpider(scrapy.Spider):
    name = "europe_ambassadors"

    def start_requests(self):
        urls = [
            "https://www.eu.lululemon.com/en-lu/c/community/ambassadors/store"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        cards = response.css('.card .body-wrapper .desc')
        for card in cards:
            city = card.css('p:nth-child(1)::text').get()
            name = card.css('p:nth-child(2)::text').get()
            role = card.css('p:nth-child(3)::text').get()
            insta = card.css('p:nth-child(4) a::attr(href)').get().split('/')[-1]
            yield {
                'city': city,
                'name': name,
                'role': role,
                'instagram': insta
            }
