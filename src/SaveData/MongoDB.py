import pymongo
from methodRelationship import sequential_call
from library import judge_type


class Mongo:
    def __init__(self, conn: str = 'localhost') -> None:
        self.connection = pymongo.MongoClient(conn)
        self.db = None
        self.emp = None

    @sequential_call()
    def use_database(self, database: str):
        """选择数据库

        Args:
            database (str): 数据库名称
        """
        self.db = self.connection[database]

    @sequential_call("use_database")
    def use_collection(self, collection: str):
        """选择集合

        Args:
            collection (str): 集合名称
        """
        # if self.db == None:
        #     raise ValueError("未指定数据库")
        self.emp = self.db[collection]

    @sequential_call("use_collection")
    def operating_statement(self, operate: str, **statement):
        """接收操作

        Args:
            operate (str): 操作
        """
        if operate in ("C", "R", "U", "D"):
            self.parameter_checking(operate, **statement)
        else:
            raise ValueError("选项错误,期待C,R,U,D")

    def parameter_checking(self, operate: str, **statement):
        """检查参数并分发

        Args:
            operate (str): 操作
        """
        # 检查字典有无值,值的类型
        print(statement)

        if operate == "C":
            if "data" in statement:
                if isinstance(statement["data"], dict):
                    self.__create_document(statement["data"])
                elif isinstance(statement["data"], list):
                    if judge_type(statement["data"], dict):
                        self.__create_document(statement["data"], "many")
            else:
                raise ValueError("创建操作参数错误,期待'data',dict类型创建一个,list类型创建多个")
        elif operate == "R":
            pass
        elif operate == "U":
            pass
        elif operate == "D":
            if "conditions" in statement and "number" in statement:
                if isinstance(statement["conditions"], dict) and isinstance(
                        statement["number"], str):
                    self.__delete_document(statement["conditions"],
                                           statement["number"])
            else:
                raise ValueError("删除操作参数错误,期待'conditions'和'number'")

    def __create_document(self, info, number: str = "one"):
        """添加文档

        Args:
            info (dict|list[dicts]): dict添加一个,list[dicts]添加多个。
        """
        if number == "one":
            self.emp.insert_one(info)
        elif number == "many":
            self.emp.insert_many(info)
        else:
            raise ValueError("值错误,期待'one'或'many'")

    def __retrieve_document(self):
        pass

    def __update_document(self):
        pass

    def __delete_document(self, conditions: dict, number: str):
        if number == "one":
            self.emp.delete_one(conditions)
        elif number == "many":
            self.emp.delete_many(conditions)
        else:
            raise ValueError("number值错误,期待'one'或'many'")


# def main():
#     #1.连接本地数据库服务
#     connection = MongoClient('localhost')
#     database = 'crawler'
#     collection = 'ipAgent'
#     #2.连接本地数据库 demo。没有会创建
#     db = connection[database]
#     #3.创建集合
#     emp = db[collection]
#     #根据情况清空所有数据
#     emp.remove(None)
#     for name in eachFile("project\json"):
#         #4.打开外部文件
#         file = open(name, 'r', encoding="utf-8")
#         for each in file:
#             eachline = json.loads(each)
#             emp.insert(eachline)
#         file.close()

# 删除查阅 conditions number
# 添加数据 data
# 更新数据 old_data  new_data
if __name__ == '__main__':
    mongo = Mongo()
    mongo.use_database("try")
    mongo.use_collection("try")
    info = {"name": 1, "operate": "C", "num": "one"}
    info2 = {"name": 2, "operate": "C", "num": "one"}
    info3 = {"name": 3, "operate": "C", "num": "one"}
    info_list = [info, info2, info3]
    # mongo.operating_statement("C", data=info)
    mongo.operating_statement("D", conditions={"name": 1}, number="many")
