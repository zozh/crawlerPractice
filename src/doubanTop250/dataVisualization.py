import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymongo


def histogram(data: list, xlabel: str, ylabel: str, title: str):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    fix, ax = plt.subplots()
    ax.hist(data, 20)  #载入数据
    ax.set_xlabel(xlabel)  #设置X轴标签
    ax.set_ylabel(ylabel)  #设置Y轴标签
    ax.set_title(title)  #设置直方图名称
    plt.show()


client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
db = client['crawler']
collection = db['doubanT250']
find_condition = {'star': '9.5'}

star = list()
year = list()
for result in collection.find():
    star.append(float(result['star']))
    year.append(int(result['year']))
# 可视化 评分 年龄 柱形图
histogram(star, "评分", "数量", "评分直方图")

histogram(year, "年份", "数量", "年份直方图")
