import json
from library import eachFile
from pymongo import MongoClient


class Mongo:
    def __init__(self, conn: str = 'localhost') -> None:
        self.connection = MongoClient(conn)
        self.db = None
        self.emp = None

    def use_database(self, database: str):
        self.db = self.connection[database]

    def use_collection(self, collection: str):
        if self.db == None:
            raise ValueError("未指定数据库")
        self.emp = self.db[collection]

    def operate(self, operate: str, **statement):
        """根据操作分发任务

        Args:
            operate (str): 操作
        """
        self.operation_book = {
            "C": self.create_document,
            "R": "Retrieve",
            "U": "Update",
            "D": "Delete"
        }
        implement = self.operation_book.get(operate, "选项错误,期待C,R,U,D")
        implement(statement)

    def create_document(self, info):
        print(info)
        if self.emp == None:
            raise ValueError("未指定集合")
        if isinstance(info, dict):
            self.emp.insert_one(info)
        elif isinstance(info, list):
            self.emp.insert_many(info)
        else:
            raise TypeError("类型不匹配，期待dict或list")


def main():
    #1.连接本地数据库服务
    connection = MongoClient('localhost')
    database = 'crawler'
    collection = 'ipAgent'
    #2.连接本地数据库 demo。没有会创建
    db = connection[database]
    #3.创建集合
    emp = db[collection]
    #根据情况清空所有数据
    emp.remove(None)

    for name in eachFile("project\json"):
        #4.打开外部文件
        file = open(name, 'r', encoding="utf-8")
        for each in file:
            eachline = json.loads(each)
            emp.insert(eachline)
        file.close()


if __name__ == '__main__':
    mongo = Mongo()
    mongo.use_database("try")
    mongo.use_collection("try")
    info = {"name": 1, "operate": "C", "num": "one"}
    # date={"data":info}
    mongo.operate("C", date=info)
