# -*- coding: utf-8 -*-

# Scrapy settings for masterglassdoorscraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'masterglassdoorscraper'

SPIDER_MODULES = ['masterglassdoorscraper.spiders']
NEWSPIDER_MODULE = 'masterglassdoorscraper.spiders'

ITEM_PIPELINES = {
	'masterglassdoorscraper.pipelines.MultiCSVItemPipeline': 1,
	'masterglassdoorscraper.pipelines.MasterglassdoorscraperPipeline': 1
}

LOG_LEVEL = "DEBUG"

DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'masterglassdoorscraper (+http://www.yourdomain.com)'
