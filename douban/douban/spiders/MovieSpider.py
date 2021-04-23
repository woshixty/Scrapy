from scrapy import Request
from scrapy.spiders import Spider
from douban.items import DoubanItem
import json


class MovieSpider(Spider):
    name = 'movies'
    currentPage = 1
    # 定义headers属性，设置用户代理
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/89.0.4389.114 Safari/537.36 "
    }

    def start_requests(self):
        url = "https://movie.douban.com/j/new_search_subjects?" \
              "sort=U&range=0,10" \
              "&tags=电影&start=0&countries=中国大陆"
        # 生成请求对象
        yield Request(url, headers=self.headers)

    def parse(self, response, **kwargs):
        item = DoubanItem()
        # 获取JSON数据
        json_text = response.text
        # 解码
        movie_dict = json.loads(json_text)
        if len(movie_dict["data"]) == 0:
            return
        # for循环遍历每部电影
        for one_movie in movie_dict["data"]:
            # 获取电影名称
            item["title"] = one_movie["title"]
            # 获取导演
            item["directors"] = one_movie["directors"]
            # 获取演员
            item["casts"] = one_movie["casts"]
            # 获取评分
            item["rate"] = one_movie["rate"]
            # 获取封面
            item["cover"] = one_movie["cover"]

            yield item

        # 爬取更多数据
        url_next = 'https://movie.douban.com/j/new_search_subjects?tags=电影&start=%d&countries=中国大陆'%(self.currentPage*20)
        self.currentPage += 1
        yield Request(url_next, headers=self.headers)