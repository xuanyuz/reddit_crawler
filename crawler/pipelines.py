# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from crawler.items import CrawlerItem,CommentItem

class CrawlerPipeline(object):
    def __init__(self):
        self.file1 = open('./crawler.json', 'w')
        self.file2 = open('./comment.json', 'w')

    def process_item(self, item, spider):
        if isinstance(item, CrawlerItem):
            text = json.dumps(dict(item), ensure_ascii=False)
            text = text + '\n'
            self.file1.write(text.encode('utf-8'))
        elif isinstance(item, CommentItem):
            text = json.dumps(dict(item), ensure_ascii=False)
            text = text + '\n'
            self.file2.write(text.encode('utf-8'))

    def close(self):
        self.file1.close()
        self.file2.close()
'''
import pymongo

class CrawlerPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client.reddit
        self.picture_storage = db.picture_storage
        self.comments = db.comments
        
    def process_item(self, item, spider):
        if isinstance(item, CrawlerItem):
            id = self.picture_storage.insert(dict(item))
        elif isinstance(item, CommentItem):
            id = self.comments.insert(dict(item))
'''