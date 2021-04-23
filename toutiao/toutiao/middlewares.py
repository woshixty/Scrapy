# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import time  # 时间模块
from scrapy import signals
from scrapy.http import HtmlResponse  # html响应模块
from selenium.webdriver.common.by import By  # By模块
from selenium.webdriver.support import expected_conditions as EC  # 预期条件模块
from selenium.webdriver.support.wait import WebDriverWait  # 等待模块
from selenium.common.exceptions import TimeoutException, NoSuchElementException  # 异常模块
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class ToutiaoSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class ToutiaoDownloaderMiddleware:
    def process_request(self, request, spider):
        # 判断name是头条的爬虫
        if spider.name == "toutiao":
            # 打开url对应界面
            spider.driver.get(request.url)

            print("as")
            print("as")
            print("as")
            print("as")

            try:
                # 设置显式等待时间，5秒
                wait = WebDriverWait(spider.driver, 10)
                # 等待新闻列表容器加载完成
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='single-mode']")))
                # 使用JS的scrollTo方法将页面向下滚到最中间
                spider.driver.execute_script('window.scrollTo(0, document.body.scrollHeight/2)')
                for i in range(10):
                    time.sleep(10)
                    # 使用JS的scrollTo方法滚到最底部
                    spider.driver.execute_script('window.scrollTo(0, document.body.scrollHeight/2)')
                # 获取加载完成的网页源代码
                origin_code = spider.driver.page_source
                # 将源代码构造成一个Response对象并返回
                res = HtmlResponse(url=request.url, encoding="utf8", body=origin_code, request=request)
                return res
            except TimeoutException:
                print("TIME OUT")
            except NoSuchElementException:
                print("NO SUCH ELEMENT")
        return None