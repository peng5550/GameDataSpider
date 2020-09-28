# -*- coding: utf-8 -*-
import scrapy
from GameDataSpider.items import GamedataspiderItem
import re
from urllib.parse import urlparse


class GamedataSpider(scrapy.Spider):
    name = 'jjjCrawler'

    def start_requests(self):
        start_urls = ['http://www.jjj.com/', 'http://www.99s.com/', 'http://www.9ss.com/']
        for start in start_urls:
            yield scrapy.Request(start, callback=self.detail_page)

    def detail_page(self, response):
        item = GamedataspiderItem()
        dataItem = []
        for data in re.findall(r"<script>.*?(\(.*?\));</script>", response.text):
            dataList = re.findall(r'"(.*?)"', data)
            data = {
                    "title": dataList[0],
                    "ip": dataList[2],
                    "opentime": dataList[3],
                    "line": dataList[4],
                    "introduce": dataList[5],
                    "customer": dataList[6],
                    "homepage": dataList[1],
            }
            dataItem.append(data)

        item["data"] = dataItem
        item["shortName"] = urlparse(response.url).hostname
        yield item
