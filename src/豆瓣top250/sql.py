import pymongo
#1.连接本地数据库服务
connection = pymongo.MongoClient('localhost')
database = 'crawler'
collection = 'doubanT250'
#2.连接本地数据库 demo。没有会创建
db = connection[database]
#3.创建集合
emp = db[collection]
#根据情况清空所有数据
# emp.remove(None)
find_condition = {'inq': '...'}
find_result_cursor = emp.find(find_condition)
for find_result in find_result_cursor:
    print(find_result["each"])
    print()