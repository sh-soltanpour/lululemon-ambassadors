import scrapy
from scrapy import Selector
from scrapy.http import Response

from typing import Iterable

class AustraliaSpider(scrapy.Spider):
    name = "australia_ambassadors"
    already_found = []

    def start_requests(self):
        urls = [
            "https://www.lululemon.com.au/en-au/c/community/ambassadors/victoria",
            "https://www.lululemon.com.au/en-au/c/community/ambassadors/new-south-wales",
            "https://www.lululemon.com.au/en-au/c/community/ambassadors/queensland",
            "https://www.lululemon.com.au/en-au/c/community/ambassadors/australian-capital-territory",
            "https://www.lululemon.com.au/en-au/c/community/ambassadors/western-australia",
            "https://www.lululemon.com.au/en-au/c/community/ambassadors/tasmania",
            "https://www.lululemon.com.au/en-au/c/community/ambassadors/new-zealand"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: Response):
        links: Iterable[Selector] = response.css('a::attr(href)')
        for link in links:
            l = link.get()
            if 'instagram.com' in l:
                l = l[:l.find('/?')]
                instagram = l.split('/')[-1]
                name = instagram
                city = response.url.split('/')[-1]
                if instagram not in self.already_found and 'lululemon' not in instagram:
                    self.already_found.append(instagram)
                    yield {
                        'city': city,
                        'name': name,
                        'instagram': instagram
                    }
        yield
