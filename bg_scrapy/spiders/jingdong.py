# -*- coding: utf-8 -*-
import json
import random
import time

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import JdCatsItem, JdGoodsItem


class JdItemsSpider(CrawlSpider):
    name = 'jd_items'
    headers = {
        'authority': 'www.jd.com',
        ':method': 'GET',
        ':path': '/allSort.aspx',
        ':scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml'
                  ';q=0.9,image/webp,image/apng,*/*'
                  ';q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'referer': 'https://jiadian.jd.com/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36',
    }
    rules = (

        #  商品分类
        Rule(LinkExtractor(allow=(r'.*(list\.jd\.com\/list\.html\?cat=)[0-9\,]*$',),
                           restrict_xpaths='//div[@class="items"]/dl/dd/a',
                           tags=('a',),
                           attrs=('href',)),
             callback='record_cat',
             follow=True),

        #  下一页
        Rule(LinkExtractor(restrict_xpaths='//a[@class="pn-next"]',
                           tags=('a',),
                           attrs=('href',)),
             follow=True),

        #  商品详情
        Rule(LinkExtractor(allow=(r'.*(item\.jd\.com/)(\d)*\.html',),
                           restrict_xpaths='//li[@class="gl-item"]//a',
                           tags=('a',),
                           attrs=('href',)),
             callback='parse_info',
             follow=True),

    )

    # 访问入口
    def start_requests(self):
        url = 'http://www.jd.com/allSort.aspx/'
        yield scrapy.Request(url=url, headers=self.headers, dont_filter=True)

    cat_list = []

    #  记录cat
    def record_cat(self, response):
        url = response.url
        if url not in self.cat_list:
            self.cat_list.append(url)
            item = JdCatsItem()
            item['cat_href'] = url
            yield item

    info_list = []

    #  产品详情
    def parse_info(self, response):
        url = response.url
        sku = url[url.index('/', 12) + 1:url.index('.html')]
        if url not in self.info_list:
            self.info_list.append(url)
            obj = {}
            parameter_list = []
            p_l = response.xpath('//div[@class="p-parameter"]//li')
            for l in p_l:
                v = l.xpath('normalize-space(string(.))').extract_first()
                parameter_list.append(v)
            obj['sku'] = sku
            obj['sku_name'] = response.xpath('normalize-space(//div[@class="sku-name"])').extract_first()
            obj['info_href'] = url
            obj['parameter_list'] = parameter_list
            price_url = 'https://p.3.cn/prices/mgets?skuIds=J_{}&type=1'.format(sku)
            yield scrapy.Request(url=price_url, callback=self.parse_price, meta={'obj': obj})

    def parse_price(self, response):
        obj = response.meta['obj']
        result = json.loads(response.text)
        price = result[0]
        obj['price'] = price
        comment_url = 'https://club.jd.com/comment/productCommentSummaries.action' \
                      '?referenceIds={}' \
                      '&callback=jQuery{}' \
                      '&_={}'.format(obj['sku'], random.randrange(1000000, 9999999), int(time.time()))
        yield scrapy.Request(url=comment_url, callback=self.total, meta={'obj': obj})

    def total(self, response):
        obj = response.meta['obj']
        result = response.body_as_unicode()
        content = result[result.index('(') + 1: result.index(')')]
        content = json.loads(content)
        obj['CommentsCount'] = content['CommentsCount']
        item = JdGoodsItem(obj)
        yield item