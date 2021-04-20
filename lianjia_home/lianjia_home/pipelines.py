# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# import re
# from scrapy.exceptions import DropItem
#
#
# class FilterPipeline(object):
#     def process_item(self, item, spider):
#         # 总面积、提取数字
#         item["area"] = re.findall(r"\d+\.?\d*", item["area"])[0]
#         # 单价、提取数字
#         item["unit_price"]=re.findall(r"\d+\.?\d*", item["unit_price"])[0]
#         # 如果房源过少、就抛弃该条数据
#         if item["direction"] == "暂无数据":
#             # 抛弃缺少数据的Item
#             raise DropItem("房屋朝向无数据，抛弃此项目：%s" % item)
#         return item
#
#
# class CSVPipeline(object):
#     index = 0
#     file = None
#
#     # Spider开启时，执行打开文件操作
#     def open_spider(self, spider):
#         # 以追加形式打开文件
#         self.file = open("home1.csv", "a", encoding="utf-8")
#
#     def process_item(self, item, spider):
#         # 第一行写入列名
#         if self.index == 0:
#             column_name = "name, type, direction, fitment, elevator, total_price, " \
#                           "unit_price, property\n"
#             # 将字符写入文件中
#             self.file.write(column_name)
#             self.index = 1
#             # 获取item中各个字段，将其连接成一个字符串
#             # 字段之间用逗号隔开
#             # 反斜杠用于连接下一行的字符串
#             # 字符串末尾要有换行符\n
#             home_str = item['name'] + "," + \
#                        item["type"] + "," + \
#                        item["area"] + "," + \
#                        item["direction"] + "," + \
#                        item["fitment"] + "," + \
#                        item["elevator"] + "," + \
#                        item["total_price"] + "," + \
#                        item["unit_price"] + "," + \
#                        item["property"] + "\n"
#             # 将字符串写入到文件中
#             self.file.write(home_str)
#
#             print("Hello World")
#             print(item)
#
#             return item
#
#     def close_file(self, spider):
#         self.file.close()

import re  # 正则表达式模块
from scrapy.exceptions import DropItem


class FilterPipeline(object):
    def process_item(self, item, spider):
        # 总面积，提取数字
        # item["area"] = re.findall(r"\d+\.?\d*", item["area"])[0]
        # 单价，提取数字
        # item["unit_price"] = re.findall(r"\d+\.?\d*", item["unit_price"])[0]
        # #产权，提取数字
        # item["property"]=re.findall(r"\d+\.?\d*",item["property"])[0]
        # 如果房屋朝向缺少数据，则抛弃该条数据
        # if item["direction"] == "暂无数据":
        # 抛弃缺少数据的Item项
        # raise DropItem("房屋朝向无数据，抛弃此项目: %s" % item)
        return item


class CSVPipeline(object):
    index = 0  # 记录起始位置
    file = None  # 文件对象

    # Spider开启时，执行打开文件操作
    def open_spider(self, spider):
        # 以追加形式打开文件
        self.file = open("home2.csv", "a", encoding="utf-8")

    # 数据处理
    def process_item(self, item, spider):
        # 第一行写入列名
        if self.index == 0:
            column_name = "name,type,area,direction,fitment,elevator,total_price,unit_price,property\n"
            # 将字符串写入到文件中
            self.file.write(column_name)
            self.index = 1
        # 获取item中各个字段，将其连接成一个字符串
        # 字段之间用逗号隔开
        # 反斜杠用于连接下一行的字符串
        # 字符串末尾要有换行符\n
        home_str = item['name'] + "," + \
                   item["type"] + "," + \
                   item["area"] + "," + \
                   item["direction"] + "," + \
                   item["fitment"] + "," + \
                   item["elevator"] + "," + \
                   item["total_price"] + "," + \
                   item["unit_price"] + "," + \
                   item["property"] + "\n"
        # 将字符串写入到文件中
        self.file.write(home_str)
        self.file.flush()
        return item

    # Spider关闭时，执行关闭文件操作
    def close_spider(self, spider):
        # 关闭文件
        self.file.close()
