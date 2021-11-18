# coding: utf8
import os
import re
import bs4
import time
import json
import random
import pymongo
import requests
from bs4 import BeautifulSoup
from ua_pool import ua_info
from library import directory, only_name


def get_html_obj(url: str) -> str:
    # 测试http网站 httpbin.org
    # 构建headers，模拟真实浏览器，防418
    # 同一ip多次爬虫,会超时
    headers = {'user-agent': ua_info()}
    try:
        html_obj = requests.get(url=url, headers=headers, timeout=3)
    except:
        pass
    return html_obj


def get_html(url: str):
    """返回html文本，utf8格式。

    Args:
        url (str): html url
    """
    html_obj = get_html_obj(url)
    return html_obj.text


def download_img(img_url: str, img_path: str = None):
    """下载图片

    Args:
        img_url (str): 图片链接
        img_path (str): 保存路径，默认工作路径
    """
    # 拼接路径
    suffix = os.path.splitext(os.path.basename(img_url))[1]
    if img_path == None:
        img_path = os.path.join(directory(os.getcwd() + "\\img"),
                                only_name() + suffix)
    # 获取响应
    requests_obj = get_html_obj(img_url)
    # 保存图片
    if (requests_obj.status_code == requests.codes.ok):
        with open(img_path, 'wb') as file_obj:
            file_obj.write(requests_obj.content)
    return img_path


def text():

    for i in range(10):
        url = "https://movie.douban.com/top250" + "?start=" + str(i * 25)
        time.sleep(3)
        html_doc = get_html(url)
        soup = BeautifulSoup(html_doc, 'lxml')
        items = soup.find_all("div", "item")

        for each in items:
            data = dict()
            # 图片
            data["photo"] = each.find("div", class_="pic").img.get("src")
            # 标题 详情
            div_title = each.find("div", class_="hd")
            data["details"] = div_title.a.get("href")
            data["title"] = div_title.a.span.string
            # 导演 主演
            text = each.find("div", class_="bd").p.get_text()
            temp_list = re.findall("导演:(.*)主演:(.*).", text)
            # 部分导演过长,主演无法捕获,引发报错
            try:
                temp_list[0] = "".join(temp_list[0].split())
                temp_list[1] = "".join(temp_list[1].split())
                data["director"] = temp_list[0]
                data["starring"] = temp_list[1]
            # 去详情页爬取
            except:
                time.sleep(1)
                html_doc = get_html(data["details"])
                soup = BeautifulSoup(html_doc, 'lxml')
                # 导演
                director = soup.select(
                    "#info > span:nth-child(1) > span.attrs")[0]
                director_list = list()
                for director_each in director.contents:
                    if isinstance(director_each, bs4.element.Tag):
                        director_list.append(director_each.string)
                # 主演
                starring = soup.select("#info > span.actor > span.attrs")[0]
                starring_list = list()
                for starring_each in starring.contents:
                    if isinstance(starring_each, bs4.element.Tag):
                        starring_list.append(starring_each.string)
                data["director"] = director_list
                data["starring"] = starring_list
            # 时间 地点 类型
            data["year"] = re.findall("\d{4}", text)[0]
            text = ''.join(text.split())
            text = text.split("/")
            data["countries"] = text[-2]
            data["film_type"] = text[-1]
            # 获取大块后遍历
            temp_list = list()
            div_star = each.find("div", class_="star")
            for star_each in div_star.span.next_siblings:
                if isinstance(star_each, bs4.element.Tag):
                    temp_list.append(star_each.string)
            # 去除评价人数的中文,只留数字
            temp_list[2] = re.sub('[\u4e00-\u9fa5]', '', temp_list[2])
            data["star"] = temp_list[0]
            data["starNum"] = temp_list[2]
            # 简介
            data["inq"] = each.find("span", class_="inq").string
            # 保存数据
            save_json(data)
            # mongoDB数据库,批量操作性能优于频繁操作,可以列表先存着一次解决.
            # 如果全部都拷贝给一个列表保存,那么必须使用深拷贝,但使用深拷贝会栈溢出
            # data_temp = copy.deepcopy(data)
            # sql_data_list.append(data_temp)
            mongoDB(data)


def save_json(data: dict):
    """字典数据保存到本地,并存数据库

    Args:
        sql_data (list): 数据字典
    """
    with open(r'src\豆瓣top250\json\a' + str(random.randint(0, 1000)) + '.json',
              'w',
              encoding='utf-8') as f:
        # 设置不转换成ascii  json字符串首缩进
        json_data = json.dumps(data, ensure_ascii=False, indent=2)
        f.write(json_data)


def mongoDB(sql_data: list):
    """数据保存到mongoDB

    Args:
        sql_data (list): 数据
    """
    #1.连接本地数据库服务
    connection = pymongo.MongoClient('localhost')
    database = 'crawler'
    collection = 'doubanT250'
    #2.连接本地数据库 demo。没有会创建
    db = connection[database]
    #3.创建集合
    emp = db[collection]
    emp.insert_one(sql_data)
    connection.close()


# TODO 测试
# 获取TOP 250 图片 导演 主演 标题 详情 评分 打分人数 简介 时间 地点 类型
if __name__ == '__main__':
    text()