# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


class DianpingItem(Item):
    # define the fields for your item here like:
    # name = Field()
    name = Field()

    tag = Field()
    avgPrice = Field()
    stars = Field()


    address = Field()
    contact = Field()
    alias = Field()
    details_info = Field()
    recommand_dressor = Field()
    service_time = Field()
    bus_info = Field()
    price_info = Field()
    comments = Field()
