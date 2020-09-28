# -*- coding: utf-8 -*-
import scrapy
from GameDataSpider.items import GamedataspiderItem
import re
from urllib.parse import urlparse

class GamedataSpider(scrapy.Spider):
    name = '9qkCrawler'

    def start_requests(self):
        start_urls = ['https://9pk.5566rs.com/', 'http://9pk.5566rs.com/index2.html']
        for start in start_urls:
            yield scrapy.Request(start, callback=self.detail_page)

    def detail_page(self, response):
        item = GamedataspiderItem()
        dataItem = []
        for index, TABLE in enumerate(response.xpath('//table[@class="tableBorder1"]/tbody')):
            if index not in [6]:
                for TR in TABLE.xpath('//tr'):
                    data = {
                        "title": TR.xpath('td[1]/a/text()').extract_first(),
                        "ip": TR.xpath('td[2]/a/text()').extract_first(),
                        "opentime": TR.xpath('td[3]/text()').extract_first("").strip(),
                        "line": TR.xpath('td[4]/text()').extract_first(),
                        "introduce": TR.xpath('td[5]/text()').extract_first(),
                        "customer": TR.xpath('td[6]/text()').extract_first(),
                        "homepage": TR.xpath('td[7]/a/@href').extract_first()
                    }
                    dataItem.append(data)

        for TR in re.findall(r'strItem\s*?=\s*?"[\s\S]*?";', response.text):
            data = {
                "title": re.findall(r'<td><a .*?>(.*?)<', TR)[0],
                "ip": re.findall(r'<td><a .*?>(.*?)<', TR)[1],
                "opentime": re.sub(r"<span.*?>|</span>", "", re.findall(r"<td class='time.*?>(.*?)</td", TR)[0]),
                "line": re.findall(r"<td>(.{1,50})</td><td class='tl'>", TR)[0],
                "introduce": re.findall(r"<td class='tl'>(.*?)<span", TR)[0],
                "customer": re.findall(r"<td>(.*?)</td>", TR)[3],
                "homepage": re.findall(r"<td><a href='(.*?)'.*?class='rk'>", TR)[0]
            }
            dataItem.append(data)

        item["data"] = dataItem
        item["shortName"] = urlparse(response.url).hostname
        yield item