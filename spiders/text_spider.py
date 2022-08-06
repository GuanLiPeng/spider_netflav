import time
import scrapy
from spider_netflav.items import SpiderNetflavItem

'''
抓取内容：
  番号(AV_id)  发行日期(AV_date)  番名(AV_title)  类别(AV_sort)
 
运行：(setting中记得修改配置)
  scrapy crawl text(爬虫名) -o text.json
'''


class TextSpider(scrapy.Spider):
    # TODO: 是否使用测试模式（仅爬取少量数据）
    DEBUG = False
    # 爬虫名字
    name = 'text'
    # 列表页链接
    start_urls = ['https://netflav.com/all?actress=%E9%88%B4%E5%8E%9F%E3%82%A8%E3%83%9F%E3%83%AA']
    # 开始页数
    page = 1
    # 总页数
    MAX_PAGE = 4
    
    # @override 默认开始函数
    def parse(self, response, **kwargs):
        for div in response.xpath('//div[@class="grid_cell"]'):  # 单个电影的div结构
            detail_href = 'https://netflav.com' + div.xpath('.//a[1]/@href').get()  # 得到单个电影的详情链接
            yield scrapy.Request(detail_href, callback=self.parse_detail, meta={'detail_href': detail_href})
            if self.DEBUG: break
            # time.sleep(1)  # 请求间隔
        
        # 翻页后继续解析
        if self.DEBUG: return
        if self.page < self.MAX_PAGE:
            self.page += 1
            next_url = self.start_urls[0] + '&page=' + str(self.page)
            print(f'Now page = {self.page}, url = {next_url}')
            yield scrapy.Request(next_url, callback=self.parse)  # 调用parse()函数爬取下一页
    
    # 爬取详情页
    def parse_detail(self, response):
        root_div = response.xpath('//div[@class="videodetail_root"]')
        item = SpiderNetflavItem()
        item['AV_id'] = root_div.xpath('./div[4]/div[1]/div[2]/text()').get()  # 提取出的内容：ADN-242
        item['AV_date'] = root_div.xpath('./div[4]/div[2]/div[2]/text()').get()  # 提取出的内容：2019-01-13
        item['AV_title'] = root_div.xpath('./div[1]/text()').get()
        temp = []
        for string in root_div.xpath('./div[4]/div[4]//text()').getall():
            if (',' not in string) and (':' not in string): temp.append(string)
        item['AV_sort'] = temp
        print(f"{item['AV_id']} is success, detail_href = {response.meta['detail_href']}")
        yield item
