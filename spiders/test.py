import scrapy

from spider_netflav.items import SpiderNetflavImageItem

"""
测试用

运行：(setting中记得修改配置)
  scrapy crawl test(爬虫名)
"""


class Test(scrapy.Spider):
    # TODO: 是否使用测试模式（仅爬取少量数据）
    DEBUG = True
    # 爬虫名字
    name = 'test'
    # 列表页链接(&page不要放进去)
    start_urls = ['https://netflav.com/video?id=iYgATu12rL']
    # 图片下载的前缀链接
    prefix_url = 'https://pics.dmm.co.jp/digital/video/'
    # 开始页数
    page = 1
    # 总页数
    MAX_PAGE = 4
    
    # @override 默认开始函数
    def parse(self, response, **kwargs):
        print(response.xpath('//meta[@property="og:image"]/@content').get())
        print(response.xpath('//meta[@property="og:url"]/@content').get())
    