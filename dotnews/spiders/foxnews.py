# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from dotnews.items import NewsItem

class FoxnewsSpider(scrapy.Spider):
    name = 'foxnews'
    allowed_domains = ['foxnews.com']
    start_urls = ['http://www.foxnews.com']

    script = """
function main(splash)
     splash.images_enabled = false
     splash.resource_timeout = 100.0
     splash:autoload('http://code.jquery.com/jquery-2.1.3.min.js')
     assert(splash:go(splash.args.url))
     splash:wait(1)

     for i = 10,1,-1
     do
         splash:runjs("$('.js-load-more').click()")
         splash:wait(0.5)
     end

     return splash:html()
end
    """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,
                                self.parse,
                                args={})

    def parse(self, response):
        topic_urls_xpath = '//footer/div/div/nav/ul/li/a/@href'
        urls = response.xpath(topic_urls_xpath).extract()
        for url in urls:
            if 'category' in url:
                yield SplashRequest('https:' + url,
                                    self.parse_articles,
                                    endpoint='execute',
                                    args={'lua_source': self.script})

    def parse_articles(self, response):
        # meta tags
        category = response.xpath("//meta[@name='prism.subsection1']/@content")[0].extract()
        subcategory = response.xpath("//meta[@name='prism.subsection2']/@content")[0].extract()

        articles = response.xpath('//main/div/div/article')
        for article in articles:
            meta_xpath = './/div[@class="meta"]/span/a/text()'
            title_xpath = './/h2[@class="title"]/a/text()'
            abstract_xpath = './/div[@class="content"]/p/a/text()'

            yield {
                'category' : category,
                'subcategory' : subcategory,
                'meta' : article.xpath(meta_xpath).extract_first(),
                'title' : article.xpath(title_xpath).extract_first(),
                'short_description' : article.xpath(abstract_xpath).extract_first()
            }
