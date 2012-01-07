from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from dianping.items import DianpingItem

class DmozSpider(BaseSpider):
    name="dianping"
    allowed_domains=["dianping.com"]
    start_urls=[
    "http://www.dianping.com/search/category/1/50/g157",
         ]

    def parse(self, response):
        #filename =response.url.split("/")[-2]
        #open(filename, 'wb').write(response.body)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//li[@class='shopname']/a[@class='BL']")
        //li[@class='address']/strong
        //li[@class='address']d
        items = []
        for site in sites:
            item = DianpingItem()
            item['name'] = site.select('text()').extract()
            items.append(item)
        return items

