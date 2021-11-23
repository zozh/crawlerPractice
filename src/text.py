import json
import random
import pymongo
import time
#1.连接本地数据库服务
connection = pymongo.MongoClient('localhost')
database = 'try'
collection = 'sqlTry'
#2.连接本地数据库 demo。没有会创建
db = connection[database]
#3.创建集合
emp = db[collection]
for i in range(250 + 1):
    print(emp.find_one({"serialNum": str(i)}))
