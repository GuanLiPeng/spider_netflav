"""
测试用

运行：
  scrapy crawl test
"""
import scrapy


# TODO:setting中记得修改配置
class Test(scrapy.Spider):
    # 爬虫名字
    name = 'test'
    # 列表页链接
    start_urls = [
        ''
    ]
    
    def parse(self, response, **kwargs):
        """@override \n
        默认解析函数，此函数对列表页进行了解析
        """
        lis = ""
        for item in response.xpath('//div[@class="genre_filter_root"]/div[@class="genre_filter_item"]/text()').getall():
            if len(lis) > 0: lis += '，'
            lis += item
        print(lis)
