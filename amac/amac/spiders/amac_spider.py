# -*- coding: utf-8 -*-
import scrapy


class AmacSpiderSpider(scrapy.Spider):
    name = 'amac_spider'
    allowed_domains = ['www.amac.org.cn/xxgs/']
    start_urls = ['http://www.amac.org.cn/xxgs//']

    def parse(self, response):
        pass
