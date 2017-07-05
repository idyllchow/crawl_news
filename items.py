# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import Identity, ItemLoader


class MynewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    urls = scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    last_updated = scrapy.Field()
    # 图片
    image_urls = scrapy.Field()
    images = scrapy.Field()


class NYItemLoader(ItemLoader):
    default_item_class = MynewsItem
    default_output_processor = Identity()