# 导入requests请求库
import requests
import pymongo

# mongo步骤
# 获取Database 和 Collection
# CURD
mongo_client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
#判断是否连接成功
if mongo_client.server_info() == None:
    raise RuntimeError("数据库连接失败")
database = 'crawler'
collection = 'ipAgent'
mongo_db = mongo_client[database]
mongo_collection = mongo_db[collection]

# 要访问的网址
url = 'http://httpbin.org/get'
# 填入代理IP和端口
proxy = '39.155.253.58:8060'
# 构造完整的代理链接(url)
proxies = {
    # HTTP协议的完整url
    # 格式：协议+IP+目录
    'http': 'http://' + proxy,
    # HTTPS协议简单来说就是HTTP协议的安全版
    'https': 'https://' + proxy,
}
# proxies参数设置代理
rsp = requests.get(url, proxies=proxies)
print(rsp.text)