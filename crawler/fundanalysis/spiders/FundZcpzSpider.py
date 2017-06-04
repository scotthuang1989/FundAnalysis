# -*- coding: utf-8 -*-
#python standard library
import datetime
import logging
import sqlite3

# scrapy
import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import Request

#custome module
from .. import items
from . import FundIdSpider
import re


logger = logging.getLogger(__name__)

class FundspiderSpider(scrapy.Spider):
    name = "FundZcpzSpider"
    allowed_domains = ["http://fund.eastmoney.com"]

    def start_requests(self):
        url_template = "http://fund.eastmoney.com/f10/zcpz_{0}.html"
        all_fund_id = FundIdSpider.GetFundID()
        # test_run = 0
        for fund_id in all_fund_id:
            # test_run += 1
            # if test_run >1:
            #     break
            fund_id = fund_id[0]
            zcpz_item = items.ZcpzItem(item_id = "Fund_ZCPZ_Item",fund_id=fund_id)
            zcpz_request = Request(url=url_template.format(fund_id),callback=self.parse)
            zcpz_request.meta['item'] = zcpz_item
            yield zcpz_request

    def parse(self,response):
        temp_item = response.meta['item']

        # logger.info("extract zcpz")
        zcpz_rows = response.xpath('//*[@class="w782 comm tzxq"]/tbody/tr')

        for row in zcpz_rows:
            zcpz_tds = row.xpath("./td/text()").extract()
            zcpz_item = items.ZcpzItem(item_id = temp_item["item_id"],fund_id = temp_item['fund_id'],date=zcpz_tds[0],\
                                       stock=zcpz_tds[1][:-1],bond = zcpz_tds[2][:-1],currency = zcpz_tds[3][:-1],net_value = zcpz_tds[4])
            yield zcpz_item
