from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from dianping.items import DianpingItem

import re


class DianpingSpider(CrawlSpider):
    name="dianping"
    allowed_domains=["dianping.com"]
    REVIEW_MAXROWS_PERPAGE = 20
    
    start_urls=[
    "http://www.dianping.com/search/category/1/50/g157p1",
         ]

    rules = (
    #next page info
        Rule(SgmlLinkExtractor(allow="/search/category/1/50/g157p\d*$"),
            'parse_info',
            follow=True,
        ),
    #branch info
        Rule(SgmlLinkExtractor(allow="/search/branch/1/[0-9_]+/g0$"),
                    'parse_info',
                    follow=True,
                ),
    #next review page    http://www.dianping.com/shop/5192533/review_all?pageno=2
            Rule(SgmlLinkExtractor(allow="/shop/\d+/review_all\?pageno=\d+$"),
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
            shoplink = site.select("descendant::li[@class='shopname']/a/@href").extract()
            shoplink = shoplink[0]
            shopID = re.search("shopId=(\d+)#", shoplink).groups()[0]
          

            item['tag'] = site.select("descendant::li[@class='tags']/descendant::text()").extract()
            item['avgPrice'] = site.select("descendant::strong[@class='average']/text()").extract()
            item['stars'] = site.select("/descendant::span[contains(@class,'item-rank-rst')]/@title").extract()
        
            self.items_buffer[shopID] = item
            yield Request(url=self.base_url+shoplink, callback=self.parse_details)


    def parse_details(self, response):
        shopID = re.search("shopId=(\d+)#", response.request.url).groups()[0]
        hxs = HtmlXPathSelector(response)
        
        
        #address
        address = hxs.select("//dl[@class='shopDeal-Info-address']/descendant::text()").extract()
        #contact
        contact = hxs.select("//dl[@class='shop-info-contact']/descendant::text()").extract()
        #details_info
        details_info = hxs.select("//div[contains(@class,'shop-detail-info')]/div[2]/descendant::text()").extract()
        
        item = self.items_buffer[shopID]
        item['address'] = address
        item['contact'] = contact
        item['details_info'] = details_info
        item['comments'] = []
        
        reviewlink = hxs.select("//div[@id='ctl00_PlaceHolderPage_dpcAllReviewHint']/a/@href").extract()
        if reviewlink:
            reviewlink =re.search("([^#]+)",str(reviewlink)).groups()[0] #fetch all the review
            yield Request(url=self.base_url+reviewlink, callback=self.parse_reviews)
        else:
            del self.items_buffer[shopID]
            #todo  add left items in current page
            
            yield item             
            
    def parse_reviews(self, response):
        shopID = re.search("shop/(\d+)/", response.request.url).groups()[0]
        print "ken=========parse_reviews"
        print "shopiD:%s"%shopID
        hxs = HtmlXPathSelector(response)
        reviews = hxs.select("//li[@class='comment-list-item']")  
        item = self.items_buffer[shopID] 
        review_contents = []   
        for review in reviews:
            content = review.select("descendant::text()").extract()
            review_contents.append(content)
        item['comments'].extend(review_contents)
        if len(reviews) < REVIEW_MAXROWS_PERPAGE:
            del self.items_buffer[shopID]
            return item