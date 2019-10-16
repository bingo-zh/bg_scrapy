# -*- coding: utf-8 -*-

# Define here the models for your scraped items
import scrapy


# 中国福利
class CwlItem(scrapy.Item):
    _id = scrapy.Field()
    key = scrapy.Field()
    name = scrapy.Field()
    code = scrapy.Field()
    date = scrapy.Field()
    week = scrapy.Field()
    red = scrapy.Field()
    blue = scrapy.Field()
    sales = scrapy.Field()
    poolmoney = scrapy.Field()
    content = scrapy.Field()
    prizegrades = scrapy.Field()
    detailsLink = scrapy.Field()
    videoLink = scrapy.Field()


# 猎聘网
class LiepinItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    salary = scrapy.Field()
    location = scrapy.Field()
    location_href = scrapy.Field()
    pub_date = scrapy.Field()
    qualifications = scrapy.Field()
    job_intro = scrapy.Field()
    company_name = scrapy.Field()
    company_href = scrapy.Field()
    company_info = scrapy.Field()


# 京东商品分类
class JdCatsItem(scrapy.Item):
    _id = scrapy.Field()
    cat_href = scrapy.Field()


# 京东商品详情
class JdGoodsItem(scrapy.Item):
    _id = scrapy.Field()
    sku = scrapy.Field()
    sku_name = scrapy.Field()
    info_href = scrapy.Field()
    parameter_list = scrapy.Field()
    price = scrapy.Field()
    CommentsCount = scrapy.Field()
