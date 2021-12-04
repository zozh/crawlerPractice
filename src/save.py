import pymongo


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
