import os
import json
import random
import datetime
import pymongo
import redis


class mongoDB:
    def __init__(
        self,
        database: str,
        collection: str,
        conn: str = 'localhost',
    ) -> None:
        self.connection = pymongo.MongoClient(conn)
        self.db = self.connection[database]
        self.emp = self.db[collection]

    def create(self, data):
        if isinstance(data, dict):
            self.emp.insert_one(data)
        elif isinstance(data, list):
            self.emp.insert_many(data)
        else:
            raise TypeError("传入类型错误,期待dict或list")

    def delete_library_to_run_road(self):
        """删库跑路
        """
        #清空所有数据
        self.emp.remove(None)


class Redis():
    def __init__(self, host: str = '127.0.0.1', port: int = 6379, db: int = 0):
        self.conn = redis.Redis(host, port, db)


def directory(path: str):
    """查找目录存在返回,否创建

    Args:
        path (str): 目录路径
    """
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def save_html(content: str):
    """保存html

    Args:
        content (str): html字符串
    """

    file_path = os.path.join(
        directory('data\\html-data') + '\\' + only_name() + ".html")
    with open(file_path, 'w', encoding='utf-8') as file_obj:
        file_obj.write(content)


def only_name():
    """返回名字"""
    now_time = datetime.datetime.now().strftime("%Y-%m-%d, %H-%M-%S,")
    random_code = str(random.randint(0, 300000))
    return now_time + random_code


def save_json(data: dict, name: str):
    """字典数据保存到本地,并存数据库

    Args:
        sql_data (list): 数据字典
    """
    file_path = os.path.join(
        directory('data\\json-data') + '\\' + only_name() + ".json")
    with open(file_path, 'w', encoding='utf-8') as f:
        # 设置不转换成ascii  json字符串首缩进
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        f.write(json_data)


def sava_photo(content: bytes):
    """下载图片

    Args:
        content (bytes): 二进制数据
    """
    # 以二进制的方式下载图片
    file_path = os.path.join(
        directory('data\\photo-data') + '\\' + only_name() + ".jpg")
    with open(file_path, 'wb') as f:
        f.write(content)


def save_file(content, suffix: str, folder: str = 'data//'):
    """下载文件

    Args:
        content (str|bytes): 目标文件数据
        suffix (str): 文件后缀
        folder (str, optional): 文件存放目录,默认:'data//'.
    """
    if suffix.find('.') == -1:
        suffix = '.' + suffix
    if folder.find('/') == -1:
        folder = folder + '//'
    file_path = os.path.join(directory(folder) + only_name() + suffix)
    if isinstance(content, str):
        with open(file_path, 'w', encoding='utf8') as f:
            f.write(content)
    elif isinstance(content, bytes):
        with open(file_path, 'wb', encoding='utf8') as f:
            f.write(content)
    else:
        raise ValueError("类型错误，期待str或bytes")
