# coding=utf-8
# 获取肯德基餐厅位置信息
import requests
import hadToClimb
import json
import math
import save
import time
import random


def kfc(data: dict):
    url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=keyword'
    data = data
    res = requests.post(url=url, headers=hadToClimb.get_ua(), data=data).json()
    return res


keyword = '北京'
data = {
    'cname': '',
    'pid': '',
    'keyword': keyword,
    'pageIndex': 1,
    'pageSize': 10,
}
# 第一次获取总页数
json_data = kfc(data)
rowcount = math.ceil(json_data['Table'][0]['rowcount'] / data['pageSize'])
# 通过索引与总索引做对比
mongoDB = save.mongoDB('try', 'kfc')
while data['pageIndex'] < rowcount:
    data['pageIndex'] += 1
    list_data = kfc(data)['Table1']
    mongoDB.create(list_data)
    time.sleep(random.randint(1, 3))
