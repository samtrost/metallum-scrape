# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MetallumItem(scrapy.Item):
	name = scrapy.Field()
	country = scrapy.Field()
	city = scrapy.Field()
	status = scrapy.Field()
	formed = scrapy.Field()
	active_yrs = scrapy.Field()
	genre = scrapy.Field()
	lyr_themes = scrapy.Field()
	demo_ls = scrapy.Field()
	album_ls = scrapy.Field()

