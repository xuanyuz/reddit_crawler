# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    timestamp = scrapy.Field()
    category = scrapy.Field()
    comments = scrapy.Field()
    likes = scrapy.Field()
    dislikes = scrapy.Field()
    unvoted = scrapy.Field()
    rank = scrapy.Field()
    author = scrapy.Field()
    type = scrapy.Field()

