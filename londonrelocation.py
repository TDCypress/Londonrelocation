import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from ..items import Property


class LondonrelocationSpider(scrapy.Spider):
    name = 'londonrelocation'
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']

    def parse(self, response):
        for start_url in self.start_urls:
            yield Request(url=start_url,
                          callback=self.parse_area)

    def parse_area(self, response):
        area_urls = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()
        for area_url in area_urls:
            yield Request(url=area_url,
                          callback=self.parse_area_pages)

    def parse_area_pages(self, response):
        # Write your code here and remove `pass` in the following line

        property = ItemLoader(item=Property())

        title = response.css('.h4-space a').css('::text').extract()
        price = response.css('h5').css('::text')[0].extract()
        price = str(''.join(x for x in price if x.isdigit()))
        url = response.css('.h4-space a').css('::attr(href)')[0].extract()
        url = 'https://londonrelocation.com'+url

        property.add_value('title', title)
        property.add_value('price', price) # 420 per week
        property.add_value('url', url)

        return property.load_item()

        # an example for adding a property to the json list:
        # property = ItemLoader(item=Property())
        # property.add_value('title', '2 bedroom flat for rental')
        # property.add_value('price', '1680') # 420 per week
        # property.add_value('url', 'https://londonrelocation.com/properties-to-rent/properties/property-london/534465-2-bed-frognal-hampstead-nw3/')
        # return property.load_item()
