# -*- coding: utf-8 -*-
import scrapy
from GameDataSpider.items import GamedataspiderItem
import re
from urllib.parse import urlparse

class GamedataSpider(scrapy.Spider):
    name = 'sfbaoCrawler'

    def start_requests(self):
        start_urls = ['https://www.sfbao.org/local_iframe.html']
        for start in start_urls:
            yield scrapy.Request(start, callback=self.detail_page, dont_filter=True)

    def detail_page(self, response):
        item = GamedataspiderItem()
        dataItem = []
        for TR in re.findall(r'trad\[item_no\].*?=\s*?"[\s\S]*?";', response.text):
            data = {
                "title": re.findall(r'<a.*?>(.*?)</a', TR)[0],
                "ip": re.findall(r'<a.*?>(.*?)</a', TR)[1],
                "opentime": re.findall(r'<span.*?>(.*?)</span', TR)[0],
                "line": re.findall(r'<td >(.*?)</td>', TR)[0],
                "introduce": re.findall(r'<td style=.*?>(.*?)<span', TR)[0].strip('" +"'),
                "customer": re.findall(r'<td>(.*?)</td>', TR)[-1],
                "homepage": re.findall(r'<td class = \\"c7\\"><a.*?href=\\"(.*?)\\">点击查看', TR)[0]
            }
            dataItem.append(data)

        item["data"] = dataItem
        item["shortName"] = urlparse(response.url).hostname
        yield item
