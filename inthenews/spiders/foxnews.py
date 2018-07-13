# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from inthenews.items import NewsItem

class FoxnewsSpider(scrapy.Spider):
    name = 'foxnews'
    allowed_domains = ['foxnews.com']
    start_urls = ['http://www.foxnews.com/category/us/crime.html']

    category_xpath = '//div[@class="meta"]/span/a/text()'
    title_xpath = '//h2[@class="title"]/a/text()'
    abstract_xpath = '//div[@class="content"]/p/a/text()'

    # TODO click 'Show more' and capture more articles
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={})

    def parse(self, response):
        articles = response.xpath('//article')
        for article in articles:
            yield {
                'category' : article.xpath(self.category_xpath).extract_first(),
                'title' : article.xpath(self.title_xpath).extract_first(),
                'short_description' : article.xpath(self.abstract_xpath).extract_first()
            }
