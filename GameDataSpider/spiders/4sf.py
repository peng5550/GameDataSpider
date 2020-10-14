# -*- coding: utf-8 -*-
import scrapy
from GameDataSpider.items import GamedataspiderItem
from urllib.parse import urlparse

class GamedataSpider(scrapy.Spider):
    name = '4sfCrawler'

    def start_requests(self):
        start_urls = ['https://4sf.4sf.2000kai.com/']
        for start in start_urls:
            yield scrapy.Request(start, dont_filter=True, callback=self.detail_page)

    def detail_page(self, response):
        item = GamedataspiderItem()
        dataItem = []
        for TR in response.xpath('//*[@id="list"]/div[@class="table"]/table/tr'):
            if TR.css("td"):
                data = {
                    "title": TR.xpath('td[1]/@title').extract_first(),
                    "ip": TR.xpath('td[2]/@title').extract_first(),
                    "opentime": TR.xpath('td[3]/@title').extract_first(),
                    "line": TR.xpath('td[4]/@title').extract_first(),
                    "introduce": TR.xpath('td[5]/@title').extract_first(),
                    "customer": TR.xpath('td[6]/@title').extract_first(),
                    "homepage": TR.xpath('td[7]/@title').extract_first()
                }
                dataItem.append(data)

        item["data"] = dataItem
        item["shortName"] = urlparse(response.url).hostname
        yield item
