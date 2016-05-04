# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class DoubanmovieItem(scrapy.Item):

    """moive dim"""

    # 电影url
    movieUrl = Field()

    # 名字
    movieName = Field()

    # 导演
    movieDirector = Field()

    # 编剧
    movieScenarist = Field()

    # 主演
    movieActors = Field()

    # 类型
    movieType = Field()

    # 国家
    movieCountry = Field()

    # 地区
    movieRegion = Field()

    # 语言
    movieLanguage = Field()

    # 上映时间
    movieShowTime = Field()

    # 重映时间(可空)
    movieUpdateShowTime = Field()

    # 片长
    movieTime = Field()

    # 又名
    movieOtherNames = Field()

    # 打分
    movieScore = Field()

    # 评论个数
    movieScoreNumber = Field()

    # 与其他电影比较
    movieCompare = Field()

    # 影片简介
    movieDescription = Field()

    # 影片tag
    movieTags = Field()

class DoubanmovieCommentItem(scrapy.Item):

    """ movie comment fact"""

    # 电影url
    movieUrl = Field()

    # 电影名字
    movieName = Field()

    # 评分
    commnetScore = Field()

    # 评论title
    commnetTitle = Field()

    # 评论时间
    commnetTime = Field()

    # 评论内容
    commnetContent = Field()

    # user name
    userName = Field()

    # user url
    userUrl = Field()
