import os
import random
import datetime


def directory(path: str):
    """查找目录存在返回,否创建

    Args:
        path (str): 目录路径
    """
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def save_sql():
    pass


def save_html(content: str):
    file_path = os.path.join("project\\html-data\\", only_name() + ".html")
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
    with open(r'src\豆瓣top250\json\a' + name + '.json', 'w',
              encoding='utf-8') as f:
        # 设置不转换成ascii  json字符串首缩进
        json_data = json.dumps(data, ensure_ascii=False, indent=2)
        f.write(json_data)


def print_file(item: object):
    """打印输出到文件
    """
    f = open("project\log.txt", "w", encoding="utf-8")
    print(item, file=f)