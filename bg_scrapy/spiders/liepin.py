# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule

from ..items import LiepinItem


class LpSpiderSpider(CrawlSpider):
    name = 'liepin'
    allowed_domains = ['www.liepin.com']
    #  java, 上海区域
    start_urls = ['https://www.liepin.com/zhaopin/?key={}&dqs={}'.format('java', '020')]
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml'
                      ';q=0.9,image/webp,image/apng,*/*'
                      ';q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'www.liepin.com',
        }
    }
    rules = (
        # 下一页
        Rule(LinkExtractor(allow=('/zhaopin/',), restrict_xpaths='//div[@class="pagerbar"]/a[last()-1]'),
             follow=True),
        # 详情
        Rule(LinkExtractor(allow=('[0-9].shtml',), restrict_xpaths='//div[@class="job-info"]//a'),
             callback='parse_item', ),
    )

    def parse_item(self, response):
        resp = Selector(response)
        item = LiepinItem()
        # company_name = scrapy.Field()
        # company_href = scrapy.Field()
        # company_info = scrapy.Field()

        title = resp.xpath('//div[@class="title-info" or @class="title-info "]/h1/text()').extract_first()
        url = response.url
        salary = resp.xpath(
            'normalize-space(//p[@class="job-item-title" or @class="job-main-title"]/text()').extract_first()
        location = resp.xpath('normalize-space(//p[@class="basic-infor"]/span/text())').extract_first()
        location_href = resp.xpath('//p[@class="basic-infor"]/span/a/@href').extract_first()
        pub_date = resp.xpath('//p[@class="basic-infor"]/time/@title').extract_first()
        qualifications_list = []
        qualifications = resp.xpath('//div[@class="job-qualifications"]//span')
        for q in qualifications:
            qualifications_list.append(q.xpath('./text()').extract_first())
        job_intro = resp.xpath(
            'string(//div[contains(@class,"content") and contains(@class,"content-word")])').extract_first()
        company_name = resp.xpath('//div[@class="company-logo"]/p/a/text()').extract_first()
        company_href = resp.xpath('//div[@class="company-logo"]/p/a/@href').extract_first()
        company_info = resp.xpath('//div[@class="company-logo"]/p/a/text()').extract_first()



        yield item
