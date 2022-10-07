"""
抓取内容：
  番号(AV_id)  发行日期(AV_date)  番名(AV_title)  类别(AV_sort)

运行：
  scrapy crawl text -o text.csv
"""
import scrapy

from spider_netflav.items import SpiderNetflavItem


# TODO: setting中记得修改配置
class TextSpider(scrapy.Spider):
    # TODO: 是否使用测试模式（仅爬取少量数据）
    DEBUG = False
    # 爬虫名字
    name = 'text'
    
    # 单个详情页的链接
    detail_urls = [
    ]
    # 列表页链接(&page不要放进去)
    index_url = ''
    # 列表页开始页数
    page = 1
    # 列表页总页数
    END_PAGE = 1
    
    def start_requests(self):
        """@override \n
        此函数将优先调用，可在此处进行初始化或选择不同的解析函数
        """
        # 单独详情页爬取
        if len(self.detail_urls) > 0:
            for itemUrl in self.detail_urls:
                yield scrapy.Request(url=itemUrl, callback=self.parse_detail, meta={'detail_href': itemUrl})
        # 索引页爬取
        if len(self.index_url) > 0:
            yield scrapy.Request(url=self.index_url, callback=self.parse)
    
    def parse(self, response, **kwargs):
        """@override \n
        默认解析函数，此函数对列表页进行了解析，并进一步调用parse_detail()函数
        """
        for div in response.xpath('//div[@class="grid_cell"]'):  # 单个电影的div结构
            detail_href = 'https://netflav.com' + div.xpath('.//a[1]/@href').get()  # 得到单个电影的详情链接
            yield scrapy.Request(detail_href, callback=self.parse_detail, meta={'detail_href': detail_href})
            if self.DEBUG: break
            # time.sleep(1)  # 请求间隔
        
        # 翻页后继续解析
        if self.DEBUG: return
        if self.page < self.END_PAGE:
            self.page += 1
            next_url = self.index_url + '&page=' + str(self.page)
            print(f'Now page= {self.page}, url= {next_url}')
            yield scrapy.Request(next_url, callback=self.parse)  # 调用parse()函数爬取下一页
    
    def parse_detail(self, response):
        """
        爬取详情页，并存入item
        """
        root_div = response.xpath('//div[@class="videodetail_root"]')
        item = SpiderNetflavItem()
        item['AV_id'] = root_div.xpath('./div[4]/div[1]/div[2]/text()').get()  # 提取出的内容：ADN-242
        item['AV_date'] = root_div.xpath('./div[4]/div[2]/div[2]/text()').get()  # 提取出的内容：2019-01-13
        item['AV_title'] = root_div.xpath('./div[1]/text()').get()
        sort = ""
        for string in root_div.xpath('./div[4]/div[4]//text()').getall():
            if (',' not in string) and (':' not in string) and ('類別' not in string):
                if len(sort) > 0: sort += '，'
                sort += string
        item['AV_sort'] = sort
        print(f"{item['AV_id']} is success, detail_href= {response.meta['detail_href']}")
        yield item
