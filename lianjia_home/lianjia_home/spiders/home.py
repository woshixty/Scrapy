import scrapy
from scrapy import Request
from scrapy.spiders import Spider
# 用于数据封装
from lianjia_home.items import LianjiaHomeItem

class HomeSpider(scrapy.Spider):
    name = 'home'
    current_page = 1  # 记录当前的页数，默认为第1页
    total_page = 4  # 总页数

    def start_requests(self):  # 获取初始请求
        url = "https://su.lianjia.com/ershoufang/"
        # 生成请求对象
        yield Request(url)

    # allowed_domains = ['https://su.lianjia.com/ershoufang/']
    # start_urls = ['http://https://su.lianjia.com/ershoufang//']

    def parse(self, response):  # 主页面解析函数
        # 1、提取主页面中的房屋信息
        # 使用xpath定位到二手房信息的div元素
        list_selector = response.xpath("//li/div[@class='info clear']")
        # 依次遍历每个选择器，获取信息
        for one_selector in list_selector:
            try:
                # 房屋名称
                name = one_selector.xpath("div[@class='title']/a/text()").extract_first()
                # 获取其他信息
                other = one_selector.xpath("div[@class='address']/"
                                           "div[@class='houseInfo']"
                                           "/text()").extract_first()
                # 以｜作为分隔符，转换列表
                other_list = other.split("|")
                type = other_list[1].strip(" ")
                area = other_list[2].strip(" ")
                direction = other_list[3].strip(" ")
                fitment = other_list[4].strip(" ")
                elevator = other_list[5].strip(" ")

                # 获取总价和单价存入列表
                price_list = one_selector.xpath("div[@class='priceInfo']//span/text()")
                # 总价
                total_price = price_list[0].extract()
                # 单价
                unit_price = price_list[1].extract()
                item = LianjiaHomeItem()  # 生成对象
                # 将信息保存到item对象中去
                item["name"] = name.strip(" ")
                item["type"] = type.strip(" ")
                item["area"] = area.strip(" ")
                item["direction"] = direction.strip(" ")
                item["fitment"] = fitment.strip(" ")
                item["elevator"] = elevator.strip(" ")
                item["total_price"] = total_price.strip(" ")
                item["unit_price"] = unit_price.strip(" ")

                print(item)

                # 获取详情页url
                url_more = one_selector.xpath("div[@class='title']/a/@href").extract_first()
                # 生成详情页的请求对象，参数mate保存房屋部分数据
                print(url_more)

                yield Request(url_more,
                              meta={"item": item},
                              callback=self.property_parse)
            except:
                print("error")
                pass
        # 4、获取下一页url，并生成Request请求
        # （1）获取下一页URl。仅在解析第一页时获取总页数的值
        # if self.current_page == 1:
            # 属性page-data的值中包含总页数和当前页。
            # self.total_page = response.xpath("//div[@class='page-box house-lst-page-box']"
            #                                  "//@page-data").re("\d+")
            # print(self.total_page)
            # 获取总页数
            # pass
        self.current_page += 1
        if self.current_page <= self.total_page:  # 判断页数是否已经越界
            next_url = "https://su.lianjia.com/ershoufang/pg%d" % self.current_page
            # （2）根据URL生成Request，使用yield提交引擎

            print(next_url)

            yield Request(next_url)

    # 详情页解析函数
    def property_parse(self, response):
        # 1.获取产权信息
        property = response.xpath("//*[@id='introduction']/div/div/div[2]/div[2]/ul/li[6]/span[2]/text()").extract_first()
        # 2.获取主页面中的房屋信息
        item = response.meta["item"]
        # 3.将产权信息放到item中，返回给引擎
        item["property"] = property
        yield item
