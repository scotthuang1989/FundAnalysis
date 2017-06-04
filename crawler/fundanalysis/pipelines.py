# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter
from scrapy.exporters import CsvItemExporter
from scrapy.exceptions import DropItem
from scrapy import signals
import sqlite3
import logging
import os

logger = logging.getLogger(__name__)
# g_processed_counter = 0

# class FundanalysisPipeline(object):
#
#     def __init__(self):
#         self.files = {}
#         self.processed_counter=0
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         pipeline = cls()
#         crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
#         crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
#         return pipeline
#
#     def spider_opened(self, spider):
#         file = open('%s_products.json' % spider.name, 'w+b')
#         self.files[spider] = file
#         self.exporter = JsonItemExporter(file)
#         self.exporter.start_exporting()
#
#     def spider_closed(self, spider):
#         self.exporter.finish_exporting()
#         file = self.files.pop(spider)
#         file.close()
#
#     def process_item(self, item, spider):
#         self.processed_counter +=1
#         logger.info("process_item:%d", self.processed_counter)
#         self.exporter.export_item(item)
#         return item
#
#
# class FundIdPipeline(object):
#     def __init__(self):
#         self.file = open("FundId.csv", 'wb')
#         self.exporter = CsvItemExporter(self.file, include_headers_line=True)
#         self.exporter.start_exporting()
#
#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()
#
#     def process_item(self, item, spider):
#         if item["item_id"] == "Fund_ID_Item":
#             logger.info("FundId processor")
#             logger.info(item)
#             self.exporter.export_item(item)
#         else:
#             return item


class FundIdPipelineToDatabase(object):
    def __init__(self):
        self.files = {}
        self.processed_counter=0

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        # connect to database and get cursor.
        logger.debug("FundIdPipelineToDatabase open")
        self.conn = sqlite3.connect('FundProject.db')
        self.cursor = self.conn.cursor()

    def spider_closed(self, spider):
        # close and commit to database.
        self.conn.commit()
        self.conn.close()
        logger.info("FundIdPipelineToDatabase close")

    def process_item(self, item, spider):
        # IF ITEM_ID mathced, write to database
        logger.debug("FundIdPipelineToDatabase process"+os.getcwd())
        if item["item_id"] == "Fund_ID_Item":
            # logger.info("FundIdPipelineToDatabase binggo")
            try:
                self.cursor.execute("INSERT INTO FundBasicInfo VALUES(?,?,?,?,?)",
                                    (item["fund_id"], item["fund_cate"], item["fund_scale"], item["fund_start_date"],
                                     item["fund_corp"]))
            except:
                logger.error("Insert Error:"+item["fund_id"])
            raise DropItem
        else:
            return item


class FundValToDatabase(object):
    def __init__(self):
        self.files = {}
        self.processed_counter=0
        self.count=0

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        #connect to database and get cursor.
        logger.info("FundValToDatabase open")
        self.conn = sqlite3.connect('FundProject.db')
        self.cursor = self.conn.cursor()
    def spider_closed(self, spider):
        #close and commit to database.
        self.conn.commit()
        self.conn.close()
        logger.info("FundValToDatabase close")
    def process_item(self, item, spider):
        # IF ITEM_ID mathced, write to database
        if item["item_id"] != "Fund_Val_Item":
            return item
        #first check if database table for this ID exsist.
        table_name = "FundNetValue"+str(item["fund_id"])
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=? ",(table_name,))
        if not (self.cursor.fetchall()):
            try:
                self.cursor.execute("""
                CREATE TABLE {0} (
                `NetValueDate`	TEXT NOT NULL,
                `NetValue`	REAL NOT NULL,
                `CumNetValue`	REAL NOT NULL,
                PRIMARY KEY(`NetValueDate`)
                )
                """.format(table_name))
            except:
                raise DropItem
        # then write date to database
        insert_data="INSERT INTO {0} VALUES( '{1}',{2},{3})".format(table_name, item["val_date"],
                                                   item["fund_net_val"], item["fund_cum_net_val"])
        try:
            self.cursor.execute(insert_data)
        except:
            logger.info("Data exist; skip.")
        raise DropItem


class FundZcpzToDatabase(object):
    def __init__(self):
        self.files = {}
        self.processed_counter=0
        self.count=0

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        #connect to database and get cursor.
        logger.info("FundValToDatabase open")
        self.conn = sqlite3.connect('FundProject.db')
        self.cursor = self.conn.cursor()
    def spider_closed(self, spider):
        #close and commit to database.
        self.conn.commit()
        self.conn.close()
        logger.info("FundValToDatabase close")
    def process_item(self, item, spider):
        # IF ITEM_ID mathced, write to database
        if item["item_id"] != "Fund_ZCPZ_Item":
            return item
        # insert_data="INSERT INTO zcpz_tbl VALUES( ?,?,?,?,?,? )".format(item["fund_id"],\
        #                                            item["date"], item["stock"], item["bond"], item["currency"],\
        #                                                                             item["net_value"])
        # logging.info(insert_data)
        try:
            self.cursor.execute("INSERT INTO zcpz_tbl VALUES( ?,?,?,?,?,? )",(item["fund_id"],\
                                                   item["date"], item["stock"], item["bond"], item["currency"],\
                                                                                    item["net_value"]))
        except Exception as exception:
            logger.error("zcpz pipeline excption: " + str(exception))
        # logging.info("TEST 001: %s %s %s %s %s %s",item["fund_id"],
        #                                             item["date"], item["stock"], item["bond"], item["currency"],\
        #                                                                              item["net_value"])
        raise DropItem
