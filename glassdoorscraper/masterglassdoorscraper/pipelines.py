# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from masterglassdoorscraper.items import ReviewItem, SalaryItem, CompanyInfoItem, CompanyUrlsItem, InterviewItem
from datetime import datetime, timedelta
from scrapy import log

import pdb

class MasterglassdoorscraperPipeline(object):
    def process_item(self, item, spider):
        return item

class MultiCSVItemPipeline(object):
    SaveTypes = ['SalaryItem','ReviewItem','InterviewItem', 'CompanyInfoItem', 'CompanyUrlsItem']

    SALARY_ITEM_FIELDS = [
        "scrape_date",
        "scrape_time",
        "company_name", 
        "salaries_cnt", 
        "jobs_count",
        "pos_cnt",
        "updated",
        "position_url",        
        "avg_sal",
        "low_sal",
        "high_sal",
        "salaries_page_url", 
        "total_compensation",
        "base_pay",
        "total_pay_low", 
        "total_pay_high", 
        "cash_bonuses_cnt",
        "cash_bonuses_avg",
        "cash_bonuses_low",
        "cash_bonuses_high",
        "stock_cnt",
        "stock_avg",
        "stock_low",
        "stock_high",
        "position"
        ]

    INTERVIEW_ITEM_FIELDS = [
        "scrape_date",
        "scrape_time",
        "interviewUrl",
        "interviewsCnt",
        "company",
        "updated",
        "interDif",
        "posInter",
        "neutInter",
        "negInter",
        "getAnInt1Desc",
        "getAnInt1Perc",
        "getAnInt2Desc",
        "getAnInt2Perc",
        "getAnInt3Desc",
        "getAnInt3Perc",
        "getAnInt4Desc",
        "getAnInt4Perc",
        "getAnInt5Desc",
        "getAnInt5Perc",
        "getAnInt6Desc",
        "getAnInt6Perc",
        "getAnInt7Desc",
        "getAnInt7Perc",
        "reviewDate",
        "position",
        "location",
        "dateInterview",
        "appDetails",
        "interDetails",
        "interQuestions",
        "negotDetails",
        "sq1Color",
        "sq1Txt",
        "sq2Color",
        "sq2Txt",
        "sq3Color",
        "sq3Txt",
        "numberHelpful"
        ]

    REVIEW_ITEM_FIELDS = [
        "scrape_date",
        "scrape_time",
        "company_name",
        "reviewUrl",
        "reviewDate",
        "title",
        "rating",
        "currentFormer",
        "position",
        "location",
        "fullPartTime",
        "tenure",
        "pros", 
        "cons",
        "advice",
        "sq1Color",
        "sq1Txt",
        "sq2Color",
        "sq2Txt", 
        "sq3Color",
        "sq3Txt"
        ]

    COMPANY_URLS_ITEM_FIELDS = [
        "company_name",
        "salaries_url",
        "overview_url",
        "reviews_url",
        "interviews_url"
        ]


    COMPANY_INFO_ITEM_FIELDS = [
        "company_name",
        "AverageRating",
        "ReviewsCNT",
        "RecToFriend",
        "ApprCEO",
        "CEOName", 
        "CEORateCNT",
        "CompanyWebsite", 
        "Size",
        "Type",
        "Ticker",
        "Revenue",
        "HQ",
        "Founded",
        "Industry",
        "Competitors",
        "Text",
        "Mission"
        ]

    ordering = {'SalaryItem': SALARY_ITEM_FIELDS, 'ReviewItem': REVIEW_ITEM_FIELDS, 'InterviewItem': INTERVIEW_ITEM_FIELDS, 'CompanyInfoItem': COMPANY_INFO_ITEM_FIELDS, 'CompanyUrlsItem': COMPANY_URLS_ITEM_FIELDS}

    def __init__(self):
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)
        LOG_FILE = "scrapy_masterglsdrscraper_%s.log" % (datetime.now())
        log.start(LOG_FILE)

    def spider_opened(self, spider):
        self.files = dict([(name, open('test_output_'+name.lower()+'.csv','a')) for name in self.SaveTypes])
        self.exporters = {}
        for name in self.SaveTypes:
            currExporter = CsvItemExporter(self.files[name])
            # define the ordering of the columns
            currExporter.fields_to_export = self.ordering[name]
            self.exporters[name] = currExporter
        print self.exporters
        [e.start_exporting() for e in self.exporters.values()]

    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):

        if isinstance(item, SalaryItem):
            self.exporters['SalaryItem'].export_item(item)
        elif isinstance(item, CompanyInfoItem):
            self.exporters['CompanyInfoItem'].export_item(item)
        elif isinstance(item, ReviewItem):
            self.exporters['ReviewItem'].export_item(item)
        elif isinstance(item, InterviewItem):
            self.exporters['InterviewItem'].export_item(item)
        elif isinstance(item, CompanyInfoItem):
            self.exporters['CompanyInfoItem'].export_item(item)
        elif isinstance(item, CompanyUrlsItem):
            self.exporters['CompanyUrlsItem'].export_item(item)
        return item

