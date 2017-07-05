# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy
from scrapy.loader import ItemLoader

from mynews.items import MynewsItem, NYItemLoader


class NYSpider(scrapy.Spider):
    name = "nytimes"
    allowed_domains = ["cn.nytimes.com"]
    start_urls = ["https://cn.nytimes.com/"]

    def parse(self, response):
        # for sel in response.xpath('//ul/li'):
        l = NYItemLoader(item=MynewsItem(), response=response)
        # l.add_xpath('title', '//h3/a/text()')
        l.add_xpath('title', '//h3[@class="articleHeadline"]/text()')
        l.add_xpath('urls', '//h3/a/@href')
        # l.add_xpath('content', '//h3/a/text()')
        l.add_xpath('content', '//div[@class="content chinese"]/p/text()')
        l.add_xpath('image_urls', "//img[@class='img-lazyload']/@data-url")
        l.add_xpath('author', '//meta[@name="byline"]/@content')
        l.add_xpath('date', '//meta[@name="date"]/@content')
        yield l.load_item()

        # next_href = response.xpath('//h3/a/@href').extract_first()
        # if next_href is not None:
        #     next_page = response.urljoin(next_href)
        #     print("========next_page=======%s" % next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
        for sel in response.xpath('//ul/li'):
            # 遍历首页h3新闻标题
            links = sel.xpath('//h3/a/@href').extract()
            for link in links:
                next_page = response.urljoin(link)
                # print("====next_page======%s" % next_page)
                yield scrapy.Request(next_page, callback=self.parse)

