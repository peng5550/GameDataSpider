# -*- coding: utf-8 -*-
import scrapy
from GameDataSpider.items import GamedataspiderItem
import re
from urllib.parse import urlparse

class GamedataSpider(scrapy.Spider):
    name = 'haosfCrawler'

    def start_requests(self):
        start_urls = ['https://www.haosf.com/haosfjs2.htm']
        for start in start_urls:
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'referer': 'https://www.haosf.com/haosfjs2.htm',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
            }
            yield scrapy.Request(start, callback=self.detail_page, headers=headers, dont_filter=True)

    def detail_page(self, response):
        item = GamedataspiderItem()
        dataItem = []
        for TR in response.xpath('//dl'):
            data = {
                "title": TR.xpath('dd[1]/a/text()').extract_first(),
                "ip": TR.xpath('dd[2]/a/text()').extract_first(),
                "opentime": TR.xpath('dd[3]/text()').extract_first("").strip(),
                "line": TR.xpath('dd[4]/text()').extract_first(),
                "introduce": TR.xpath('dd[5]//text()').extract_first("").strip(),
                "customer": TR.xpath('dd[6]/text()').extract_first(),
                "homepage": TR.xpath('dt[1]/a/@href').extract_first()
            }
            dataItem.append(data)

        for TR in re.findall(r"theAds\[\d+\]\s*?=\s*?'[\s\S]*?';", response.text):
            data = {
                "title": re.findall(r'<dd class="mc">.*?href=.*?>(.*?)</a></dd><dd class="ip">', TR)[0],
                "ip": re.findall(r'<dd class="ip">.*?href=.*?>(.*?)</a></dd><dd class="sj">', TR)[0],
                "opentime": re.findall(r'<dd class="sj">(.*?)</dd><dd class="xl">', TR)[0],
                "line": re.findall(r'<dd class="xl">(.*?)</dd><dd class="js">', TR)[0],
                "introduce": re.findall(r'<dd class="js"><div.*?>(.*?)</dd><dd class="qq">', TR)[0],
                "customer": re.findall(r'<dd class="qq">(.*?)</dd><dt class="xx">', TR)[0],
                "homepage": re.findall(r'<dt class="xx"><a.*?href=(.*?)>点击查看<', TR)[0].strip()
            }
            dataItem.append(data)

        item["data"] = dataItem
        item["shortName"] = urlparse(response.url).hostname
        yield item
