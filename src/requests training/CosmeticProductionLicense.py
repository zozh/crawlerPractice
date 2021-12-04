# coding=utf-8
# 获取化妆品生产许可详情
import requests
import hadToClimb
import json
import save
import random
import time


# 50页之后 数据异常
def post_data(data: dict, save_json: bool = False):
    url = 'http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList'
    data = data
    res = requests.post(url=url, headers=hadToClimb.get_ua(), data=data)
    json_data = json.loads(res.text)
    print(json_data)
    return json_data


# conditionType 1 许可证编号 2 企业名称 3 社会信用代码
# productName 查询关键字
data = {
    'on': "true",
    'page': 1,
    'pageSize': 15,
    'page': 1,
    'productName': '',
    'conditionType': 1,
    'applyname': '',
    'applysn': '',
}
# 第一次获取总页数
json_data = post_data(data)
pageCount = json_data['pageCount']
# 通过索引与总页数做对比
mongoDB = save.mongoDB('try', 'cosmetics')
while data['page'] <= pageCount:
    data['page'] += 1
    json_data = post_data(data)
    list_data = json_data['list']
    mongoDB.create(list_data)
    print(data['page'])
    time.sleep(random.randint(1, 3))