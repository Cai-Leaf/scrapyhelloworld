import scrapy
from scrapyhelloworld.items import QixingcaiItem

class QixingcaiSpider(scrapy.spiders.Spider):
    name = "qixingcai"
    start_urls = [
        "http://www.lecai.com/lottery/draw/list/2?d=2017-01-01",
        "http://www.lecai.com/lottery/draw/list/2?d=2016-01-01",
        "http://www.lecai.com/lottery/draw/list/2?d=2015-01-01",
        "http://www.lecai.com/lottery/draw/list/2?d=2014-01-01",
        "http://www.lecai.com/lottery/draw/list/2?d=2013-01-01",
        "http://www.lecai.com/lottery/draw/list/2?d=2012-01-01",
        "http://www.lecai.com/lottery/draw/list/2?d=2011-01-01",
        "http://www.lecai.com/lottery/draw/list/2?d=2010-01-01",
        "http://www.lecai.com/lottery/draw/list/2?d=2009-01-01",
        "http://www.lecai.com/lottery/draw/list/2?d=2008-01-01",
        "http://www.lecai.com/lottery/draw/list/2?d=2007-01-01",
        "http://www.lecai.com/lottery/draw/list/2?d=2006-01-01",
        "http://www.lecai.com/lottery/draw/list/2?d=2005-01-01",
        "http://www.lecai.com/lottery/draw/list/2?d=2004-01-01"
    ]

    def parse(self, response):
        links = response.xpath('//tr[@class="bgcolor1"]|//tr[@class="bgcolor2"]')
        for index, link in enumerate(links):
            item = QixingcaiItem()
            item["date"] = link.xpath('.//td[@class="td1"]/text()').extract()[0]
            item["no"] = link.xpath('.//a/text()').extract()[0]
            numbers = '="'
            for num in link.xpath('.//span[@class="ball_1"]/text()').extract():
                numbers += num
            item["number"] = numbers+'"'
            item["sellnum"] = link.xpath('.//td[@class="td4"]/text()').extract()[0]
            yield item

