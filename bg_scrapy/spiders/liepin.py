# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule

from ..items import LiepinItem


class LpSpiderSpider(CrawlSpider):
    name = 'liepin'
    allowed_domains = ['www.liepin.com']
    #  key: java, dqs: 上海
    start_urls = ['https://www.liepin.com/zhaopin/?key={}&dqs={}'.format('财务', '020')]
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
        r = Selector(response)
        item = LiepinItem()

        title = r.xpath('//div[@class="title-info" or @class="title-info "]/h1/@title').extract_first()
        url = response.url
        salary = r.xpath(
            'normalize-space(//p[@class="job-item-title" or @class="job-main-title"]/text())').extract_first()
        location = r.xpath('string(//p[@class="basic-infor"]/span)').extract_first()
        if location:
            location = location.strip()
        location_href = r.xpath('//p[@class="basic-infor"]/span/a/@href').extract_first()
        pub_date = r.xpath('//p[@class="basic-infor"]/time/@title').extract_first()
        qualifications = r.xpath('//div[@class="job-qualifications"]//span/text()').extract()  # 企业
        if qualifications is None:
            # 猎头
            qualifications = r.xpath(
                '//div[contains(@class,"resume") and contains(@class,"clearfix")]//span/text()').extract()
        qualifications = ';'.join(qualifications)

        job_intro = r.xpath(
            'normalize-space(//div[contains(@class,"content") and contains(@class,"content-word")])').extract_first()
        company_name = r.xpath('//div[@class="company-logo"]/p/a/text()').extract_first()
        if company_name is None:
            company_name = r.xpath('//p[@class="company-name"]/@title').extract_first()
        company_href = r.xpath('//div[@class="company-logo"]/p/a/@href').extract_first()
        company_info = r.xpath('//ul[@class="new-compintro" or @class="new-compdetail"]//li[position() < last()]')
        li = []
        for i in company_info:
            v = i.xpath('string(.)').extract_first().strip()
            li.append(v)
        li = ';'.join(li)

        item['title'] = title
        item['url'] = url
        item['salary'] = salary
        item['location'] = location
        item['location_href'] = location_href
        item['pub_date'] = pub_date
        item['qualifications'] = qualifications
        item['job_intro'] = job_intro
        item['company_name'] = company_name
        item['company_href'] = company_href
        item['company_info'] = li
        yield item
