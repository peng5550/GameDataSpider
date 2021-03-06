# -*- coding: utf-8 -*-
import scrapy
from GameDataSpider.items import GamedataspiderItem
from urllib.parse import urlparse
from GameDataSpider.sqlConn import connSql


class GamedataSpider(scrapy.Spider):
    name = '2wwCrawler'

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
        for UL in response.xpath('//div[@class="kf-table-center-table-body"]/div/ul'):
            data = {
                "title": UL.xpath('li[1]//a/text()').extract_first("").strip(),
                "ip": UL.xpath('li[2]//a/text()').extract_first("").strip(),
                "opentime": UL.xpath('li[3]/p/text()').extract_first("").strip(),
                "line": None,
                "introduce": UL.xpath('li[4]/div/p[1]/text()').extract_first(),
                "customer": None,
                "homepage": UL.xpath('li[6]//a/@href').extract_first()
            }
            dataItem.append(data)

        item["data"] = dataItem
        item["shortName"] = urlparse(response.url).hostname
        yield item
