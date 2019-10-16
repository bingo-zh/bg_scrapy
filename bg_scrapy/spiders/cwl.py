# -*- coding: utf-8 -*-
import json

import scrapy

from ..items import CwlItem


class CwlSpider(scrapy.Spider):
    name = 'cwl'
    allowed_domains = ['www.cwl.gov.cn']
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'www.cwl.gov.cn',
            'Referer': 'http://www.cwl.gov.cn/kjxx/ssq/kjgg/',
            'X-Requested-With': 'XMLHttpRequest'
        }
    }

    def start_requests(self):
        keys = ['ssq', 'qlc', '3d']
        count = 100
        urls = [{'key': k,
                 'url': 'http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name={}&issueCount={}'.format(k, count)}
                for k in keys]
        for u in urls:
            yield scrapy.Request(url=u['url'], meta={'key': u['key']}, callback=self.parse_info)

    def parse_info(self, response):
        result = json.loads(response.body_as_unicode())
        data = result.get('result')
        key = response.meta['key']
        for i in data:
            item = CwlItem()
            item['key'] = key
            item['name'] = i.get('name')
            item['code'] = i.get('code')
            item['date'] = i.get('date')
            item['week'] = i.get('week')
            item['red'] = i.get('red')
            item['blue'] = i.get('blue')
            item['sales'] = i.get('sales')
            item['poolmoney'] = i.get('poolmoney')
            item['content'] = i.get('content')
            item['prizegrades'] = i.get('prizegrades')
            item['detailsLink'] = i.get('detailsLink')
            item['videoLink'] = i.get('videoLink')
            yield item
