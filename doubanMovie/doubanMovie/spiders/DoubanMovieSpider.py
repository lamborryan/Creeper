#!/bin/env python
# coding:utf-8
"""
@author:ruanchengfeng 
@email=:ruanchengfeng@xiaomei.com  
@date=16/5/4
@project=Creeper
"""
from scrapy import Selector

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from doubanMovie.items import DoubanMovieItem, DoubanMovieReviewItem

class DoubanGroupSpider(CrawlSpider):
    name = 'doubanMovie'
    allowed_domains = ["movie.douban.com"]
    start_urls = [
        "https://movie.douban.com/tag/2015"
    ]

    rules = [

        # tag选取页选择时间tag(如2013), https://movie.douban.com/tag/
        Rule(LinkExtractor(allow=('/tag/\d{4}$'),restrict_xpaths=('//table[@class="tagCol"]')),
            follow=True, callback='parse_tag_time'),

        # movie的主页
        Rule(LinkExtractor(allow=('https://movie.douban.com/subject/\d+/$'),
                           restrict_xpaths=('//div[@class="article"]')),
            follow = True, callback = 'parse_movie_home_page'),

        # tag的分页(next)

        Rule(LinkExtractor(allow=('https://movie.douban.com/tag/\d{4}[?]start=.*?[&]type=T$'),
                           restrict_xpaths=('//span[@class="next"]')),
            callback='parse_tag_next_page',follow=True),

        # review的展示页  https://movie.douban.com/subject/10574468/reviews

        Rule(LinkExtractor(allow=('https://movie.douban.com/subject/\d+/reviews$'),
                           restrict_xpaths=('//div[@id="review_section"]')),
            callback='parse_home_review',follow=True),

        # review的next
        Rule(LinkExtractor(allow=('[?]start=\d+&filter=[&]limit=20$'),
                           restrict_xpaths=('//a[@class="next"]')),
            callback='parse_review_next', follow=True),

        # review的解析 https://movie.douban.com/review/7657435/
        Rule(LinkExtractor(allow=('https://movie.douban.com/review/\d+/$'),
                           restrict_xpaths=('//div[@class="article"]')),
                           callback='parse_home_review')
    ]

    def parse_movie_home_page(self, response):
        self.log("Fetch movie home page: %s" % response.url)

        sel = Selector(response)
        item = DoubanMovieItem()

        item['movieUrl'] = response.url

        item['movieName'] = sel.xpath('//h1/span/text()').extract_first(default=u"None")

        item['movieDirector'] = sel.xpath('//div[contains(@id,"info")]/span/span[contains(@class,"attrs")]/a/text()').extract()[0]

        item['movieScenarist'] = sel.xpath('//div[contains(@id,"info")]/span/span[contains(@class,"attrs")]/a/text()').extract()[1]

        item['movieActors'] = sel.xpath('//div[contains(@id,"info")]/span[contains(@class,"actor")]/span[contains(@class,"attrs")]/a/text()').extract()

        item['movieType'] = sel.xpath('//div[contains(@id,"info")]/span[contains(@property,"v:genre")]/text()').extract_first(default=u'None')

        contexts = filter(lambda x : len(x.strip()) > 0 and not x.strip().startswith(u'/'), sel.xpath('//div[contains(@id,"info")]/text()').extract())

        if len(contexts) >= 3:

            item['movieRegion'] = contexts[0]

            item['movieLanguage'] = contexts[1]

            item['movieOtherNames'] =  contexts[2]

        item['movieShowTime'] = sel.xpath('//div[contains(@id,"info")]/span[contains(@property,"v:initialReleaseDate")]/text()').extract()

        item['movieTime'] = sel.xpath('//div[contains(@id,"info")]/span[contains(@property,"v:runtime")]/text()').extract_first(default=u'None')

        item['movieScore'] = sel.xpath('//strong[contains(@property,"v:average")]/text()').extract_first(default=u"None")

        item['movieScoreNumber'] = sel.xpath('//span[contains(@property,"v:votes")]/text()').extract_first(default=u'None')

        item['movieCompare'] = sel.xpath('//div[contains(@class,"rating_betterthan")]/a/text()').extract()

        descrips = sel.xpath('//span[contains(@class,"all hidden")]/text()').extract()

        if not len(descrips):

            descrips = sel.xpath('//span[contains(@property,"v:summary")]/text()').extract()

        item['movieDescription'] = ''.join([des.strip() for des in descrips])

        item['movieTags'] = sel.xpath('//div[contains(@class,"tags-body")]/a/text()').extract()

        return item

    def parse_movie_next_page(self, response):
        self.log("Fetch movie next page: %s" % response.url)

    def parse_review(self, response):
        self.log("Fetch review page: %s" % response.url)
        pass

    def parse_home_review(self, response):
        self.log("Fetch home reviews page: %s" % response.url)

        sel = Selector(response)
        item = DoubanMovieReviewItem()

        item['reviewUrl'] = response.url

        item['movieUrl'] = sel.xpath('//div[contains(@class,"side-back")]/a/@href').extract_first(default=u'None')

        item['movieName'] = sel.xpath('//div[contains(@class,"side-back")]/a/text()').extract_first(default=u'None')

        item['commnetScore'] = sel.xpath('//span[contains(@property,"v:rating")]/text()').extract_first(default=u'None')

        item['commnetTitle'] = sel.xpath('//h1/span[contains(@property,"v:summary")]/text()').extract_first(default=u'None')

        item['commnetTime'] = sel.xpath('//span[contains(@property,"v:dtreviewed")]/text()').extract_first(default=u'None')

        item['commnetContent'] = u'\n'.join([ l.strip() for l in sel.xpath('//div[contains(@property, "v:description")]/text()').extract()])

        item['userName'] = sel.xpath('//span[contains(@property, "v:reviewer")]/text()').extract_first(default=u'None')

        item['userUrl'] = sel.xpath('//a[contains(@class,"main-avatar")]/@href').extract_first(default=u'None')

        return item

    def parse_tag_time(self, response):
        self.log("Fetch time tag page: %s" % response.url)
        pass

    def parse_tag_next_page(self, response):
        self.log("Fetch tag next page: %s" % response.url)
        pass