from scrapy import Request
from scrapy.spiders import Spider
from QQMusic.items import QqmusicItem
import json

class MusicSpider(Spider):
    name = 'music'
    # 定义属性、设置用户代理
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/89.0.4389.114 Safari/537.36 "
    }

    def start_requests(self):
        url = "https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?&topid=4"
        # 生成请求对象
        yield Request(url, headers=self.headers)

    # 数据解析
    def parse(self, response):
        item = QqmusicItem()
        # 获取json数据格式
        json_text = response.text
        # 使用json.loads解码json格式数据，返回python的数据类型
        # 这里的music_dict是一个字典类型
        music_dict = json.loads(json_text)
        # for循环遍历每首歌曲
        for one_music in music_dict["songlist"]:
            # 获取歌曲
            item["song_name"] = one_music["data"]["songname"]
            # 获取唱片
            item["album_name"] = one_music["data"]["albumname"]
            # 获取歌手
            item["singer_name"] = one_music["data"]["singer"][0]["name"]
            # 获取时长
            item["interval"] = one_music["data"]["interval"]

            yield item