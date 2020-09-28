# -*- coding: utf-8 -*-
import scrapy
from GameDataSpider.items import GamedataspiderItem
import re
from urllib.parse import urlparse

class GamedataSpider(scrapy.Spider):
    name = 'zhaohfCrawler'

    def start_requests(self):
        start_urls = ['https://c.zhaohf.com/web.html']
        for start in start_urls:
            yield scrapy.Request(start, callback=self.detail_page)

    def detail_page(self, response):
        item = GamedataspiderItem()
        dataItem = []
        for TR in response.xpath('//div[@class="wrap"]/dl'):
            data = {
                "title": TR.xpath('dd[1]/a/text()').extract_first(),
                "ip": TR.xpath('dd[2]/a/text()').extract_first(),
                "opentime": TR.xpath('dd[3]//text()').extract_first("").strip(),
                "line": TR.xpath('dd[4]/span/text()').extract_first(),
                "introduce": TR.xpath('dd[5]/span/text()').extract_first("").strip(),
                "customer": TR.xpath('dd[6]/span/text()').extract_first(),
                "homepage": TR.xpath('dd[7]/a/@href').extract_first()
            }
            dataItem.append(data)

        for TR in re.findall(r"theAds\[\d+\]\s*?=\s*?'[\s\S]*?';", response.text):
            data = {
                "title": re.findall(r'<dd class=\\"c1\\"><a.*?>(.*?)<', TR)[0],
                "ip": re.findall(r'<dd class=\\"c2\\"><a.*?>(.*?)<', TR)[0],
                "opentime": re.findall(r'<dd class=\\"c3\\"><span><font.*?>(.*?)<', TR)[0],
                "line": re.findall(r'<dd class=\\"c4\\"><span>(.*?)<', TR)[0],
                "introduce": re.findall(r'<dd class=\\"c5\\"><span>(.*?)<', TR)[0],
                "customer": re.findall(r'<dd class=\\"c6\\"><span>(.*?)<', TR)[0],
                "homepage": re.findall(r'<dd class=\\"c7\\"><a href=\\"(.*?)\\"', TR)[0]
            }
            dataItem.append(data)

        item["data"] = dataItem
        item["shortName"] = urlparse(response.url).hostname
        yield item
