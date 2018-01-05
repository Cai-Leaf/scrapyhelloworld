import scrapy
import json
from scrapyhelloworld.items import ScrapyhelloworldItem
from scrapy.contrib.linkextractors import LinkExtractor

class CheckXpathSpider(scrapy.spiders.Spider):
    name = "check_xpath"
    # allowed_domains = ["dmoz.org"]
    start_urls = [
        "https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%9C%80%E6%96%B0&page_limit=20&page_start=0"
    ]

    def parse(self, response):
        test = json.loads(response.body_as_unicode())
        for aaa in test['subjects']:
            print(aaa['url'])


