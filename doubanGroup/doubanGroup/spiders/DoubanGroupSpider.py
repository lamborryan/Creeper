#!/bin/env python
# coding:utf-8
"""
@author:ruanchengfeng 
@email=:ruanchengfeng@xiaomei.com  
@date=16/4/27
@project=scrapy
"""
import re

import scrapy
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import  Rule, CrawlSpider
from scrapy.contrib.linkextractors import LinkExtractor
from doubanGroup.items import DoubangroupItem


class DoubanGroupSpider(CrawlSpider):
    name = 'doubanGroup'
    allowed_domains = ["douban.com"]
    start_urls = [
        "http://www.douban.com/group/explore?tag=%E8%B4%AD%E7%89%A9",
        "http://www.douban.com/group/explore?tag=%E7%94%9F%E6%B4%BB",
        "http://www.douban.com/group/explore?tag=%E7%A4%BE%E4%BC%9A",
        "http://www.douban.com/group/explore?tag=%E8%89%BA%E6%9C%AF",
        "http://www.douban.com/group/explore?tag=%E5%AD%A6%E6%9C%AF",
        "http://www.douban.com/group/explore?tag=%E6%83%85%E6%84%9F",
        "http://www.douban.com/group/explore?tag=%E9%97%B2%E8%81%8A",
        "http://www.douban.com/group/explore?tag=%E5%85%B4%E8%B6%A3"
    ]

    rules = [
        Rule(LinkExtractor(allow=('/group/[^/]+/$', )), callback='parse_group_home_page'),
        Rule(LinkExtractor(allow=('/group/explore\?tag')), follow=True),
    ]

    def __get_id_from_group_url(self, url):
        m =  re.search("^https://www.douban.com/group/([^/]+)/$", url)
        if(m):
            return m.group(1)
        else:
            return 0

    def add_cookie(self, request):
        request.replace(cookies=[])
        return request

    def parse_group_home_page(self, response):
        self.log("Fetch douban homepage page: %s" % response.url)
        sel = Selector(response)
        item = DoubangroupItem()
        item['groupName'] = sel.xpath('//h1/text()').re("^\s+(.*)\s+$")[0]
        #get group id
        item['groupURL'] = response.url
        groupid = self.__get_id_from_group_url(response.url)

        #get group members number
        members_url = "https://www.douban.com/group/%s/members" % groupid
        members_text = sel.xpath('//a[contains(@href, "%s")]/text()' % members_url).re("\((\d+)\)")
        item['totalNumber'] = members_text[0]

        #get relative groups
        item['RelativeGroups'] = []
        groups = sel.xpath('//div[contains(@class, "group-list-item")]')
        for group in groups:
            url = group.xpath('div[contains(@class, "title")]/a/@href').extract()[0]
            item['RelativeGroups'].append(url)

        return item