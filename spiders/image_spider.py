"""
抓取内容：
  AV_id  image_urls

运行：
  scrapy crawl image
"""
import scrapy

from spider_netflav.items import SpiderNetflavImageItem


# TODO: setting中记得修改配置
class ImageSpider(scrapy.Spider):
    # TODO: 是否使用测试模式（仅爬取少量数据）
    DEBUG = False
    # 爬虫名字
    name = 'image'
    # 图片下载的前缀链接
    prefix_url = 'https://pics.dmm.co.jp/digital/video/'
    
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
            # 判断当前div是否有图片
            have_img: bool = div.xpath('.//a[@class="video_grid_overlays_preview_tags"]/text()').get() is not None
            # 如果有图片，调用parse_detail()函数爬取详情页
            if have_img:
                yield scrapy.Request(detail_href, callback=self.parse_detail, meta={'detail_href': detail_href})
            if self.DEBUG: break
        
        # 翻页后继续解析
        if self.DEBUG: return
        if self.page < self.END_PAGE:
            self.page += 1
            next_url = self.index_url + '&page=' + str(self.page)
            print(f'Now page= {self.page}, url= {next_url}')
            yield scrapy.Request(next_url, callback=self.parse)  # 调用parse()函数爬取下一页
    
    def parse_detail(self, response):
        """
        爬取详情页，并存入item \n
        思路：通过番号拼凑出下载图片的完整链接
        """
        cover_url: str = response.xpath('//meta[@property="og:image"]/@content').get()
        image_urls = [cover_url]
        suffix = cover_url.split('/')[-2]  # 示例：http.../118raw00006/118raw00006pl.jpg -> 118raw00006
        list_len = len(response.xpath('//div[@class="withRatio _16x10"]').getall())  # 得到图片个数
        for index in range(1, list_len):
            image_urls.append(self.prefix_url + f'{suffix}/{suffix}jp-{index}.jpg')  # https...adn00242/adn00242jp-1.jpg
        
        # 装载数据
        item = SpiderNetflavImageItem()
        item['AV_id'] = response.xpath('//*[@id="video-details"]/div[4]/div[1]/div[2]/text()').get()
        item['image_urls'] = image_urls
        # 打印结果
        print(f"{item['AV_id']} success, image numbers= {len(image_urls)}, detail_href= {response.meta['detail_href']}")
        yield item
