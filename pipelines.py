# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re

import scrapy
from scrapy.pipelines.images import ImagesPipeline


class SpiderNetflavPipeline(ImagesPipeline):
    # @override 对图片地址发起请求
    def get_media_requests(self, item, info):
        for image_url in item["image_urls"]:
            yield scrapy.Request(image_url, meta={'item': item, 'image_url': image_url})
    
    # @override 当一个单独项目中的所有图片请求完成时（要么完成下载，要么因为某种原因下载失败）将被调用
    def item_completed(self, results, item, info):
        return item
    
    # @override 图片存放的路径
    def file_path(self, request, response=None, info=None, *, item=None):
        item = request.meta['item']
        folder_name = item['AV_id']  # AND-123
        tail = str(request.meta['image_url']).split('/')[-1]  # adn00381pl.jpg  or  adn00381jp-1.jpg
        name: str
        if 'pl' in tail:
            name = folder_name + "-0.jpg"  # adn00381pl.jpg -> AND-123-0.jpg
        else:
            name = folder_name + re.search(r'-\d+.jpg', tail).group()  # adn00381jp-1.jpg -> AND-123-1.jpg
        file_path = rf'{folder_name}\{name}'
        return file_path  # 路径格式：AND-123\AND-123-1.jpg
