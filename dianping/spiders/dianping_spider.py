from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from dianping.items import DianpingItem

class DmozSpider(CrawlSpider):
    name="dianping"
    allowed_domains=["dianping.com"]
    first_time = True
    start_urls=[
    "http://www.dianping.com/search/category/1/50/g157p1",
         ]
    #'http://www.dianping.com/search/category/1/50/g157p2'
    rules = (   
        Rule(SgmlLinkExtractor(allow="/search/category/1/50/g157p\d*$"),
            'parse_info',
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
 #           item['telphone'] = site.select("descendant::li[@class='shopname']/a/text()").extract()
            item['tag'] = site.select("descendant::li[@class='tags']/descendant::text()").extract()
            item['avgPrice'] = site.select("descendant::strong[@class='average']/text()").extract()
            item['commentAff'] = site.select("descendant::li[@class='grade']/span[@class='score1']/text()").extract()
            item['commentEnv'] = site.select("descendant::li[@class='grade']/span[@class='score2']/text()").extract()
            item['commentServ'] = site.select("descendant::li[@class='grade']/span[@class='score3']/text()").extract()

            items.append(item)
 #       if  first_time == True:
 #           first_time = False
 #           yield Request(url="http://www.dianping.com/search/category/1/50/g15", callback=self.parse)
        return items
