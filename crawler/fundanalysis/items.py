# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

# class FundanalysisItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     # HouseKeeping fields
#     url = Field()
#     date = Field()
#     fund_id = Field()
#     fund_category = Field()
#     #scrapied data
#     zcpz_table = Field()


# def Serialize_Corp(value):
#     return value.encode("UTF-16")


class FundIdItem(scrapy.Item):
    item_id = Field()
    fund_id = Field()
    fund_cate = Field()
    fund_scale = Field()
    fund_start_date = Field()
    # fund_corp = Field(serializer=Serialize_Corp)
    fund_corp = Field()


class FundNetValue(scrapy.Item):
    item_id = Field()
    fund_id = Field()
    val_date = Field()
    fund_net_val = Field()
    fund_cum_net_val = Field()


class ZcpzItem(scrapy.Item):
    item_id = Field()
    fund_id = Field()
    date = Field()
    stock = Field()
    bond = Field()
    currency = Field()
    net_value = Field()