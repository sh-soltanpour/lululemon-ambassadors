import scrapy


class KoreaSpider(scrapy.Spider):
    name = "korea_ambassadors"

    def start_requests(self):
        urls = [
            "https://www.lululemon.co.kr/ko-kr/ambassadors.html"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        cards = response.css('.card .body-wrapper .desc')
        city = 'KOREA'
        for card in cards:
            name = card.css('p:nth-child(1)::text').get()
            insta = card.css('.desc a::attr(href)').get()
            if insta:
                insta = insta.split("/")[-1]
                yield {
                    'city': city,
                    'name': name,
                    'instagram': insta
                }
