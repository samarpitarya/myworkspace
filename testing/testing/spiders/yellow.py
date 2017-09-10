import scrapy
import json
import re
from testing.items import TestingItem
class Listing(scrapy.Spider):
    name = 'yellow'
    start_urls = ['https://www.yellowpages.com/santa-barbara-ca/attorneys',
    'https://www.yellowpages.com/santa-barbara-ca/home-services',
    'https://www.yellowpages.com/santa-barbara-ca/medical-dental',
    'https://www.yellowpages.com/santa-barbara-ca/restaurants',
    'https://www.yellowpages.com/santa-barbara-ca/automotive',
    'https://www.yellowpages.com/santa-barbara-ca/insurance',
    'https://www.yellowpages.com/santa-barbara-ca/beautly-spa',
    'https://www.yellowpages.com/santa-barbara-ca/pets']

    def parse(self, response):
        listingCount = response.xpath('//div[@class="pagination"]/p/text()').extract_first()
        listingCount =  re.findall(r'\d+',listingCount)
        try:
            listingCount = listingCount[-1]
            listingCount = int(listingCount)/30
            pages = listingCount
            for i in range(1, pages+1):
                pageForCrawl = response.url+"?page="+str(i)
                yield scrapy.Request(url=pageForCrawl, callback=self.parseSingleListingPage)
        except:
            print "there is something wrong in pagination"
    #
    def parseSingleListingPage(self, response):
        print response.url
        links = response.xpath('//div[@class="links"]/a[contains(text(),"More Info")]/@href').extract()
        for link in links:
            yield scrapy.Request(url="https://www.yellowpages.com"+link, callback= self.detailsParser)
    def detailsParser(self, response):
        item = TestingItem()

        mail_id = response.xpath('//a[@class="email-business"]/@href').extract_first()
        if mail_id:
            mail_id = mail_id.replace('mailto:','')
        title = response.xpath('//h1[@itemprop="name"]/text()').extract_first()
        item ={}
        item['mail_id'] = mail_id
        item['title'] = title
