# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from doubanMovie.items import DoubanMovieItem
from doubanMovie.items import DoubanMovieReviewItem


class MongoDBPipeline(object):

     def __init__( self ):
         host = settings[ 'MONGODB_SERVER' ]
         port = settings[ 'MONGODB_PORT' ]
         db = settings[ 'MONGODB_DB' ]
         username = settings[ 'MONGODB_USE' ]
         password = settings[ 'MONGODB_PASWD' ]
         mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
         self.conn = MongoClient(mongo_uri)[db]


     def process_item( self , item, spider):
         if isinstance(item, DoubanMovieItem):
            table = settings['MONGODB_MOVIE_DIM_COLLECTION']
            self .collection = self.conn[table].update({'movieUrl': item['movieUrl']}, dict(item), upsert=True)
            log.msg( "Added to MongoDB database! {0}".format(table) ,level = log.DEBUG, spider = spider)
         elif isinstance(item, DoubanMovieReviewItem):
            table = settings['MONGODB_MOVIE_REVIEW_COLLECTION']
            self .collection = self.conn[table].update({'reviewUrl': item['reviewUrl']}, dict(item), upsert=True)
            log.msg( "Added to MongoDB database! {0}".format(table) ,level = log.DEBUG, spider = spider)

         else:
             raise DropItem("error item")
         return item
