# -*- coding: utf-8 -*-
import scrapy
import logging
import re
from scrapy.http import Request
from .. import items
import sqlite3

logger = logging.getLogger(__name__)

fund_scale_re = re.compile(r"([0-9.]+)亿元")
fund_start_date_re = re.compile("[0-9]{4,4}-[0-1][0-9]-[0-3][0-9]")


class FundidspiderSpider(scrapy.Spider):
    name = "FundIdSpider"
    allowed_domains = ["fund.eastmoney.com"]
    start_urls = (
        'http://fund.eastmoney.com/fundguzhi.html',
    )

    def parse(self, response):
        #1st: get a list of id of all funds.
        id_rows = response.xpath("//table[@class='dbtable']/tbody/tr")
        id_list = [i.xpath("./td/text()").extract()[1] for i in id_rows]

        logger.info("length of id_list:%d",len(id_list))
        if len(id_list) ==0:
            return None
        # count = 5
        for id_fund in id_list:
            # if count ==0:
            #     break;
            # count -= count
            fund_item = items.FundIdItem( item_id = "Fund_ID_Item", fund_id=id_fund)
            # yield a request for zcpz
            zcpz_request = Request(str.format("http://fund.eastmoney.com/{0}.html", id_fund),  callback=self.parse_fund)
            zcpz_request.meta['item'] = fund_item
            # logger.info(zcpz_request.url)
            # logger.info(zcpz_request.callback)
            yield zcpz_request

    def parse_fund(self, response):
        # data_loader = ItemLoader(item=FundanalysisItem(),response=response)
        fund_item = response.meta['item']

        trs = response.xpath("//div[@class='infoOfFund']/table/tr")
        # ['基金类型：', '\xa0\xa0|\xa0\xa0中高风险', '：25.48亿元（2017-03-31）', '基金经理：']
        first_row = trs[0].xpath("./td/text()").extract()
        # logger.debug(first_row)
        #Fund category
        fund_item['fund_cate'] = trs[0].xpath("./td")[0].xpath("./a/text()").extract()[0]
        # fund scale
        fund_item['fund_scale'] = trs[0].xpath("./td")[1].xpath("./text()").extract()
        fund_item['fund_scale'] = fund_scale_re.findall(fund_item['fund_scale'][0])[0]
        # fund corp
        fund_item['fund_corp'] = trs[1].xpath("./td")[1].xpath("./a/text()").extract()[0]
        # fund start date
        fund_item['fund_start_date'] = trs[1].xpath("./td/text()").extract()
        fund_item['fund_start_date'] = fund_start_date_re.findall(fund_item['fund_start_date'][0])[0]
        return fund_item


def GetFundID():
    try:
        conn = sqlite3.connect('FundProject.db')
        cursor = conn.cursor()
        cursor.execute("SELECT fund_id FROM FundBasicInfo")
    except:
        logging.error("Database error: can't get fund ID")
        return None
    return cursor.fetchall()