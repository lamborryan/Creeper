#!/bin/env python
# coding:utf-8
"""
@author:ruanchengfeng 
@email=:ruanchengfeng@xiaomei.com  
@date=16/5/4
@project=Creeper
"""

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from doubanMovie.items import DoubanmovieItem, DoubanmovieCommentItem

class DoubanGroupSpider(CrawlSpider):
    name = 'doubanMovie'
    allowed_domains = ["movie.douban.com"]
    start_urls = [
        "https://movie.douban.com/tag/"
    ]

    rules = [

        # tag选取页选择时间tag(如2013), https://movie.douban.com/tag/
        Rule(LinkExtractor(allow=('/tag/\d{4}$')), follow=True, callable='parse_tag_time'),

        # movie的主页
        Rule(LinkExtractor(allow=('https://movie.douban.com/subject/\d?/$')),
                           follow = True,
                           callback = 'parse_movie_next_page'),

        # tag的分页(next)

        Rule(LinkExtractor(allow=('https://movie.douban.com/tag/\d{4}[?]start=.*?[&]type=T$'),
                           restrict_xpaths=('//span[@class="next"]')),
                           callback='parse_next_page',
                           follow=True),

        # comment的展示页  https://movie.douban.com/subject/10574468/reviews

        Rule(LinkExtractor(allow=('https://movie.douban.com/subject/\d?/reviews$')),
                           callback='parse_comment_review',
                           follow=True),

        # comment的next
        Rule(LinkExtractor(allow=('[?]start=\d?&filter=[&]limit=20$'),
                           restrict_xpaths=('//span[@class="next"]')),
                           callable='parse_comment_next',
                           follow=True),

        # comment的解析 https://movie.douban.com/review/7657435/
        Rule(LinkExtractor(allow=('https://movie.douban.com/review/\d?/$')),
                           callable='parse_comment')
    ]

    def parse_movie_dim(self, response):
        pass

    def parse_movie_next_page(self, response):
        self.log("Fetch next page: %s" % response.url)