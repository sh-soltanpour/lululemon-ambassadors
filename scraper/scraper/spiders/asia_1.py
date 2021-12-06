import scrapy


class Asia1Spider(scrapy.Spider):
    name = "asia_1_ambassadors"

    def start_requests(self):
        urls = [
            "https://www.lululemon.com.hk/en-hk/content/asia-ambassador-index1.html"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        communities = response.css('.community-component')
        for community in communities:
            cards = community.css(".card .body-wrapper .desc")
            title = community.css('.title::text').get()
            if title:
                for card in cards:
                    name = card.css('p:nth-child(1)::text').get()
                    insta = card.css('p a::attr(href)').get().split('/')[-2]
                    city = title
                    yield {
                        'city': city,
                        'name': name,
                        'instagram': insta
                    }
