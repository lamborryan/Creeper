# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class DoubangroupItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    groupName = Field()
    groupURL = Field()
    totalNumber = Field()
    RelativeGroups = Field()
    ActiveUesrs = Field()
