# -*- coding: utf-8 -*-
import scrapy
from GameDataSpider.items import GamedataspiderItem
import re
from urllib.parse import urlparse

from GameDataSpider.sqlConn import connSql


class GamedataSpider(scrapy.Spider):
    name = '88aCrawler'

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
        for TR in response.xpath('//table[@class="tableBorder1"]/tbody/tr'):
            data = {
                "title": TR.xpath('td[1]/a/text()').extract_first(),
                "ip": TR.xpath('td[2]/a/text()').extract_first(),
                "opentime": TR.xpath('td[3]/text()').extract_first("").strip(),
                "line": TR.xpath('td[4]/text()').extract_first(),
                "introduce": TR.xpath('td[5]/text()').extract_first("").strip(),
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
