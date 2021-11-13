# coding=utf-8
import json
import os

from chardet.universaldetector import UniversalDetector

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
    """结构化txt转换成json文件,每行生成一个json文件

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


if __name__ == '__main__':
    txt_to_json("project\ip.txt")
