from abc import ABC

from scrapy import Request
from scrapy.spiders import Spider
from qidian_hot.items import QidianHotItem
from scrapy.loader import ItemLoader

class HotSalesSpider(Spider, ABC):
    # 定义爬虫名称-区分不同爬虫的唯一标识
    name = 'hot'
    # 设置当前页 默认为1
    current_page = 1

    # 设置用户代理
    # qidian_headers = {
    #     "User-Agent": "Mozilla/"
    #     "5.0 (Macintosh;"
    #     "Intel Mac OS X 10_15_7) AppleWebKit/"
    #     "537.36 (KHTML, like Gecko) Chrome/"
    #     "89.0.4389.114 Safari/"
    #     "537.36"
    # }
    # 获取初始化Request
    def start_requests(self):
        # url = "https://www.qidian.com/rank/hotsales?page=5&style=1"
        url = "https://www.qidian.com/rank/hotsales?style=1"
        # 生成请求对象，设置url、headers、callback-制定回调函数
        # yield Request(url, headers=self.qidian_headers, callback=self.qidian_parse)
        yield Request(url, callback=self.qidian_parse)

    # 起始的URL列表-存储目标网站地址-存放要爬取的目标网页地址的列表
    # start_urls = ['https://www.qidian.com/rank/hotsales?page=1&style=1',
    #               'https://www.qidian.com/rank/hotsales?page=2&style=1']
    # start_urls = 'https://www.qidian.com/rank/hotsales?style=1'

    # start_request(): 引擎自动调用该方法，读取URL（start_urls列表中的）
    # 1、定义Spider类-HotSalesSpider
    # 2、确定Spider名称-name
    # 3、获取初始请求-start_request()
    # 4、解析数据-parse()

    # 解析函数
    def qidian_parse(self, response):
        # 使用xpath定位到div元素保存到列表中
        list_selector = response.xpath("//div[@class='book-mid-info']")
        # 依次读取每部小说的元素，从中获取名称、作者、类型、形式
        for one_selector in list_selector:
            # 生成ItemLoader实例
            # 参数item接收QidianHotItem实例，selector接收一个选择器
            novel = ItemLoader(item=QidianHotItem(), selector=one_selector)
            # 获取小说名称
            # name = one_selector.xpath("h4/a/text()").extract()[0]
            novel.add_xpath("name", "h4/a/text()")
            # 获取作者
            # author = one_selector.xpath("p[1]/a[1]/text()").extract()[0]
            novel.add_xpath("author", "p[1]/a[1]/text()")
            # 获取类型
            # type = one_selector.xpath("p[1]/a[2]/text()").extract()[0]
            novel.add_xpath("type", "p[1]/a[2]/text()")
            # 获取形式（连载、完结）
            # form = one_selector.xpath("p[1]/span/text()").extract()[0]
            novel.add_css("form", ".author span::text")
            # 将爬取到一本小说保存到字典中
            # hot_dict = {
            #     "name": name,
            #     "author": author,
            #     "type": type,
            #     "form": form
            # }
            # 保存到item中
            # item = QidianHotItem()
            # item["name"] = name
            # item["author"] = author
            # item["type"] = type
            # item["form"] = form
            # 使用yieId返回字典
            # yield hot_dict
            # yield item
            # 提取好的数据返回
            yield novel.load_item()
        # 获取下一页，并生成Request请求，提交给引擎
        # 获取下一页URL
        self.current_page += 1
        if self.current_page <= 3:
            next_url = "https://www.qidian.com/rank/hotsales?style=1&page=%d" % self.current_page
            # 根据URL生成Request，使用yield返回给引擎
            yield Request(next_url, callback=self.qidian_parse)