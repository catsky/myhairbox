# Scrapy settings for dianping project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'dianping'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['dianping.spiders']
NEWSPIDER_MODULE = 'dianping.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

