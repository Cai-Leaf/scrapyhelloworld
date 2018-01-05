import scrapy
from datetime import datetime
from scrapyhelloworld.items import MovieItem

class DmozSpider(scrapy.spiders.Spider):
    name = "douban_movie"
    start_urls = [
        "https://movie.douban.com/tag/%E5%89%A7%E6%83%85"
    ]

    def parse(self, response):
        url_list = response.xpath('//div[@class="pl2"]/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url, callback=self.getMovieinfo)
        next_url = response.xpath('//link[@rel="next"]/@href').extract()[0]
        yield scrapy.Request(next_url, callback=self.parse)

    def getMovieinfo(self, response):
            item = MovieItem()
            item["name"] = self.check_attr_blank(response.xpath('//span[@property="v:itemreviewed"]/text()').extract())
            item["score"] = self.check_attr_blank(response.xpath('//strong[@property="v:average"]/text()').extract())
            item["director"] = self.check_attr_blank(response.xpath('//a[@rel="v:directedBy"]/text()').extract())
            item["area"] = self.check_attr_blank(response.xpath('//span[@class="pl" and text()="制片国家/地区:"]/following::text()[1]').extract())
            item["date"] = self.check_attr_blank(response.xpath('//span[@property="v:initialReleaseDate"]/text()').extract())
            item["time"] = self.check_attr_blank(response.xpath('//span[@property="v:runtime"]/@content|//span[@class="pl" and text()="单集片长:"]/following::text()[1]').extract())
            item["summary"] = self.check_attr_blank(response.xpath('//span[@property="v:summary"]/text()').extract())
            item["imdb"] = self.check_key_blank(response.xpath('//span[@class="pl" and text()="IMDb链接:"]/following::a[1]/text()').extract())
            yield item

    def check_attr_blank(self, attr):
        if len(attr) > 0:
            attr = attr[0].strip()
        else:
            attr = ""
        return attr

    def check_key_blank(self, key):
        if len(key) > 0:
            key = key[0]
        else:
            key = 'imdb'+datetime.now().strftime('%Y%m%d%H%M%S%f')
        return key


