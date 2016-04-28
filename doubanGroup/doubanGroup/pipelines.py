# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

class MongoDBPipeline(object):

     def __init__( self ):
         host = settings[ 'MONGODB_SERVER' ]
         port = settings[ 'MONGODB_PORT' ]
         db = settings[ 'MONGODB_DB' ]
         username = settings[ 'MONGODB_USE' ]
         password = settings[ 'MONGODB_PASWD' ]
         table = settings[ 'MONGODB_COLLECTION' ]
         mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
         conn = MongoClient(mongo_uri)
         self .collection = conn[db][table]

     def process_item( self , item, spider):
         valid = True
         for data in item:
           if not data:
             valid = False
             raise DropItem( "Missing {0}!" . format(data))
         if valid:
           self.collection.update({'groupURL': item['groupURL']}, dict(item), upsert=True)
           log.msg( "Question added to MongoDB database!" ,level = log.DEBUG, spider = spider)
         return item