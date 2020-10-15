# -*- coding: utf-8 -*-
import scrapy
from GameDataSpider.items import GamedataspiderItem
import re
from urllib.parse import urlparse

from GameDataSpider.sqlConn import connSql


class GamedataSpider(scrapy.Spider):
    name = 'laomirCrawler'

    def __init__(self):
        super(GamedataSpider, self).__init__()
        self.sql = connSql()

    def start_requests(self):
        item_info = {"shortName": self.name.replace("Crawler", "")}
        sqlres = self.sql.select_data(item_info=item_info)
        start_urls = sqlres[0].split("||")
        if sqlres[1]:
            oth_urls = sqlres[1].split("||")
        else:
            oth_urls = []
        for start in start_urls:
            yield scrapy.Request(start, dont_filter=True, meta={"othLink": oth_urls}, callback=self.detail_page)

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
