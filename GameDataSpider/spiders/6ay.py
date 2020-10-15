# -*- coding: utf-8 -*-
import scrapy
from GameDataSpider.items import GamedataspiderItem
from urllib.parse import urlparse

from GameDataSpider.sqlConn import connSql


class GamedataSpider(scrapy.Spider):
    name = '6ayCrawler'

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
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Referer': 'https://www.6ay.com.7xq.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
            }
            yield scrapy.Request(start, dont_filter=True, headers=headers, meta={"othLink": oth_urls}, callback=self.detail_page)

    def detail_page(self, response):
        item = GamedataspiderItem()
        dataItem = []
        for TR in response.xpath('//div[@class="table"]/table/tr'):
            if TR.css("td"):
                data = {
                    "title": TR.xpath('td[1]/@title').extract_first(),
                    "ip": TR.xpath('td[2]/@title').extract_first(),
                    "opentime": TR.xpath('td[3]/@title').extract_first("").strip(),
                    "line": TR.xpath('td[4]/@title').extract_first(),
                    "introduce": TR.xpath('td[5]/@title').extract_first("").strip(),
                    "customer": TR.xpath('td[6]/@title').extract_first(),
                    "homepage": TR.xpath('td[7]/a/@href').extract_first(),
                }
                dataItem.append(data)

        item["data"] = dataItem
        item["shortName"] = urlparse(response.url).hostname
        yield item
