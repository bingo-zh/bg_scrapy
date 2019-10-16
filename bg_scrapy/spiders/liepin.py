# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule

from ..items import LiepinItem


class LpSpiderSpider(CrawlSpider):
    name = 'liepin'
    allowed_domains = ['www.liepin.com']
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml'
                  ';q=0.9,image/webp,image/apng,*/*'
                  ';q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'www.liepin.com',
    }
    rules = (
        # 下一页
        Rule(LinkExtractor(allow=(r'/zhaopin/',), restrict_xpaths='//div[@class="pagerbar"]/a[last()-1]'),
             follow=True),
        # 详情
        Rule(LinkExtractor(allow=(r'[0-9].shtml',), restrict_xpaths='//div[@class="job-info"]//a'),
             callback='parse_item', ),
    )
    key = 'java'
    dqs = '020'

    # 访问入口
    def start_requests(self):
        url = 'https://www.liepin.com/zhaopin/?key={}&dqs={}'.format(self.key, self.dqs)
        yield scrapy.Request(url=url, headers=self.headers)

    def parse_item(self, response):
        l = ItemLoader(item=LiepinItem(), response=response)
        url = response.url
        l.add_value('url', url)
        if url.find('a') > -1:
            # 猎头
            l.add_value('pub_type', 'hunter')
            l.add_xpath('title', '//div[@class="title-info "]/h1/text()')
            l.add_xpath('company', 'normalize-space(//div[@class="title-info "]/h3/text())')
            l.add_xpath('salary', 'normalize-space(//p[@class="job-main-title"]/text())')
            qualifications = response.xpath('//div[contains(@class,"resume") and contains(@class,"clearfix")]//span')
            q_list = []
            for q in qualifications:
                q_list.append(q.xpath('./text()').extract_first())
            l.add_value('qualifications', ';'.join(q_list))
            l.add_xpath('hunter_name', '//p[@class="hunter-name"]/span/text()')
            l.add_xpath('hunter_company', '//p[@class="company-name"]/@title')
        else:
            # 公司
            l.add_value('pub_type', 'company')
            l.add_xpath('title', '//div[@class="title-info"]/h1/text()')
            l.add_xpath('company', '//div[@class="title-info"]/h3/a/text()')
            l.add_xpath('company', '//div[@class="title-info"]/h3/a/@href')
            l.add_xpath('salary', 'normalize-space(//p[@class="job-item-title"]/text())')
            qualifications = response.xpath('//div[@class="job-qualifications"]//span')
            q_list = []
            for q in qualifications:
                q_list.append(q.xpath('./text()').extract_first())
            l.add_value('qualifications', ';'.join(q_list))
            compintro = response.xpath('//ul[@class="new-compintro"]//li')
            c_list = []
            for c in compintro:
                c_list.append(c.xpath('string(.)').extract_first().strip())
            l.add_value('compintro', ';'.join(c_list))

            compdetail = response.xpath('//ul[@class="new-compdetail"]//li')
            d_list = []
            for c in compdetail:
                d_list.append(c.xpath('string(.)').extract_first().strip())
            l.add_value('compdetail', ';'.join(d_list))

        l.add_xpath('address', 'normalize-space(//p[@class="basic-infor"]/span)')
        l.add_xpath('address', 'string(//p[@class="basic-infor"]/span/a/@href)')
        l.add_xpath('pub_date', '//p[@class="basic-infor"]/time/@title')

        main_message = response.xpath('//div[contains(@class,"main-message")]')
        for m in main_message:
            h1 = m.xpath('./h3/text()').extract_first()
            content = m.xpath('normalize-space(./div)').extract_first()
            l.add_value('main_message', h1 + content + ';')

        yield l.load_item()
