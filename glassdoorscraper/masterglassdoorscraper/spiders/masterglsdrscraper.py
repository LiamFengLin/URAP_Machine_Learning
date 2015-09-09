from scrapy.contrib.spiders.init import InitSpider
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
from masterglassdoorscraper.items import ReviewItem, SalaryItem, CompanyInfoItem, CompanyUrlsItem, InterviewItem
from datetime import datetime, timedelta
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from datetime import datetime
import random
import time
import re
import pdb

class MasterGlsDrScraper(Spider):

    name = "masterglsdrscraper"
    allowed_domains = ["www.glassdoor.com"]
    # industry level url
    start_urls = ["http://www.glassdoor.com/Reviews/company-reviews.htm"]
    
    # note: change this following section if start_urls change. It is merely a breakdown of the url above, for the ease of parsing
    start_url_front_component = "http://www.glassdoor.com/Reviews/reviews-SRCH_IP"
    current_page_number = 1
    start_url_tail_component = ".htm"
    # this is the maximum page the url goes up to. Find it manually by trial-and-error to save trouble of coding   
    MAX_PAGE_NUNBER = 300
    

    SALARY_ITEM_FIELDS = [
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
        "company_name",
        "scrape_date",
        "scrape_time",
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

    # Jass' scraper
    def parse(self, response):

        time.sleep(random.random() * 1)

        sel = Selector(response)

        company_batch_info = sel.xpath('.//div[contains(@class, "companySearchResult")]')
        next_page_info = sel.xpath('.//div[contains(@class, "pagingControls")]/ul/li[@class="next"]')

        #recursive calls to get the next companies_page
        if (self.current_page_number < self.MAX_PAGE_NUNBER):
            main_page_url = self.__generate_next_page_url()             
            yield Request(main_page_url, callback=self.parse, errback=self.after_webpage_error)
        #if (next_page_info.xpath('a')):
            # main_page_url = form_valid_url(next_page_info.xpath('a/@href').extract()[0])
            # next_page_info = sel.xpath('.//div[contains(@class, "pagingControls")]/ul/li[@class="next"]')
            
        for company_info in company_batch_info:

            company_name_info = company_info.xpath('div[@class="companyData"]//h3[@class="tightTop"]//tt[@class="i-emp"]/text()')
            company_name = company_name_info.extract()[0] if company_name_info else "n/a"

            meta = {'company_name': company_name}
            
            salaries_url_info = company_info.xpath('div/div/a[contains(@href, "Salary")]/@href')
            if salaries_url_info:
                salaries_url = salaries_url_info.extract()[0]
                salaries_url = form_valid_url(salaries_url)
                time.sleep(random.random() * 1)
                yield Request(salaries_url, callback=self.parse_salaries_page, meta=meta, errback=self.after_webpage_error)
            else:
                salaries_url = "n/a"

            overview_url_info = company_info.xpath('div/div/a[contains(@href, "Overview")]/@href')
            if overview_url_info:
                overview_url = overview_url_info.extract()[0]
                overview_url = form_valid_url(overview_url)
                time.sleep(random.random() * 1)
                yield Request(overview_url, callback=self.parse_company_page, meta=meta, errback=self.after_webpage_error)
            else:
                overview_url = "n/a"
            
            reviews_url_info = company_info.xpath('div/div/a[contains(@href, "Reviews")]/@href')
            if reviews_url_info:
                reviews_url = reviews_url_info.extract()[0]
                reviews_url = form_valid_url(reviews_url)
                time.sleep(random.random() * 1)
                yield Request(reviews_url, callback=self.parse_reviews_page, meta=meta, errback=self.after_webpage_error)
            else:
                reviews_url = "n/a"
            
            interviews_url_info = company_info.xpath('div/div/a[contains(@href, "Interview")]/@href')
            if interviews_url_info:
                interviews_url = interviews_url_info.extract()[0] 
                interviews_url = form_valid_url(interviews_url)
                time.sleep(random.random() * 1)
                yield Request(interviews_url, callback=self.parse_interviews_page, meta=meta, errback=self.after_webpage_error)
            else:
                interviews_url = "n/a"
            
            meta = {'company_name': company_name, 'salaries_url': salaries_url, 'overview_url': overview_url, 
            'reviews_url': reviews_url, 'interviews_url': interviews_url}

            item = CompanyUrlsItem()
            yield self.__build_item(item, meta)

    # yijia's scraper
    def parse_company_page(self, response):

        sel = Selector(response)

        avg = sel.xpath('.//div[contains(@class, "ratingInfo")]/div[contains(@class, "ratingNum")]/text()').extract()[0].encode('utf-8') 
        review = sel.xpath('//div[contains(@class,"ratingInfo")]/div[@class="minor hideHH"]/tt/text()').extract()[0].encode('utf-8') 

        rec = sel.xpath('.//div[@id="EmpStats_Recommend"]').xpath('@data-value').extract()[0].encode('utf-8')
        appr_ceo = sel.xpath('//div[@id="EmpStats_Approve"]').xpath('@data-value').extract()[0].encode('utf-8')

        ceo = sel.xpath(".//div[@class='cell middle text']/div[@class='i-per']/text()")
        ceo_name = sel.xpath(".//div[@class='cell middle text']/div[@class='i-per']/text()").extract()[0].encode('utf-8') if ceo else "n/a"
        ceo_rate = sel.xpath('.//div[@class="minor"]/tt/text()').extract()[0].encode('utf-8')

        company_additional_info = sel.xpath('.//div[contains(@class, "infoWithPhoto")]/div[contains(@class, "empInfo")]')
        website_info = company_additional_info.xpath('strong[contains(text(), "Website")]')
        website = website_info.xpath('../span[@class="empData"]/text()').extract()[0] if website_info.xpath('../span[@class="empData"]/text()').extract() else "n/a"
            
        founded_info = company_additional_info.xpath('strong[contains(text(), "Founded")]')
        found = founded_info.xpath('../span[@class="empData"]/text()').extract()[0] if founded_info.xpath('../span[@class="empData"]/text()').extract() else "n/a"
        
        size_info = company_additional_info.xpath('strong[contains(text(), "Size")]')
        size = size_info.xpath('../span[@class="empData"]/text()').extract()[0] if size_info.xpath('../span[@class="empData"]/text()').extract() else "n/a"
        
        type_info = company_additional_info.xpath('strong/tt[contains(text(), "Type")]')
        ty = type_info.xpath('../../span[@class="empData"]/text()').extract()[0] if type_info.xpath('../../span[@class="empData"]/text()').extract() else "n/a"
        
        ticker_info = type_info.xpath('../../span[@class="empData"]/tt[@class="notranslate"]/text()')  
        ticker = ticker_info.extract()[0].encode('utf-8') if ticker_info else "n/a"
        
        revenue_info = company_additional_info.xpath('strong[contains(text(), "Revenue")]')  
        revenue = revenue_info.xpath('../span[@class="empData"]/text()').extract()[0] if revenue_info else "n/a"

        hq_info = company_additional_info.xpath('strong[contains(text(), "Headquarters")]')
        hq = hq_info.xpath('../span[@class="empData"]/text()').extract()[0] if hq_info.xpath('../span[@class="empData"]/text()').extract() else "n/a"

        industry_info = company_additional_info.xpath('strong[contains(text(), "Industry")]')
        industry = industry_info.xpath('../span[@class="empData"]/tt/text()').extract()[0] if industry_info.xpath('../span[@class="empData"]/tt/text()').extract() else "n/a"
        
        competitor_info = company_additional_info.xpath('strong[contains(text(), "Competitors")]')
        competitor = competitor_info.xpath('../span[@class="empData"]/text()').extract()[0] if competitor_info.xpath('../span[@class="empData"]/text()').extract() else "n/a"

        text_info = sel.xpath('.//p[contains(@id,"EmpDescription")]/tt/text()') 
        text = text_info.extract()[0].encode('utf-8') if text_info else "n/a"
        
        mission_info = sel.xpath('.//p[contains(@id,"EmpMission")]').xpath('.//tt').xpath('text()')
        if mission_info:
            mission = mission_info.extract()[0].encode('utf-8')
        else:
            mission = "n/a"
        item = CompanyInfoItem()
        meta = {'AverageRating': avg, 'ReviewsCNT': review, 'RecToFriend': rec, 'ApprCEO': appr_ceo, 'CEOName': ceo_name,     'CEORateCNT': ceo_rate, 'CompanyWebsite': website,
            'Size': size, 'Type': ty, 'Ticker': ticker, 'Revenue': revenue, 'HQ': hq, 'Founded': found, 'Industry': industry, 'Competitors': competitor, 'Text': text,
            'Mission': mission}
        meta.update(response.meta)
        yield self.__build_item(item, meta)
        
    def parse_salaries_page(self, response):

        time.sleep(random.random() * 1)

        sel = Selector(response)

        #basic company info; scraped only once for every page
        salaries_cnt_info = sel.xpath('.//div[contains(@class, "counts")]/tt/tt/text()')
        salaries_cnt = salaries_cnt_info.extract()[0] if salaries_cnt_info else "n/a"

        jobs_count_info = sel.xpath('.//div[contains(@class, "counts")]/span/tt/tt/text()')
        jobs_count = jobs_count_info.extract()[0] if jobs_count_info else "n/a"

        updated_info = sel.xpath('.//div[contains(@class, "lastUpdate")]/tt/tt/text()')
        updated = updated_info.extract()[0] if updated_info else "n/a"
 
        next_page_info = sel.xpath('.//div[contains(@class, "pagingControls")]/ul/li[@class="next"]')
        if (next_page_info.xpath('a')):
            salaries_page_url = form_valid_url(next_page_info.xpath('a/@href').extract()[0])
            next_page_info = sel.xpath('.//div[contains(@class, "pagingControls")]/ul/li[@class="next"]')
            next_page_meta = {}
            next_page_meta['salaries_page_url'] = salaries_page_url
            next_page_meta.update(response.meta)
            time.sleep(random.random() * 1)
            yield Request(salaries_page_url, callback=self.parse_salaries_page, meta=next_page_meta, errback=self.after_webpage_error)
        
        data_rows = sel.xpath('.//div[contains(@class, "salaryRow")]/div[contains(@class, "row")]')

        for row in data_rows:
            position_info = row.xpath('.//span[contains(@class, "i-occ")]/text()')
            position = position_info.extract()[0] if position_info else "n/a"
            
            position_url_info = row.xpath('div[contains(@class, "jobTitleCol")]/a/@href')
            position_url = form_valid_url(position_url_info.extract()[0]) if position_url_info else "n/a"

            pos_cnt_info = row.xpath('div[contains(@class, "jobTitleCol")]//span[contains(@class, "salaryCount")]/text()')
            pos_cnt = pos_cnt_info.extract()[0] if pos_cnt_info else "n/a"

            avg_sal_info = row.xpath('div[contains(@class, "meanPayCol")]/div/text()')
            avg_sal = avg_sal_info.extract()[0] if avg_sal_info else "n/a"

            salary_range_chart = row.xpath('.//div[contains(@class, "salaryRangeChart")]')
            if salary_range_chart.xpath('div[contains(@class, "rangeValues")]/div/text()'):
                low_sal = salary_range_chart.xpath('div[contains(@class, "rangeValues")]/div/text()').extract()[0]
                high_sal = salary_range_chart.xpath('div[contains(@class, "rangeValues")]/div/text()').extract()[1]
            else:
                low_sal = "n/a"
                high_sal = "n/a"

            meta = {"avg_sal": avg_sal, "low_sal": low_sal, "high_sal": high_sal,
            "position_url": position_url, "pos_cnt": pos_cnt, "position": position, "salaries_cnt": salaries_cnt, 
            "jobs_count": jobs_count, "salaries_page_url": response.url, "updated": updated}

            meta.update(response.meta)

            if position_url is not "n/a":
                valid_position_url = form_valid_url(position_url)
                if self.__is_other_category(valid_position_url):
                    time.sleep(random.random() * 1)
                    yield Request(valid_position_url, callback=self.parse_individual_intern_position_page, meta=meta, errback=self.after_webpage_error)
                else:
                    time.sleep(random.random() * 1)
                    yield Request(valid_position_url, callback=self.parse_individual_position_page, meta=meta, errback=self.after_webpage_error)
            else:
                meta["total_compensation"] = "n/a"
                meta["total_pay_low"] = "n/a"
                meta["total_pay_high"] = "n/a"
                meta["cash_bonuses_cnt"] = "n/a"
                meta["cash_bonuses_avg"] = "n/a"
                meta["cash_bonuses_low"] = "n/a"
                meta["cash_bonuses_high"] = "n/a"
                meta["stock_cnt"] = "n/a"
                meta["stock_avg"] = "n/a"
                meta["stock_low"] = "n/a"
                meta["stock_high"] = "n/a"
                meta["base_pay"] = "n/a"
                
                item = SalaryItem()
                yield self.__build_item(item, meta)


    def parse_individual_intern_position_page(self, response):
        sel = Selector(response)
        
        time.sleep(random.random() * 1)
        
        salary_chart_info = sel.xpath('.//div[contains(@class, "salaryChartModule")]/div[@class="row"]')
        
        total_compensation_info = salary_chart_info.xpath('.//div[contains(@class, "jobTitleCol")]//span[contains(@class, "i-cur")]/text()')
        total_compensation = total_compensation_info.extract()[0] if total_compensation_info else "n/a"

        salary_range_values = salary_chart_info.xpath('.//div[contains(@class, "salaryRangeChart")]/div[contains(@class, "rangeValue")]')
        if salary_range_values:
            total_pay_low = salary_range_values.xpath('div/text()').extract()[0]
            total_pay_high = salary_range_values.xpath('div/text()').extract()[1]
        else:
            total_pay_high = "n/a"
            total_pay_low = "n/a"
        
        cash_bonuses_cnt = "n/a"
        cash_bonuses_avg = "n/a"

        meta = {
            "total_compensation": "n/a",
            "total_pay_low": "n/a",
            "total_pay_high": "n/a",
            "cash_bonuses_cnt": "n/a",
            "cash_bonuses_avg": "n/a",
            "cash_bonuses_low": "n/a",
            "cash_bonuses_high": "n/a",
            "stock_cnt": "n/a",
            "stock_avg": "n/a",
            "stock_low": "n/a",
            "stock_high": "n/a",
            "base_pay": "n/a"
        }
        meta.update(response.meta)
        item = SalaryItem()
        yield self.__build_item(item, meta)

    def parse_individual_position_page(self, response):

        time.sleep(random.random() * 1)
        sel = Selector(response)

        salary_chart_info = sel.xpath('.//div[@id="SalaryOverviewWrapper"]')
        
        base_pay_info = salary_chart_info.xpath('.//div[contains(@class, "basePay")]//div[contains(@class, "dollarAmount")]/text()')
        base_pay = base_pay_info.extract()[0] if base_pay_info else "n/a"

        total_compensation_info = salary_chart_info.xpath('.//div[contains(@class, "totalComp")]//div[contains(@class, "dollarAmount")]/text()')
        total_compensation = total_compensation_info.extract()[0] if total_compensation_info else "n/a"

        salary_range_values = salary_chart_info.xpath('.//div[contains(@class, "salaryRangeChart")]/div[contains(@class, "rangeValue")]')
        if salary_range_values:
            total_pay_low = salary_range_values.xpath('div/text()').extract()[0]
            total_pay_high = salary_range_values.xpath('div/text()').extract()[1]
        else:
            total_pay_high = "n/a"
            total_pay_low = "n/a"

        other_pay_info = sel.xpath('.//div[contains(@class, "salaryJobChart")]/div[contains(@class,"chartBody")]//div[contains(@class, "row")]')
        cash_bonuses_cnt_info = other_pay_info.xpath('div[contains(text(), "Cash Bonus")]')
        if cash_bonuses_cnt_info:
            cash_bonuses_cnt = cash_bonuses_cnt_info.xpath('span[contains(@class, "minor")]/text()').extract()[0]    
            cash_bonuses_cnt = cash_bonuses_cnt.encode('UTF8')[1:-1]
            cash_bonuses_avg = cash_bonuses_cnt_info.xpath('../div[contains(@class, "colSalary")]/span/text()').extract()[0]
            cash_bonuses_low = cash_bonuses_cnt_info.xpath('../div[contains(@class, "colChart")]//div[contains(@class, "rangeValues")]/div/text()').extract()[0]
            cash_bonuses_high = cash_bonuses_cnt_info.xpath('../div[contains(@class, "colChart")]//div[contains(@class, "rangeValues")]/div/text()').extract()[1]
        else:
            cash_bonuses_cnt = 'n/a'
            cash_bonuses_avg = 'n/a'
            cash_bonuses_low = 'n/a'
            cash_bonuses_high = 'n/a'

        stock_cnt_info = other_pay_info.xpath('div[contains(text(), "Stock Bonus")]')
        if stock_cnt_info:
            stock_cnt = stock_cnt_info.xpath('span[contains(@class, "minor")]/text()').extract()[0]    
            stock_cnt = stock_cnt.encode('UTF8')[1:-1]
            stock_avg = stock_cnt_info.xpath('../div[contains(@class, "colSalary")]/span/text()').extract()[0]
            stock_low = stock_cnt_info.xpath('../div[contains(@class, "colChart")]//div[contains(@class, "rangeValues")]/div/text()').extract()[0]
            stock_high = stock_cnt_info.xpath('../div[contains(@class, "colChart")]//div[contains(@class, "rangeValues")]/div/text()').extract()[1]
        else:
            stock_cnt = 'n/a'
            stock_avg = 'n/a'
            stock_low = 'n/a'
            stock_high = 'n/a'
        
        meta = {
            "total_compensation": total_compensation,
            "total_pay_low": total_pay_low,
            "total_pay_high": total_pay_high,
            "cash_bonuses_cnt": cash_bonuses_cnt,
            "cash_bonuses_avg": cash_bonuses_avg,
            "cash_bonuses_low": cash_bonuses_low,
            "cash_bonuses_high": cash_bonuses_high,
            "stock_cnt": stock_cnt,
            "stock_avg": stock_avg,
            "stock_low": stock_low,
            "stock_high": stock_high,
            "base_pay": base_pay
        }

        meta.update(response.meta)
        item = SalaryItem()
        yield self.__build_item(item, meta)

    def parse_reviews_page(self, response):

        time.sleep(random.random() * 1.5)

        sel = Selector(response)

        info = ReviewItem()
        today = datetime.now()

        info["scrape_date"] = today.strftime('%m/%d/%Y')
        info["scrape_time"] = today.strftime('%I:%M %p')

        next_reviews_page_url = get_next_page_url_if_exists(sel)
        if next_reviews_page_url:
            yield Request(next_reviews_page_url, callback=self.parse_reviews_page, errback=self.after_webpage_error)
        
        if response.xpath('.//*[@id="EIHdrModule"]/div/div[3]/div[2]/p/text()'):
            info['company_name'] = response.xpath('//*[@id="EIHdrModule"]/div/div[3]/div[2]/p/text()').extract()[0]

        for sel in response.xpath('.//*[@id="EmployerReviews"]/ol/li'):
            info['reviewUrl'] = unicode(response.url)

            if sel.xpath('div/div[1]/div/time/tt'):
                info['reviewDate'] = sel.xpath('div/div[1]/div/time/tt/text()').extract()[0]
            else:
                info['reviewDate'] = unicode('')

            if sel.xpath('div/div[2]/div/div[2]/div/div[1]/span/span/span/@title'):
                info['rating'] = sel.xpath('div/div[2]/div/div[2]/div/div[1]/span/span/span/@title').extract()[0]
            else:
                info['rating'] = unicode('')

            if sel.xpath('div/div[2]/div/div[2]/h2/tt/a/span/text()'):
                info['title'] = sel.xpath('div/div[2]/div/div[2]/h2/tt/a/span/text()').extract()[0]
            else:
                info['title'] = unicode('')

            if sel.xpath('div/div[2]/div/div[2]/div/div[2]/div/span[1]/span[1]/text()'):
                info['currentFormer'] = sel.xpath('div/div[2]/div/div[2]/div/div[2]/div/span[1]/span[1]/text()').extract()[0]
            else:
                info['currentFormer'] = unicode('')

            if sel.xpath('div/div[2]/div/div[2]/div/div[2]/div/span[1]/span[1]/span/tt/text()'):
                info['position'] = sel.xpath('div/div[2]/div/div[2]/div/div[2]/div/span[1]/span[1]/span/tt/text()').extract()[0]
            else:
                info['position'] = unicode('')

            if sel.xpath('div/div[2]/div/div[2]/div/div[2]/div/span[1]/span[2]'):
                info['location'] = sel.xpath('div/div[2]/div/div[2]/div/div[2]/div/span[1]/span[2]/text()').extract()[0]
            else:
                info['location'] = unicode('')

            text = sel.xpath('div/div[3]/div/div[2]/p/text()').extract()[0]
            if sel.xpath('div/div[3]/div/div[2]/p/text()'):
                if not text.find('full') == -1:
                    info['fullPartTime'] = unicode('full')
                elif not text.find('part') == -1:
                    info['fullPartTime'] = unicode('part')
                else:
                    info['fullPartTime'] = unicode('')
            else:
                info['fullPartTime'] = unicode('')

            text = sel.xpath('div/div[3]/div/div[2]/p/text()').extract()[0]
            if sel.xpath('div/div[3]/div/div[2]/p/text()'):
                tenure = text[text.find("(")+1:text.find(")")]
                if not tenure == "":
                    info['tenure'] = unicode(tenure)
                else:
                    info['tenure'] = unicode('')
            else:
                info['tenure'] = unicode('')

            if sel.xpath('div/div[3]/div/div[2]/div/div[1]/div[1]/div[2]/p/text()'):
                info['pros'] = sel.xpath('div/div[3]/div/div[2]/div/div[1]/div[1]/div[2]/p/text()').extract()[0]
            else:
                info['pros'] = unicode('')

            if sel.xpath('div/div[3]/div/div[2]/div/div[1]/div[2]/div[2]/p/text()'):
                info['cons'] = sel.xpath('div/div[3]/div/div[2]/div/div[1]/div[2]/div[2]/p/text()').extract()[0]
            else:
                info['cons'] = unicode('')

            if sel.xpath('div/div[3]/div/div[2]/div/div[1]/div[3]/div[2]/p'):
                info['advice'] = sel.xpath('div/div[3]/div/div[2]/div/div[1]/div[3]/div[2]/p/text()').extract()[0]
            else:
                info['advice'] = unicode('')

            colorcheck = sel.xpath('div/div[3]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div')
            if colorcheck.xpath('i[contains(concat(" ", normalize-space(@class), " ")," green ")]'):
                info['sq1Color'] = unicode('green')
            elif colorcheck.xpath('i[contains(concat(" ", normalize-space(@class), " ")," yellow ")]'):
                info['sq1Color'] = unicode('yellow')
            elif colorcheck.xpath('i[contains(concat(" ", normalize-space(@class), " ")," red ")]'):
                info['sq1Color'] = unicode('red')
            else:
                info['sq1Color'] = unicode('')

            if sel.xpath('div/div[3]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div/span/text()'):
                info['sq1Txt'] = sel.xpath('div/div[3]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[1]/div/span/text()').extract()[0]
            else:
                info['sq1Txt'] = unicode('')
            
            colorcheck = sel.xpath('div/div[3]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div')
            if colorcheck.xpath('i[contains(concat(" ", normalize-space(@class), " ")," green ")]'):
                info['sq2Color'] = unicode('green')
            elif colorcheck.xpath('i[contains(concat(" ", normalize-space(@class), " ")," yellow ")]'):
                info['sq2Color'] = unicode('yellow')
            elif colorcheck.xpath('i[contains(concat(" ", normalize-space(@class), " ")," red ")]'):
                info['sq2Color'] = unicode('red')
            else:
                info['sq2Color'] = unicode('')

            if sel.xpath('div/div[3]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div/span/text()'):
                info['sq2Txt'] = sel.xpath('div/div[3]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/div/span/text()').extract()[0]
            else:
                info['sq2Txt'] = unicode('')

            colorcheck = sel.xpath('div/div[3]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[3]')
            if colorcheck.xpath('i[contains(concat(" ", normalize-space(@class), " ")," green ")]'):
                info['sq3Color'] = unicode('green')
            elif colorcheck.xpath('i[contains(concat(" ", normalize-space(@class), " ")," yellow ")]'):
                info['sq3Color'] = unicode('yellow')
            elif colorcheck.xpath('i[contains(concat(" ", normalize-space(@class), " ")," red ")]'):
                info['sq3Color'] = unicode('red')
            else:
                info['sq3Color'] = unicode('')

            if sel.xpath('div/div[3]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[3]/span/text()'):
                info['sq3Txt'] = sel.xpath('div/div[3]/div/div[2]/div/div[2]/div[1]/div[2]/div/div[3]/span/text()').extract()[0] + unicode(" CEO")
            else:
                info['sq3Txt'] = unicode('')

            yield info

    def parse_interviews_page(self, response):

        time.sleep(random.random() * 1.5)

        sel = Selector(response)

        today = datetime.now()
        info = InterviewItem()
        
        next_interviews_page_url = get_next_page_url_if_exists(sel)
        if next_interviews_page_url:
            yield Request(next_interviews_page_url, callback=self.parse_interviews_page, errback=self.after_webpage_error)

        info["scrape_date"] = today.strftime('%m/%d/%Y')
        info["scrape_time"] = today.strftime('%I:%M %p')

        if response.xpath('//*[@id="EIHdrModule"]/div[3]/div[2]/p/text()'):
            info["company"] = response.xpath('//*[@id="EIHdrModule"]/div[3]/div[2]/p/text()').extract()[0]
        else:
            info['company'] = unicode('')

        if response.xpath('//*[@id="MainCol"]/div[2]/header/div[1]/tt/text()'):
            info["updated"] = response.xpath('//*[@id="MainCol"]/div[2]/header/div[1]/tt/text()').extract()[0]
        else:
            info['updated'] = unicode('')

        if response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[3]/div/div/div[1]/div/text()'):
            info["interDif"] = response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[3]/div/div/div[1]/div/text()').extract()[0]
        else:
            info['interDif'] = unicode('')

        if response.xpath('//*[@id="AllStats"]/div[1]/div[1]/div/div/div[2]/div/div[2]/div[2]/tt/text()'):
            info["posInter"] = response.xpath('//*[@id="AllStats"]/div[1]/div[1]/div/div/div[2]/div/div[2]/div[2]/tt/text()').extract()[0] + '%'
        else:
            info['posInter'] = unicode('')

        if response.xpath('//*[@id="AllStats"]/div[1]/div[1]/div/div/div[2]/div/div[3]/div[2]/tt/text()'):
            info["neutInter"] = response.xpath('//*[@id="AllStats"]/div[1]/div[1]/div/div/div[2]/div/div[3]/div[2]/tt/text()').extract()[0] + '%'
        else:
            info['neutInter'] = unicode('')

        # interview count
        if sel.xpath('.//div[contains(@class, "empLinks")]//a[contains(@class, "interviews")]/span'):
            info["interviewsCnt"] = response.xpath('//div[contains(@class, "empLinks")]//a[contains(@class, "interviews")]/span/text()').extract()[0]
        else:
            info['interviewsCnt'] = unicode('')

        if response.xpath('//*[@id="AllStats"]/div[1]/div[1]/div/div/div[2]/div/div[4]/div[2]/tt/text()'):
            info["negInter"] = response.xpath('//*[@id="AllStats"]/div[1]/div[1]/div/div/div[2]/div/div[4]/div[2]/tt/text()').extract()[0] + '%'
        else:
            info['negInter'] = unicode('')

        if response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[2]/div[1]/label/text()'):
            info["getAnInt1Desc"] = response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[2]/div[1]/label/text()').extract()[0]
        else:
            info['getAnInt1Desc'] = unicode('')

        if response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[2]/div[2]/tt/text()'):
            info["getAnInt1Perc"] = response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[2]/div[2]/tt/text()').extract()[0] + '%'
        else:
            info['getAnInt1Perc'] = unicode('')

        if response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[3]/div[1]/label/text()'):
            info["getAnInt2Desc"] = response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[3]/div[1]/label/text()').extract()[0]
        else:
            info['getAnInt2Desc'] = unicode('')

        if response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[3]/div[2]/tt/text()'):
            info["getAnInt2Perc"] = response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[3]/div[2]/tt/text()').extract()[0] + '%'
        else:
            info['getAnInt2Perc'] = unicode('')

        if response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[4]/div[1]/label/text()'):
            info["getAnInt3Desc"] = response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[4]/div[1]/label/text()').extract()[0]
        else:
            info['getAnInt3Desc'] = unicode('')

        if response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[4]/div[2]/tt/text()'):
            info["getAnInt3Perc"] = response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[4]/div[2]/tt/text()').extract()[0] + '%'
        else:
            info['getAnInt3Perc'] = unicode('')

        if response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[6]/div[1]/label/text()'):
            info["getAnInt4Desc"] = response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[6]/div[1]/label/text()').extract()[0]
        else:
            info['getAnInt4Desc'] = unicode('')

        if response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[6]/div[2]/tt/text()'):
            info["getAnInt4Perc"] = response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[6]/div[2]/tt/text()').extract()[0] + '%'
        else:
            info['getAnInt4Perc'] = unicode('')

        if response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[7]/div[1]/label/text()'):
            info["getAnInt5Desc"] = response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[7]/div[1]/label/text()').extract()[0]
        else:
            info['getAnInt5Desc'] = unicode('')

        if response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[7]/div[2]/tt/text()'):
            info["getAnInt5Perc"] = response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[7]/div[2]/tt/text()').extract()[0] + '%'
        else:
            info['getAnInt5Perc'] = unicode('')

        if response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[8]/div[1]/label/text()'):
            info["getAnInt6Desc"] = response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[8]/div[1]/label/text()').extract()[0]
        else:
            info['getAnInt6Desc'] = unicode('')

        if response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[8]/div[2]/tt/text()'):
            info["getAnInt6Perc"] = response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[8]/div[2]/tt/text()').extract()[0] + '%'
        else:
            info['getAnInt6Perc'] = unicode('')

        if response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[9]/div[1]/label/text()'):
            info["getAnInt7Desc"] = response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[9]/div[1]/label/text()').extract()[0]
        else:
            info['getAnInt7Desc'] = unicode('')

        if response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[9]/div[2]/tt/text()'):
            info["getAnInt7Perc"] = response.xpath('/html/body/div[4]/div/div/div[1]/div/div[1]/div/div[2]/article/div[2]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[9]/div[2]/tt/text()').extract()[0] + '%'
        else:
            info['getAnInt7Perc'] = unicode('')
        
        for sel in response.xpath('//*[@id="EmployerInterviews"]/ol/li'):
            info['interviewUrl'] = unicode(response.url)

            if sel.xpath('div[1]/time/tt/text()'):
                info['reviewDate'] = sel.xpath('div[1]/time/tt/text()').extract()[0]
            else:
                info['reviewDate'] = unicode('')

            if sel.xpath('div[2]/div/div[2]/h2/tt/a/span/text()'):
                info['position'] = sel.xpath('div[2]/div/div[2]/h2/tt/a/span/text()').extract()[0]
            else:
                info['position'] = unicode('')

            if sel.xpath('div[3]/div/div[2]/div[1]/div/div[1]/div[2]/p/span/tt/text()'):
                info['location'] = sel.xpath('div[3]/div/div[2]/div[1]/div/div[1]/div[2]/p/span/tt/text()').extract()[0]
            else:
                info['location'] = unicode('')

            if sel.xpath('div[3]/div/div[2]/div[1]/div/div[1]/div[2]/p/span/tt[2]/text()'):
                info['dateInterview'] = sel.xpath('div[3]/div/div[2]/div[1]/div/div[1]/div[2]/p/span/tt[2]/text()').extract()[0]
            else:
                info['dateInterview'] = unicode('')

            if sel.xpath('div[3]/div/div[2]/div[1]/div/div[1]/div[2]/p/text()'):
                info['appDetails'] = sel.xpath('div[3]/div/div[2]/div[1]/div/div[1]/div[2]/p/text()').extract()[0]
                if sel.xpath('div[3]/div/div[2]/div[1]/div/div[1]/div[2]/p/tt/text()'):
                    info['appDetails'] += sel.xpath('div[3]/div/div[2]/div[1]/div/div[1]/div[2]/p/tt/text()').extract()[0]
            else:
                info['appDetails'] = unicode('')

            if sel.xpath('div[3]/div/div[2]/div[1]/div/div[2]/div[2]/p/text()'):
                info['interDetails'] = sel.xpath('div[3]/div/div[2]/div[1]/div/div[2]/div[2]/p/text()').extract()[0]
            else:
                info['interDetails'] = unicode('')

            if sel.xpath('div[3]/div/div[2]/div[1]/div/div[3]/div[2]/ul/li/tt/text()'):
                info['interQuestions'] = sel.xpath('div[3]/div/div[2]/div[1]/div/div[3]/div[2]/ul/li/tt/text()').extract()[0]
            else:
                info['interQuestions'] = unicode('')

            if sel.xpath('div[3]/div/div[2]/div[1]/div/div[4]/div[2]/text()'):
                info['negotDetails'] = sel.xpath('div[3]/div/div[2]/div[1]/div/div[4]/div[2]/text()').extract()[0]
            else:
                info['negotDetails'] = unicode('')

            colorcheck = sel.xpath('div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]/div')
            if colorcheck:
                if colorcheck.xpath('i[contains(concat(" ", normalize-space(@class), " ")," green ")]'):
                    info['sq1Color'] = unicode('green')
                elif colorcheck.xpath('i[contains(concat(" ", normalize-space(@class), " ")," yellow ")]'):
                    info['sq1Color'] = unicode('yellow')
                elif colorcheck.xpath('i[contains(concat(" ", normalize-space(@class), " ")," red ")]'):
                    info['sq1Color'] = unicode('red')
                else:
                    info['sq1Color'] = unicode('')

            if sel.xpath('div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/span/tt/text()'):
                info['sq1Txt'] = sel.xpath('div[3]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/span/tt/text()').extract()[0]
            else:
                info['sq1Txt'] = unicode('')
            
            colorCheck = sel.xpath('div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div')
            if colorcheck:
                if colorcheck.xpath('i[contains(concat(" ", normalize-space(@class), " ")," green ")]'):
                    info['sq2Color'] = unicode('green')
                elif colorcheck.xpath('i[contains(concat(" ", normalize-space(@class), " ")," yellow ")]'):
                    info['sq2Color'] = unicode('yellow')
                elif colorcheck.xpath('i[contains(concat(" ", normalize-space(@class), " ")," red ")]'):
                    info['sq2Color'] = unicode('red')
                else:
                    info['sq2Color'] = unicode('')
            
            if sel.xpath('div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div/span/tt/text()'):
                info['sq2Txt'] = sel.xpath('div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div/span/tt/text()').extract()[0]
            else:
                info['sq2Txt'] = unicode('')

            colorCheck = sel.xpath('div[3]/div/div[2]/div[2]/div/div[2]/div/div[3]/div')
            if colorcheck:
                if colorcheck.xpath('i[contains(concat(" ", normalize-space(@class), " ")," green ")]'):
                    info['sq3Color'] = unicode('green')
                elif colorcheck.xpath('i[contains(concat(" ", normalize-space(@class), " ")," yellow ")]'):
                    info['sq3Color'] = unicode('yellow')
                elif colorcheck.xpath('i[contains(concat(" ", normalize-space(@class), " ")," red ")]'):
                    info['sq3Color'] = unicode('red')
                else:
                    info['sq3Color'] = unicode('')

            if sel.xpath('div[3]/div/div[2]/div[2]/div/div[2]/div/div[3]/div/span/tt/text()'):
                info['sq3Txt'] = sel.xpath('div[3]/div/div[2]/div[2]/div/div[2]/div/div[3]/div/span/tt/text()').extract()[0]
            else:
                info['sq3Txt'] = unicode('')

            if sel.xpath('div[3]/div/div[2]/div[3]/div/div[2]/div/div[1]/span/button/span/span/span/text()'):
                info['numberHelpful'] = sel.xpath('div[3]/div/div[2]/div[3]/div/div[2]/div/div[1]/span/button/span/span/span/text()').extract()[0]
            else:
                info['numberHelpful'] = unicode('')

            yield info

    def after_webpage_error(self, response):
        if (self.current_page_number < self.MAX_PAGE_NUNBER):
            main_page_url = self.__generate_next_page_url()             
            yield Request(main_page_url, callback=self.parse, errback=self.after_webpage_error)

    def __build_item(self, item, meta):

        today = datetime.now()
        item["scrape_date"] = today.strftime('%m/%d/%Y')
        item["scrape_time"] = today.strftime('%I:%M %p')

        if isinstance(item, SalaryItem):
            for field in self.SALARY_ITEM_FIELDS:
                if "xxx" in meta[field]:
                    meta[field] = "n/a"
                item[field] = meta[field]
        elif isinstance(item, CompanyInfoItem):
            for field in self.COMPANY_INFO_ITEM_FIELDS:
                item[field] = meta[field]
        elif isinstance(item, CompanyUrlsItem):
            for field in self.COMPANY_URLS_ITEM_FIELDS:
                item[field] = meta[field]
        return item

    def __generate_next_page_url(self):
        self.current_page_number += 1
        return self.start_url_front_component + str(self.current_page_number) + self.start_url_tail_component

    def __is_other_category(self, position_page_url):
        return ("Internship-Salary" in position_page_url) or ("Contractor-Salary" in position_page_url)

def form_valid_url(url_posfix):
    if "http://" in url_posfix:
        return url_posfix
    return "http://" + "www.glassdoor.com" + url_posfix
            
def get_next_page_url_if_exists(sel):
    next_page_info = sel.xpath('.//div[contains(@class, "pagingControls")]/ul/li[@class="next"]')
    if (next_page_info.xpath('a')):
        return form_valid_url(next_page_info.xpath('a/@href').extract()[0])
    else:
        return False
