# -*- coding: utf-8 -*-
import scrapy
from GameDataSpider.items import GamedataspiderItem
import re
from urllib.parse import urlparse

class GamedataSpider(scrapy.Spider):
    name = 'kusfCrawler'

    def start_requests(self):
        start_urls = ["http://www.kusf.com/", "http://www.300sf.com/", "http://www.88845.com/"]
        for start in start_urls:
            yield scrapy.Request(start, callback=self.detail_page)

    def detail_page(self, response):
        item = GamedataspiderItem()
        dataItem = []
        for TR in response.xpath('//div[@class="content"]/table/tbody/tr'):
            if TR.css("td"):
                data = {
                    "title": TR.xpath('td[1]/a/text()').extract_first(),
                    "ip": TR.xpath('td[2]/a/text()').extract_first(),
                    "opentime": TR.xpath('td[3]//text()').extract_first("").strip(),
                    "line": TR.xpath('td[4]/text()').extract_first(),
                    "introduce": TR.xpath('td[5]/text()').extract_first("").strip(),
                    "customer": TR.xpath('td[6]/text()').extract_first(),
                    "homepage": TR.xpath('td[7]/a/@href').extract_first()
                }
                dataItem.append(data)

        for TR in re.findall(r"theAds\[\d+\]\s*?=\s*?'[\s\S]*?';", response.text):
            data = {
                "title": re.findall(r'<TD width=13%>\s*?<a.*?>(.*?)<', TR, re.M)[0],
                "ip": re.findall(r'<TD width=13%>\s*?<a.*?>(.*?)<', TR, re.M)[1],
                "opentime": re.findall(r'<TD.*?class=font_R.*?>(.*?)<', TR, re.M)[0],
                "line": re.findall(r'<TD.*?width=10%.*?>(.*?)<', TR, re.M)[0],
                "introduce": re.findall(r'</TD><TD>(.*?)-<font', TR, re.M)[0],
                "customer": re.findall(r'<TD.*?width=10%.*?>(.*?)<', TR, re.M)[1],
                "homepage": re.findall(r'<TD.*?width=8%.*?><a href=(.*?)target=', TR, re.M)[0]
            }
            dataItem.append(data)

        for datas in re.findall(r'<script>o4\((.*?)\);</script>', response.text, re.M):
            dataList = re.findall(r'"(.*?)"', datas)
            data = {
                "title": dataList[4],
                "ip": dataList[-6],
                "opentime": dataList[-5],
                "line": dataList[-4],
                "introduce": dataList[-3],
                "customer": dataList[-2],
                "homepage": dataList[-1]
            }
            dataItem.append(data)

        item["data"] = dataItem
        item["shortName"] = urlparse(response.url).hostname
        yield item