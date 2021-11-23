import redis
import json
import random
import pymongo
import time


def run_time(func):
    def wrapper(*args, **kw):
        local_time = time.time()
        func(*args, **kw)
        print('current Function [%s] run time is %.2f' %
              (func.__name__, time.time() - local_time))

    return wrapper


@run_time
def frequent():
    """频繁操作
    """
    for ids in range(100):
        data = {"name": random.randint(0, 100)}
        save_sql(data)


@run_time
def batch():
    """批量操作
    """
    r = redis.Redis(host="127.0.0.1", port=6379, db=0, decode_responses=True)
    for idx in range(100):
        data = {"name": random.randint(0, 100)}
        r.lpush("data_list", json.dumps(data))
    data_list = r.lrange('data_list', 0, -1)
    # 列表内字符串转字典
    data_list = list(map(lambda each: json.loads(each), data_list))
    save_sql(data_list)


def save_sql(data):
    #1.连接本地数据库服务
    connection = pymongo.MongoClient('localhost')
    database = 'try'
    collection = 'sqlTry'
    #2.连接本地数据库 demo。没有会创建
    db = connection[database]
    #3.创建集合
    emp = db[collection]
    if isinstance(data, dict):
        emp.insert_one(data)
    else:
        emp.insert_many(data)
    connection.close()


def delete_library_to_run_road(database: str, collection: str):
    """删库跑路
    """
    connection = pymongo.MongoClient('localhost')
    db = connection[database]
    emp = db[collection]
    #根据情况清空所有数据
    emp.remove(None)
    connection.close()


if __name__ == '__main__':
    delete_library_to_run_road("crawler", "try")
    # frequent()
    # batch()
