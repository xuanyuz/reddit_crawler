# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CrawlerItem(scrapy.Item):
    title = scrapy.Field(serializer = str)
    id = scrapy.Field(serializer = str)
    author = scrapy.Field(serializer = str)
    author_id = scrapy.Field(serializer = str)
    subreddit = scrapy.Field(serializer = str)
    subreddit_id = scrapy.Field(serializer = str)
    subreddit_type = scrapy.Field(serializer = str)
    timestamp = scrapy.Field(serializer = str)
    url = scrapy.Field(serializer = str)
    href = scrapy.Field(serializer = str)
    domain = scrapy.Field(serializer = str)
    rank = scrapy.Field(serializer = int)
    score = scrapy.Field(serializer = int)
    comments_count = scrapy.Field(serializer = int)
    likes = scrapy.Field(serializer = int)
    type = scrapy.Field(serializer = str)

class CommentItem(scrapy.Item):
    id = scrapy.Field(serializer = str)
    author = scrapy.Field(serializer = str)
    author_id = scrapy.Field(serializer = str)
    timestamp = scrapy.Field(serializer = str)
    href = scrapy.Field(serializer = str)
    comment_id = scrapy.Field(serializer = str)
    parent_id = scrapy.Field(serializer = str)
    child_id = scrapy.Field(serializer = str)
    reply = scrapy.Field(serializer = int)
    likes = scrapy.Field(serializer = int)
    text = scrapy.Field(serializer = str)

