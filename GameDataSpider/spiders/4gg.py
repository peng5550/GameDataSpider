# -*- coding: utf-8 -*-
import scrapy
from GameDataSpider.items import GamedataspiderItem
from urllib.parse import urlparse

class GamedataSpider(scrapy.Spider):
    name = '4ggCrawler'

    def start_requests(self):
        start_urls = ['https://4gg.4gg.4gg.7000kai.com/']
        for start in start_urls:
            yield scrapy.Request(start, callback=self.detail_page)

    def detail_page(self, response):
        item = GamedataspiderItem()
        dataItem = []
        for TR in response.xpath('//*[@id="main"]/div[@class="table"]/table/tr'):
            if TR.css("td"):
                data = {
                    "title": TR.xpath('td[1]/a/text()').extract_first("").strip(),
                    "ip": TR.xpath('td[2]/a/text()').extract_first("").strip(),
                    "opentime": TR.xpath('td[3]/text()').extract_first("").strip(),
                    "line": None,
                    "introduce": TR.xpath('td[4]/@title').extract_first(),
                    "customer": None,
                    "homepage": TR.xpath('td[5]/a/@href').extract_first()
                }
                dataItem.append(data)

        item["data"] = dataItem
        item["shortName"] = urlparse(response.url).hostname
        yield item
