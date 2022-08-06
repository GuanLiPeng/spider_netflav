# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 定义要爬取的字段
class SpiderNetflavItem(scrapy.Item):
    """
     番号 AV_id
     发行日期 AV_date
     番名 AV_title
     类别 AV_sort
    """
    AV_id = scrapy.Field()
    AV_date = scrapy.Field()
    AV_title = scrapy.Field()
    AV_sort = scrapy.Field()


# 定义下载图片的字段
class SpiderNetflavImageItem(scrapy.Item):
    """
     番号 AV_id
     图片url列表 image_urls
    """
    AV_id = scrapy.Field()
    image_urls = scrapy.Field()
