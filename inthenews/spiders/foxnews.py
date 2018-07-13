# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from inthenews.items import NewsItem

class FoxnewsSpider(scrapy.Spider):
    name = 'foxnews'
    allowed_domains = ['foxnews.com']
    start_urls = ['http://www.foxnews.com']
    #start_urls = ['http://www.foxnews.com/category/politics/executive.html']

    # TODO click 'Show more' and capture more articles
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={})

    def parse(self, response):
        topic_urls_xpath = '//footer/div/div/nav/ul/li/a/@href'
        urls = response.xpath(topic_urls_xpath).extract()
        for url in urls:
            if 'category' in url:
                yield SplashRequest("https:" + url, self.parse_articles, args={})

    def parse_articles(self, response):
        # meta tags
        category = response.xpath("//meta[@name='prism.subsection1']/@content")[0].extract()
        subcategory = response.xpath("//meta[@name='prism.subsection2']/@content")[0].extract()

        articles = response.xpath('//main/div/div/article')
        for article in articles:
            meta_xpath = './/div[@class="meta"]/span/a/text()'
            title_xpath = './/h2[@class="title"]/a/text()'
            abstract_xpath = './/div[@class="content"]/p/a/text()'

            self.log(article)
            yield {
                'category' : category,
                'subcategory' : subcategory,
                'meta' : article.xpath(meta_xpath).extract_first(),
                'title' : article.xpath(title_xpath).extract_first(),
                'short_description' : article.xpath(abstract_xpath).extract_first()
            }
