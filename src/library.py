# coding=utf-8
import os
import json
import random
import datetime
from chardet.universaldetector import UniversalDetector
import requests
import hadToClimb
from lxml import etree


def directory(path: str):
    """查找目录存在返回,否创建

    Args:
        path (str): 目录路径
    """
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def save_html(content: str):
    file_path = os.path.join("html-data\\", only_name() + ".html")
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
        json_data = json.dumps(data, ensure_ascii=False, indent=4)
        f.write(json_data)


def print_file(item: object):
    """打印输出到文件
    """
    f = open("project\log.txt", "w", encoding="utf-8")
    print(item, file=f)


def get_encoding(file_path: str):
    """返回文件编码

    Args:
        file_path (str): 文件路径
    """
    f = open(file_path, 'rb')
    detector = UniversalDetector()
    for line in f:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    return detector.result["encoding"]


def txt_to_json(file_path: str):
    """结构的txt转换成json文件,每行生成一个json文件

    Args:
        file_path (str): 文件路径
    """
    # print(str(datetime.datetime.now()))
    file_name = os.path.splitext(file_path)[0]
    encoding = get_encoding(file_path)
    with open(file_path, "r", encoding=encoding) as f:
        key_list = f.readline().split()
        save_data = dict()
        for line in key_list:
            save_data[line] = []
        count = int()
        long = len(key_list)
        for line in f:
            value_list = line.split()
            if len(value_list) != long:
                print("第{1}行错误".format(count))
                continue
            with open(file_name + str(count) + '.json', 'w',
                      encoding=encoding) as file_obj:
                save_json = dict(zip(key_list, value_list))
                json.dump(save_json, file_obj, ensure_ascii=False)
            count += 1


def get_data(url: str) -> object:
    """返回Response对象

    Args:
        url (str): [description]

    Returns:
        [type]: [description]
    """
    header = hadToClimb.get_ua()
    res = requests.get(url=url, headers=header)
    return res


def do_parsing(text: str, xpath: str) -> list:
    """返回xpath解析结果

    Args:
        text (str): 目标文本
        xpath (str): xpath表达式
    """
    parsing = etree.HTML(text)
    li_list = parsing.xpath(xpath)
    return li_list
