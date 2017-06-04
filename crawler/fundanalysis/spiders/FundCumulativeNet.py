# -*- coding: utf-8 -*-
import scrapy
import sqlite3
import logging
from datetime import datetime
from .. import items

logger = logging.getLogger()


class FundcumulativenetSpider(scrapy.Spider):
    name = "FundCumulativeNet"
    allowed_domains = ["fund.easymondy.com"]
    # start_urls = ['http://fund.easymondy.com/']

    def start_requests(self):
        url_template = "http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={0}&page=1&per={1}&sdate=&edate=&rt=0.7948167527257904"
        # connect to database and get list od fund id
        try:
            conn = sqlite3.connect("FundProject.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * From FundBasicInfo")
        except:
            logging.error("Database error")
            return None
        # if database operation ok. then go on
        all_fund_info = cursor.fetchall()
        # count = 10
        conn.commit()
        conn.close()
        for fund_info in all_fund_info:
            #calculate how many record there are
            day_after_start = (datetime.now() - datetime.strptime(fund_info[3],"%Y-%m-%d")).days
            fund_item = items.FundNetValue(item_id="Fund_Val_Item", fund_id=fund_info[0])
            net_value_request= scrapy.Request(url_template.format( fund_info[0],day_after_start ),callback = self.parse )
            net_value_request.meta['item'] =fund_item
            yield net_value_request
            # count -=1
            # if not count:
            #     break

    def parse(self, response):
        trs = response.xpath("//table[@class='w782 comm lsjz']/tbody/tr")
        num_tr = len(trs)
        fund_item = response.meta['item']
        logger.info("{0} has {1} record".format(fund_item['fund_id'],num_tr))
        while num_tr-1 >= 0:
            tr = trs[num_tr-1]
            num_tr -= 1
            tds = tr.xpath("./td")
            # index 0: net value date
            record_date = tds[0].xpath("./text()").extract()
            if len(record_date) == 0:
                continue
            fund_item['val_date'] = record_date[0]

            #index 1: net value
            net_val = tds[1].xpath("./text()").extract()
            if len(net_val) == 0:
                continue
            fund_item['fund_net_val'] = float(net_val[0])

            # index 2: cum net value
            cum_net_val = tds[2].xpath("./text()").extract()
            if len(cum_net_val) == 0:
                continue
            fund_item['fund_cum_net_val'] = float(cum_net_val[0])
            #decrease num_tr
            logger.debug("yeild a item for pipline,fundid: "+fund_item["fund_id"])
            yield fund_item
