# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

class NewsItem(scrapy.Item):
    category = scrapy.Field()
    subcategory = scrapy.Field()
    meta = scrapy.Field()
    title = scrapy.Field()
    short_description = scrapy.Field()


class NewsItemLoader(scrapy.loader.ItemLoader):
    pass
