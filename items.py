# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyhelloworldItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    test1 = scrapy.Field()
    test2 = scrapy.Field()
    test3 = scrapy.Field()
    pass

class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    score = scrapy.Field()
    director = scrapy.Field()
    area = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    summary = scrapy.Field()
    imdb = scrapy.Field()
    item_class = scrapy.Field()

    pass

class AnimaationItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    score = scrapy.Field()
    area = scrapy.Field()
    date = scrapy.Field()
    time = scrapy.Field()
    summary = scrapy.Field()
    douban_id = scrapy.Field()
    item_class = scrapy.Field()
    pass

class QixingcaiItem(scrapy.Item):
    # define the fields for your item here like:
    date = scrapy.Field()
    no = scrapy.Field()
    number = scrapy.Field()
    sellnum = scrapy.Field()
    pass