# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import requests

class GamedataspiderPipeline(object):

    def process_item(self, item, spider):

        post_url = "http://chuan.weifantech.com/admin/Api/getdata"
        post_data = {
            "txt": item["data"],
            "site_name": item["shortName"]
        }
        res = requests.post(post_url, json=post_data, timeout=600)
        print("数据发送结果：", res.text)
        return item
