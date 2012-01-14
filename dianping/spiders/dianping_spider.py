from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy import log
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from dianping.items import DianpingItem

import re


class DianpingSpider(CrawlSpider):
    name="dianping"
    allowed_domains=["dianping.com"]
    REVIEW_MAXROWS_PERPAGE = 20
    THRESHOLD_PAGES = 20
    log.start()
    
    start_urls=[
    "http://www.dianping.com/search/category/1/50/g157n1/g50g157",
         ]
    rules = (
    #next page info
        Rule(SgmlLinkExtractor(allow="/search/category/1/50/g157n1p\d*$"),
            'parse_info',
            follow=True,
        ),
    #branch info
        Rule(SgmlLinkExtractor(allow="/search/branch/1/[0-9_]+/g0$"),
                    'parse_info',
                    follow=True,
                ),
    #only fetch 2 review page at most   http://www.dianping.com/shop/5155229/review_more?pageno=
        Rule(SgmlLinkExtractor(allow="/shop/\d+/review_more\?pageno=2$"),
             'parse_reviews',
             follow=True,
             ),                       
    )

    def __init__(self, name=None, **kwargs):
        super(DianpingSpider, self).__init__(name, **kwargs)
        # Buffer to hold items during 2-steps scraping
        self.items_buffer = {}
        self.base_url = "http://www.dianping.com"

    def parse_info(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//dd[child::ul[@class='remark']]")

        for site in sites:
            item = DianpingItem()
            item['name'] = site.select("descendant::li[@class='shopname']/a/text()").extract()
            shoplink = site.select("descendant::li[@class='shopname']/a[1]/@href").extract()
            shoplink = shoplink[0]
            shopID = re.search("shopId=(\d+)#", shoplink).groups()[0]
          

            item['tag'] = site.select("descendant::li[@class='tags']/descendant::text()").extract()
            item['avgPrice'] = site.select("descendant::strong[@class='average']/text()").extract()
            item['stars'] = site.select("descendant::span[contains(@class,'item-rank-rst')]/@title").extract()
        
            self.items_buffer[shopID] = item
            log.msg("ken: yield link:%s"%self.base_url+shoplink)
            yield Request(url=self.base_url+shoplink, callback=self.parse_details)


    def parse_details(self, response):
        shopID = re.search("shopId=(\d+)#", response.request.url).groups()[0]
        hxs = HtmlXPathSelector(response)
        item['link'] = response.request.url
        
        #address
        address = hxs.select("//dl[@class='shopDeal-Info-address']/descendant::text()").extract()
        #contact
        contact = hxs.select("//div[@class='shop-info-inner Fix']/div[@class='desc-list']/dl[5]/dd/descendant::text()").extract()
        #details_info
        details_info = hxs.select("//div[contains(@class,'shop-detail-info')]/div[2]/descendant::text()").extract()
        
        item = self.items_buffer[shopID]
        item['address'] = address
        item['contact'] = contact
        item['details_info'] = details_info
        item['comments'] = []
        item['comments_count'] = 0
        reviewlink = hxs.select("//ul[@class='cmt-filter']/li[@class='first']/span/a/@href[1]").extract()
        log.msg("reviewlink type:%s"%type(reviewlink))
        if reviewlink:
            log.msg("ken: yield link to each reviews %s"%reviewlink[0])
            yield Request(url=self.base_url+reviewlink[0], callback=self.parse_reviews)
        else:
            log.msg("ken not one reviews, return")
            del self.items_buffer[shopID]
            yield item             
            
    def parse_reviews(self, response):
        #http://www.dianping.com/shop/5155229/review_more
        shopID = re.search("shop/(\d+)/", response.request.url).groups()[0]
        log.msg("ken in parse reviews, shopID:%s"%shopID)
        hxs = HtmlXPathSelector(response)
        reviews = hxs.select("//li[@class='comment-list-item']")  
        item = self.items_buffer[shopID] 
        review_contents = []   
        for review in reviews:
            content = review.select("descendant::text()").extract()
            review_contents.append(content)
        item['comments'].extend(review_contents)
        item['comments_count'] += len(review_contents)
        item['source'] = ['parse review']
        
        pagelinks = hxs.select("//div[@class='Pages']/a[@class='PageLink']/@href")
        if item['comments_count'] > DianpingSpider.THRESHOLD_PAGES:
            del self.items_buffer[shopID]
            yield item        
        elif len(pagelinks) >= 1:
            yield Request(url=self.base_url+"/shop/"+shopID+"/review_more?pageno=2", callback=self.parse_reviews)
        else:
            del self.items_buffer[shopID]
            yield item     
     
        log.msg("ken out of view withe link:%s"%response.request.url)
        log.msg("ken out of view withe item:%s"%item)
            
            
            
            