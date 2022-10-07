# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderNetflavItem(scrapy.Item):
    """
    定义要爬取的字段：
    
    AV_id      番号 \n
    AV_date    发行日期 \n
    AV_title   番名 \n
    AV_sort    类别 \n
    """
    AV_id = scrapy.Field()
    AV_date = scrapy.Field()
    AV_title = scrapy.Field()
    AV_sort = scrapy.Field()


class SpiderNetflavImageItem(scrapy.Item):
    """
    定义下载图片的字段：
    
    AV_id       番号 \n
    image_urls  图片url列表 \n
    """
    AV_id = scrapy.Field()
    image_urls = scrapy.Field()
