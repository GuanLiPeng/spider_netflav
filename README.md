# spider_netflav



## 项目简介

一个爬虫项目，项目中存在两个爬虫文件，分别是`image_spider.py`和`text_spider.py`，前者用来爬取详情页的图片下载到本地，后者用来爬取详情页文本信息（详情页爬取哪些内容可参考 `items.py`中定义的变量）

项目中文本爬取和图片爬取使用了不同的配置，具体参见`settings.py`中的内容

在爬取时，不可两个爬虫的配置同时使用

运行爬虫前，请先更改`settings.py`中的`IS_SPIDER_TEXT`变量的值



## 项目结构

```
spider_netflav
  ├── README
  ├── items.py (爬取字段定义)
  ├── settings.py (设置文件)
  ├── pipelines.py (图片下载通道)
  ├── ...
  |
  └── spiders
        ├── image_spider.py (图片下载爬虫)
        ├── text_spider.py (文本爬虫)
        └── ...
```



## 开发环境

| 环境    | 版本          |
| ------- | ------------- |
| PyCharm | 2022.2 社区版 |
| Python  | 3.8           |
| Scrapy  | 2.5.0         |



## 运行程序

**文本爬取**

1.   将`setting.py`中`IS_SPIDER_TEXT`的值设为`True`

2.   在终端中输入命令：`scrapy crawl text -o text.json`（注意命令行要运行在当前项目的目录下）

**图片爬取**

1.   将`setting.py`中`IS_SPIDER_TEXT`的值设为`False`
2.   在终端中输入命令：`scrapy crawl image`