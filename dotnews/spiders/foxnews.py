# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from dotnews.items import NewsItem, NewsItemLoader

class FoxnewsSpider(scrapy.Spider):
    name = 'foxnews'
    allowed_domains = ['foxnews.com']
    start_urls = [
        'http://www.foxnews.com/category/us/crime.html',
        'http://www.foxnews.com/category/us/military.html',
        'http://www.foxnews.com/category/us/education.html',
        'http://www.foxnews.com/category/us/terror.html',
        'http://www.foxnews.com/category/us/immigration.html',
        'http://www.foxnews.com/category/us/personal-freeedoms.html',
        'http://www.foxnews.com/category/world/united-nations.html',
        'http://www.foxnews.com/category/world/conflicts.html',
        'http://www.foxnews.com/category/world/terrorism.html',
        'http://www.foxnews.com/category/world/disasters.html',
        'http://www.foxnews.com/category/world/global-economy.html',
        'http://www.foxnews.com/category/world/environment.html',
        'http://www.foxnews.com/category/world/world-religion.html',
        'http://www.foxnews.com/category/world/scandals.html'
    ]

    script = """
function main(splash)
     splash.images_enabled = false
     splash.resource_timeout = 100.0
     splash:autoload('http://code.jquery.com/jquery-2.1.3.min.js')
     assert(splash:go(splash.args.url))
     splash:wait(1)

     for i = 1,11
     do
         ok, reason = splash:runjs("$('.js-load-more').click()")
         splash:wait(1.0)
     end

     return splash:html()
end
    """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,
                                self.parse,
                                endpoint='execute',
                                args={'lua_source': self.script})

    def parse(self, response):
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
