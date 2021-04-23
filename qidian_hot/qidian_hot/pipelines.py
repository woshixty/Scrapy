# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exceptions import DropItem
import pymysql

class QidianHotPipeline(object):
    def process_item(self, item, spider):
        # 判断小说是连结还是完结
        if item["form"] == "连载":
            item["form"] = "lianzai"
        else:
            item["form"] = "wanjie"
        return item

class DuplicatesPipeline(object):
    def __init__(self):
        # 定义一个作者姓名的集合
        self.author_set = set()

    def process_item(self, item, spider):
        if item['author'] in self.author_set:
            # 抛弃重复的Item，跑出异常
            raise DropItem("查找到相同作者名称项目：%s" % item)
        elif item['author'] == "老鹰吃小鸡":
            raise DropItem("查找到作者\"老鹰吃小鸡\"：%s" % item)
        else:
            self.author_set.add(item['author'])
        return item

class SaveToTxtPipeline(object):
    file_name = "hot.txt"
    file = None

    @classmethod
    def from_crawler(cls, crawler):
        # 获取配置文件中FILE_NAME的值
        # 获取配置失败就是用默认值
        cls.file_name = crawler.settings.get("FILE_NAME", "default.txt")
        return cls()

    # Spider开启时，执行文件打开操作
    def open_spider(self, spider):
        # 追加形式打开文件
        self.file = open(self.file_name, "a", encoding="utf-8")

    # 数据处理
    def process_item(self, item, spider):
        # 获取item的各个字段
        # 字符之间用分号隔开；字符末尾要有换行符
        novel_str = item['name'] + ";" + \
                    item['author'] + ";" + \
                    item['type'] + ";" + \
                    item['form'] + "\n"
        # 写入文件
        self.file.write(novel_str)
        return item

    def close_file(self, spider):
        # 关闭文件
        self.file.close()

class MySQLPipeline(object):
    # Spider开启时，获取数据库配置信息，链接MySql服务器
    def __init__(self):
        db_name = 'qidian'
        host = '8.131.57.6'
        user = 'root'
        pwd = 'Flzx3qcYsyhl9t'
        self.conn = pymysql.connect(host=host, port=3306, user=user, password=pwd, db=db_name)
        self.cursor = self.conn.cursor()

    # def open_spider(self, spider):
    #     # 获取配置文件中的MySQL配置信息
    #     # db_name = spider.settings.get("MYSQL_DB_NAME", "qidian")
    #     # host = spider.get("MYSQL_HOST", "8.131.57.6")
    #     # user = spider.settings.get("MYSQL_USER", "root")
    #     # pwd = spider.settings.get("MYSQL_PASSWORD", "Flzx3qcYsyhl9t")
    #     # 链接MySQL数据库
    #     # 创建连接
    #     # 创建游标

    # 将item实体类对象保存到数据库
    def process_item(self, item, spider):
        values = (
            item['name'],
            item['author'],
            item['type'],
            item['form']
        )
        # 设计插入数据库的SQL语句
        sql = 'insert into hot(name, author, type, form)values (%s, %s, %s, %s)'
        # 执行sql语句
        self.cursor.execute(sql, values)
        return item

    def close_spider(self, spider):
        # 提交数据
        self.conn.commit()
        # 关闭游标
        self.cursor.close()
        # 关闭数据库
        self.conn.close()
