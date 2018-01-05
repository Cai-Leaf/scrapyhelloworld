import scrapy
import json
from datetime import datetime
from scrapyhelloworld.items import MovieItem
from scrapyhelloworld.items import AnimaationItem

class MovieUpdateSpider(scrapy.spiders.Spider):
    name = "douban_movie_update"
    start_urls = [
        "https://movie.douban.com/cinema/nowplaying/"
    ]

    def parse(self, response):
        # 爬取院线电影
        url_list = response.xpath('//a[@data-psource="poster"]/@href').extract()
        for url in url_list:
            yield scrapy.Request(url, callback=self.getMovieinfo)
        # 爬取最新的40个电影
        uew_movie_url1 = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%9C%80%E6%96%B0&page_limit=20&page_start=0"
        uew_movie_url2 = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%9C%80%E6%96%B0&page_limit=20&page_start=20"
        yield scrapy.Request(uew_movie_url1, callback=self.getNewMovieUrl)
        yield scrapy.Request(uew_movie_url2, callback=self.getNewMovieUrl)
        # 爬取最新的40个动画片
        animation_url1 = "https://movie.douban.com/tag/%E6%97%A5%E6%9C%AC%E5%8A%A8%E7%94%BB?start=0&type=R"
        animation_url2 = "https://movie.douban.com/tag/%E6%97%A5%E6%9C%AC%E5%8A%A8%E7%94%BB?start=20&type=R"
        yield scrapy.Request(animation_url1, callback=self.parseAnimation)
        yield scrapy.Request(animation_url2, callback=self.parseAnimation)

    def parseAnimation(self, response):
        url_list = response.xpath('//div[@class="pl2"]/a/@href').extract()
        for url in url_list:
            yield scrapy.Request(url, callback=self.getAnimationinfo)

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
            item["item_class"] = 'movie'
            yield item

    def getAnimationinfo(self, response):
            item = AnimaationItem()
            item["name"] = self.check_attr_blank(response.xpath('//span[@property="v:itemreviewed"]/text()').extract())
            item["score"] = self.check_attr_blank(response.xpath('//strong[@property="v:average"]/text()').extract())
            item["area"] = self.check_attr_blank(response.xpath('//span[@class="pl" and text()="制片国家/地区:"]/following::text()[1]').extract())
            item["date"] = self.check_attr_blank(response.xpath('//span[@property="v:initialReleaseDate"]/text()').extract())
            item["time"] = self.check_attr_blank(response.xpath('//span[@property="v:runtime"]/@content|//span[@class="pl" and text()="单集片长:"]/following::text()[1]').extract())
            item["summary"] = self.check_attr_blank(response.xpath('//span[@property="v:summary"]/text()').extract())
            item["douban_id"] = self.check_attr_blank(response.xpath('//a[@class="j a_show_login lnk-sharing"]/@data-object_id').extract())
            item["item_class"] = 'animation'
            yield item

    def getNewMovieUrl(self, response):
        moviejson = json.loads(response.body_as_unicode())
        for movie in moviejson['subjects']:
            yield scrapy.Request(movie['url'], callback=self.getMovieinfo)

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



