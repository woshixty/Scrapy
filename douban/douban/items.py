# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()      # 电影名称
    directors = scrapy.Field()  # 导演
    casts = scrapy.Field()  # 演员
    rate = scrapy.Field()  # 评分
    cover = scrapy.Field()  # 封面
