# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    abstract = scrapy.Field()
    content = scrapy.Field()
    topic = scrapy.Field()
    date = scrapy.Field()
    source = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
