# -*- coding: utf-8 -*-
import scrapy
from GameDataSpider.items import GamedataspiderItem
from urllib.parse import urlparse

from GameDataSpider.sqlConn import connSql


class GamedataSpider(scrapy.Spider):
    name = '4sfCrawler'

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
        for TR in response.xpath('//*[@id="list"]/div[@class="table"]/table/tr'):
            if TR.css("td"):
                data = {
                    "title": TR.xpath('td[1]/@title').extract_first(),
                    "ip": TR.xpath('td[2]/@title').extract_first(),
                    "opentime": TR.xpath('td[3]/@title').extract_first(),
                    "line": TR.xpath('td[4]/@title').extract_first(),
                    "introduce": TR.xpath('td[5]/@title').extract_first(),
                    "customer": TR.xpath('td[6]/@title').extract_first(),
                    "homepage": TR.xpath('td[7]/@title').extract_first()
                }
                dataItem.append(data)

        item["data"] = dataItem
        item["shortName"] = urlparse(response.url).hostname
        yield item
