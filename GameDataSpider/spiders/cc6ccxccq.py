# -*- coding: utf-8 -*-
import scrapy
from GameDataSpider.items import GamedataspiderItem
from urllib.parse import urlparse

class GamedataSpider(scrapy.Spider):
    name = 'cc6ccxccqCrawler'

    def start_requests(self):
        start_urls = ['https://cc6ccxccq.602520.com/']
        for start in start_urls:
            yield scrapy.Request(start, dont_filter=True, callback=self.detail_page)

    def detail_page(self, response):
        item = GamedataspiderItem()
        dataItem = []
        for TR in response.xpath('//div[@class="table"]/table/tr'):
            if TR.css("td"):
                data = {
                    "title": TR.xpath('td[1]/a/text()').extract_first(),
                    "ip": TR.xpath('td[2]/a/text()').extract_first(),
                    "opentime": TR.xpath('td[3]/text()').extract_first("").strip(),
                    "line": TR.xpath('td[4]/text()').extract_first(),
                    "introduce": TR.xpath('td[5]/text()').extract_first("").strip(),
                    "customer": TR.xpath('td[6]/text()').extract_first(),
                    "homepage": TR.xpath('td[7]/a/@href').extract_first(),
                }
                dataItem.append(data)

        item["data"] = dataItem
        item["shortName"] = urlparse(response.url).hostname
        yield item
