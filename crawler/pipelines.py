# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class CrawlerPipeline(object):
    def __init__(self):
        self.file = open('/Users/xuanyuzhou/python/crawler/crawler.json', 'w')

    def process_item(self, item, spider):
        text = json.dumps(dict(item), ensure_ascii=False)
        text = text +'\n'
        self.file.write(text.encode('utf-8'))

    def close(self):
        self.file.close()