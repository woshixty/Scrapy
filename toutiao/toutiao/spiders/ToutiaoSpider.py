from scrapy import Request
from scrapy.spiders import Spider
from selenium import webdriver
from toutiao.items import ToutiaoItem


class ToutiaoSpider(Spider):
    # 定义爬虫名称
    name = "toutiao"

    # 构造函数
    def __init__(self):
        # 生成PhantomJS对象
        self.driver = webdriver.PhantomJS

    # 获取初始化Request
    def start_requests(self):
        url = 'https://www.toutiao.com/ch/news_hot/'
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/89.0.4389.114 Safari/537.36 "
        }
        # 生成请求对象，设置URL
        yield Request(url, headers=headers)

    # 数据解析方法
    def parse(self, response):
        item = ToutiaoItem()
        list_selector = response.xpath("//div[@class='single-mode-rbox-inner']")
        for div in list_selector:
            try:
                # 标题
                title = div.xpath("./div[@class='title-box']/a/text()").extract()
                # 去除标题空格
                title = title[0].strip(" ")
                # 来源
                source = div.xpath("./div[@class='footer-bar']/div[1]/a[2]/text()").extract()
                # 去除点号与全角空格
                source = source[1].strip("·").strip(" ")
                # 评论数
                comment = div.xpath("./div[@class='footer-bar']/div[1]/a[3]/text()").extract()
                comment = comment[1]
                item["title"] = title
                item["source"] = source
                item["comment"] = comment

                print("item:" + item)
                yield item
            except:
                continue
