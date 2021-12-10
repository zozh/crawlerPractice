# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# 写入redis数据库
from redis import Redis
import save


class RecruitmentPipeline:
    def process_item(self, item, spider):
        return item


class RedisPipeLine(object):
    conn = None

    def open_spider(self, spider):
        self.conn = Redis(host='127.0.0.1', port=6379)

    def process_item(self, item, spider):
        # item本身就是一个字典，因此可以使用队列数据结构
        self.conn.lpush('bossList', item)
        # 可以不写，没有下个管道类
        return item

    def close_spider(self, spider):
        # 关闭时把redis数据存到mongoDB
        # mongoDB = save.mongoDB()
        # 把redis bossList里的数据都转移到warehouse里
        self.conn.close()