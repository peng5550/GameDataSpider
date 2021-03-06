# -*- coding: utf-8 -*-
import scrapy
from GameDataSpider.items import GamedataspiderItem
import re
from urllib.parse import urlparse

from GameDataSpider.sqlConn import connSql


class GamedataSpider(scrapy.Spider):
    name = '92fCrawler'

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
        for TR in response.xpath('//div[@class="statistics"]/table/tbody/tr'):
            data = {
                "title": TR.xpath('td[1]/a/text()').extract_first(),
                "ip": TR.xpath('td[2]/a/text()').extract_first(),
                "opentime": TR.xpath('td[3]//text()').extract_first("").strip(),
                "line": TR.xpath('td[4]//text()').extract_first(),
                "introduce": TR.xpath('td[5]//text()').extract_first("").strip(),
                "customer": TR.xpath('td[6]//text()').extract_first(),
                "homepage": TR.xpath('td[7]/a/@href').extract_first()
            }
            dataItem.append(data)

        for TR in re.findall(r"\[\d+\]\s*?=\s*?'[\s\S]*?';", response.text):
            data = {
                "title": re.findall(r'<td style="width:13\.6%;"><a.*?>(.*?)</a', TR, re.M)[0],
                "ip": re.findall(r'<td style="width:13\.4%;"><a.*?>(.*?)</a', TR, re.M)[0],
                "opentime": re.findall(r'class="c-red-cur"><a.*?>(.*?)</a', TR, re.M)[0],
                "line": re.findall(r'style="width:9\.4%;"><a.*?>(.*?)</a', TR, re.M)[0],
                "introduce": re.findall(r'<td style="width:32\.85%;"><a.*?>(.*?)</a', TR, re.M)[0],
                "customer": re.findall(r'<td style="width:8\.8%;"><a.*?>(.*?)</a', TR, re.M)[0],
                "homepage": re.findall(r'<td><a href=(.*?) .*?>点击查看</a>', TR, re.M)[0]
            }
            dataItem.append(data)

        item["data"] = dataItem
        item["shortName"] = urlparse(response.url).hostname
        yield item
