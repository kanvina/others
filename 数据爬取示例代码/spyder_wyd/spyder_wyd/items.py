# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Item_wyd(scrapy.Item):
    # define the fields for your item here like:
    building_area_name = scrapy.Field()
    price=scrapy.Field()

    # time=scrapy.Field()
    # plot_ratio=scrapy.Field()
    # greening_rate=scrapy.Field()
    # address = scrapy.Field()
    pass
