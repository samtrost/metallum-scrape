from metallum.items import MetallumItem
from scrapy import Spider
from scrapy.http.request import Request

import numpy as np
import pandas as pd

class MetalSpider(Spider):
	name = 'metal_spider'
	allowed_urls = ['https://www.metal-archives.com/']

	def __init__(self, fn='bandsfin.csv'):
		if fn:
			bands = pd.read_csv(fn, skipinitialspace = True ,quotechar='"')
		self.start_urls = [str("https://www.metal-archives.com/bands/") + str(row['name']) + "/" + str(row['ID']) for index, row in bands.iterrows()]

	def parse(self, response):
		name = response.xpath('//div[@id="band_info"]/h1/a/text()').extract_first()
		country = response.xpath('//div[@id="band_stats"]/dl/dd/a/text()').extract_first()
		city = response.xpath('//div[@id="band_stats"]/dl/dd[2]/text()').extract_first()
		status = response.xpath('//div[@id="band_stats"]/dl/dd[3]/text()').extract_first()
		formed = response.xpath('//div[@id="band_stats"]/dl/dd[4]/text()').extract_first()
		genre = response.xpath('//div[@id="band_stats"]/dl[2]/dd/text()').extract_first()
		lyr_themes = response.xpath('//div[@id="band_stats"]/dl[2]/dd[2]/text()').extract_first()
		active_yrs =  response.xpath('//div[@id="band_stats"]/dl[3]/dd/text()').extract_first().strip()
		album_link =  response.xpath('//div[@id="band_disco"]/ul/li[2]/a/@href').extract_first()
		demo_link =  response.xpath('//div[@id="band_disco"]/ul/li[4]/a/@href').extract_first()

		item = MetallumItem()
		item['name'] = name
		item['country'] = country
		item['city'] = city
		item['status'] = status
		item['formed'] = formed
		item['genre'] = genre
		item['lyr_themes'] = lyr_themes
		item['active_yrs'] = active_yrs

		yield Request(album_link, callback = self.parse_albums,
			meta={'item': item, 'demo_link': demo_link})

	def parse_albums(self, response):

		demo_link = response.meta['demo_link']
		item = response.meta['item']
		albums = response.xpath('//tbody/tr')

		album_ls = []

		for album in albums:
			main_album = {}
			a_name = album.xpath('./td/a/text()').extract_first()
			a_year = album.xpath('./td[3]/text()').extract_first()
			#a_reviews = album.xpath('./td[4]/a/text()').extract_first()
			main_album['name'] = a_name
			main_album['year'] = a_year
			#main_album['reviews'] = a_reviews
			album_ls.append(main_album)

		item['album_ls'] = album_ls

		yield Request(demo_link, callback = self.parse_demos,
			meta={'item': item})

	def parse_demos(self, response):

		demos = response.xpath('//tbody/tr')
		item = response.meta['item']

		demo_ls = []

		for demo in demos:
			demo_album = {}
			d_name = demo.xpath('./td/a/text()').extract_first()
			d_year = demo.xpath('./td[3]/text()').extract_first()
			#d_reviews = demo.xpath('./td[4]/a/text()').extract_first()
			demo_album['name'] = d_name
			demo_album['year'] = d_year
			#demo_album['reviews'] = d_reviews
			demo_ls.append(demo_album)

		item['demo_ls'] = demo_ls

		yield item

