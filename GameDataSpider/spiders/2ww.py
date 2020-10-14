# -*- coding: utf-8 -*-
import scrapy
from GameDataSpider.items import GamedataspiderItem
from urllib.parse import urlparse

class GamedataSpider(scrapy.Spider):
    name = '2wwCrawler'

    def start_requests(self):
        start_urls = ['https://www.2ww.com/h5/index/ifindex.html']
        for start in start_urls:
            yield scrapy.Request(start, dont_filter=True, callback=self.detail_page)

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
