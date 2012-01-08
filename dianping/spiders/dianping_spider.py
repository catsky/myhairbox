from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from dianping.items import DianpingItem

import re


class DmozSpider(CrawlSpider):
    name="dianping"
    allowed_domains=["dianping.com"]
    first_time = True
    start_urls=[
    "http://www.dianping.com/search/category/1/50/g157p1",
         ]
    #'http://www.dianping.com/search/category/1/50/g157p2'
    rules = (
    #next page info
        Rule(SgmlLinkExtractor(allow="/search/category/1/50/g157p\d*$"),
            'parse_info',
            follow=True,
        ),
    #branch info
        Rule(SgmlLinkExtractor(allow="/search/branch/1/[0-9_]+/g0$"),
                    'parse_branch',
                    follow=True,
                ),
    )

    def parse_info(self, response):
        #filename =response.url.split("/")[-2]
        #open(filename, 'wb').write(response.body)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//dd[child::ul[@class='remark']]")

        items = []
        for site in sites:
            item = DianpingItem()
            item['name'] = site.select("descendant::li[@class='shopname']/a/text()").extract()
            item['address'] = site.select("descendant::li[@class='address']/descendant::text()").extract()
            result = re.search("(\d{5,21})",str(item['address']))
            if result:
                item['telphone'] = result.groups()[0][1:]
            else:
                item['telphone'] = ""
                
            item['tag'] = site.select("descendant::li[@class='tags']/descendant::text()").extract()
            item['avgPrice'] = site.select("descendant::strong[@class='average']/text()").extract()
            item['commentAff'] = site.select("descendant::li[@class='grade']/span[@class='score1']/text()").extract()
            item['commentEnv'] = site.select("descendant::li[@class='grade']/span[@class='score2']/text()").extract()
            item['commentServ'] = site.select("descendant::li[@class='grade']/span[@class='score3']/text()").extract()

            items.append(item)
 
        return items
    def parse_branch(self, response):
            #filename =response.url.split("/")[-2]
            #open(filename, 'wb').write(response.body)
            hxs = HtmlXPathSelector(response)
            sites = hxs.select("//dd[child::ul[@class='remark']]")
    
            items = []
            for site in sites:
                item = DianpingItem()
                item['name'] = site.select("descendant::li[@class='shopname']/a/text()").extract()
                item['address'] = site.select("descendant::li[@class='address']/descendant::text()").extract()
                result = re.search("(\d{5,21})",str(item['address']))
                if result:
                    item['telphone'] = result.groups()[0][1:]
                else:
                    item['telphone'] = ""
                    
                item['tag'] = site.select("descendant::li[@class='tags']/descendant::text()").extract()
                item['avgPrice'] = site.select("descendant::strong[@class='average']/text()").extract()
                item['commentAff'] = ""
                item['commentEnv'] = ""
                item['commentServ'] = ""    
                items.append(item)
     
            return items
    
