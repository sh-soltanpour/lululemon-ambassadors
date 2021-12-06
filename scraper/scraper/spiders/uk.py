import scrapy


class UKSpider(scrapy.Spider):
    name = "uk_ambassadors"

    def start_requests(self):
        urls = [
            "https://www.lululemon.co.uk/en-gb/c/community/ambassadors/store"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        cards = response.css('.card .body-wrapper .desc')
        print(len(cards))
        for card in cards:
            city = card.css('p:nth-child(1)::text').get()
            name = card.css('p:nth-child(2)::text').get()
            role = card.css('p:nth-child(3)::text').get()
            try:
                insta = card.css('p:nth-child(4) a::attr(href)').get().split('/')[-1]
            except AttributeError:
                print("MISSING INSTA OF " + name)
                insta = None
            if insta:
                yield {
                    'city': city,
                    'name': name,
                    'role': role,
                    'instagram': insta
                }
            else:
                yield
