#!/bin/env python
# coding:utf-8
"""
@author:ruanchengfeng 
@email=:ruanchengfeng@xiaomei.com  
@date=16/4/28
@project=scrapy
"""
import re
from scrapy import Spider, Selector
from doubanGroup.items import DoubangroupItem


class DoubanGroupTestSpider(Spider):
    name = 'doubanGroupTest'
    allowed_domains = ["douban.com"]
    start_urls = ['https://www.douban.com/group/142121/']

    def __get_id_from_group_url(self, url):
        m =  re.search("^https://www.douban.com/group/([^/]+)/$", url)
        if(m):
            return m.group(1)
        else:
            return 0

    def parse(self, response):
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
