import time
import scrapy

from spider_netflav.items import SpiderNetflavImageItem

'''
抓取内容：
  AV_id  image_urls

运行：(setting中记得修改配置)
  scrapy crawl image(爬虫名)
'''


class ImageSpider(scrapy.Spider):
    # TODO: 是否使用测试模式（仅爬取少量数据）
    DEBUG = False
    # 爬虫名字
    name = 'image'
    # 列表页链接(&page不要放进去)
    start_urls = ['https://netflav.com/all?actress=%E9%88%B4%E5%8E%9F%E3%82%A8%E3%83%9F%E3%83%AA']
    # 图片下载的前缀链接
    prefix_url = 'https://pics.dmm.co.jp/digital/video/'
    # 开始页数
    page = 1
    # 总页数
    MAX_PAGE = 4
    
    # @override 默认开始函数
    def parse(self, response, **kwargs):
        for div in response.xpath('//div[@class="grid_cell"]'):  # 单个电影的div结构
            detail_href = 'https://netflav.com' + div.xpath('.//a[1]/@href').get()  # 得到单个电影的详情链接
            # 判断当前div是否有图片
            have_img: bool = div.xpath('.//a[@class="video_grid_overlays_preview_tags"]/text()').get() is not None
            # 如果有图片，调用parse_detail()函数爬取详情页
            if have_img:
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
    # 思路：通过番号拼凑出下载图片的完整链接
    def parse_detail(self, response):
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
        print(f"{suffix} success, image len={len(image_urls)}, detail_href={response.meta['detail_href']}")  # 打印结果
        yield item
