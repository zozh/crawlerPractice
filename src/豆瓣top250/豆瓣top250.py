# coding: utf8
# import os
import re
import bs4
import time
# import json
import queue
import random
import pymongo
import requests
# import crawlerGet
import threading
import configuration
from bs4 import BeautifulSoup
# from library import directory, only_name
# from concurrent.futures import ThreadPoolExecutor

# def get_html_obj(url: str) -> str:
#     # 测试http网站 httpbin.org
#     # 构建headers，模拟真实浏览器，防418
#     # 同一ip多次爬虫,会超时
#     headers = {'user-agent': ua_info()}
#     try:
#         html_obj = requests.get(url=url, headers=headers, timeout=3)
#     except requests.exceptions.ConnectionError as e:
#         print('Error', e.args)
#     return html_obj

# def get_html(url: str):
#     """返回html文本，utf8格式。

#     Args:
#         url (str): html url
#     """
#     html_obj = get_html_obj(url)
#     return html_obj.text


def get_ua():
    """返回随机用户代理"""
    ua_headers = [
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    ]
    headers = {'user-agent': random.choice(ua_headers)}
    return headers


def get_ip():
    """获取快代理ip
    """
    api_url = configuration.api_url
    proxy_ip = requests.get(api_url).text
    username = configuration.username
    password = configuration.password
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {
            "user": username,
            "pwd": password,
            "proxy": proxy_ip
        }
    }
    return proxies


def do_crawler(urls: queue.Queue, html_queue: queue.Queue):
    while True:
        url = urls.get()
        proxies = get_ip()
        headers = get_ua()
        try:
            html_obj = requests.get(url=url,
                                    headers=headers,
                                    proxies=proxies,
                                    timeout=3)
        except requests.exceptions.ConnectionError as e:
            print('Error', e.args)
        html_queue.put(html_obj.text)
        time.sleep(random.randint(1, 3))


def do_parse(html_queue: queue.Queue):
    while True:
        html_doc = html_queue.get()
        soup = BeautifulSoup(html_doc, 'lxml')
        items = soup.find_all("div", "item")
        for each in items:
            data = dict()
            # 图片 序号
            div_pic = each.find("div", class_="pic")
            data["serialNum"] = div_pic.em.string
            data["photo"] = div_pic.img.get("src")
            # 标题 详情
            div_title = each.find("div", class_="hd")
            data["details"] = div_title.a.get("href")
            data["title"] = div_title.a.span.string
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

            try:
                data["inq"] = each.find("span", class_="inq").string
            except:
                data["inq"] = "..."
                data["each"] = str(each)
                # data["find"] = each.find("span", class_="inq")
                print(data["serialNum"])
                print("***********")
                print(each)
                print("***********")
            # 导演 主演
            text = each.find("div", class_="bd").p
            text_list = list()
            for txt in text.strings:
                txt = re.sub('\s', ' ', txt)
                text_list.append(txt)
            print(text_list)
            print("============")
            try:
                temp = re.findall("导演:(.*)(主演:|主)(.*)", str(text_list[0]))
                print(temp)
                print("============")
                major_text = list(temp)[0]
                data["director"] = major_text[0].strip()
                data["starring"] = major_text[2].strip()
            except:
                temp = re.findall("导演:(.*)", str(text_list[0]))
                print(temp)
                print("============")
                major_text = list(temp)[0]
                data["director"] = major_text[0].strip()
                data["starring"] = "..."
            # print(temp)
            # print("============")
            # major_text = list(temp)[0]
            # print(major_text)
            # print("============")
            # data["director"] = major_text[0].strip()
            # data["starring"] = major_text[2].strip()
            # 时间 地点 类型
            other_text = re.findall("(.*)/(.*)/(.*)", str(text_list[1]))[0]
            print(other_text)
            print("============")
            data["year"] = other_text[0]
            data["countries"] = other_text[1].strip()
            data["film_type"] = other_text[2].strip()
            # print(data)
            # text = each.find("div", class_="bd").p.string
            # # print(text)
            # text = re.findall("导演:(.*)(主演:|主)(.*)\n", text)
            # # 详情页面获取导演主演
            # # time.sleep(1)
            # # html_doc = get_html(data["details"])
            # # soup = BeautifulSoup(html_doc, 'lxml')
            # # # 导演
            # # director = soup.select("#info > span:nth-child(1) > span.attrs")[0]
            # # director_list = list()
            # # for director_each in director.contents:
            # #     if isinstance(director_each, bs4.element.Tag):
            # #         director_list.append(director_each.string)
            # # # 主演
            # # starring = soup.select("#info > span.actor > span.attrs")[0]
            # # starring_list = list()
            # # for starring_each in starring.contents:
            # #     if isinstance(starring_each, bs4.element.Tag):
            # #         starring_list.append(starring_each.string)
            # data["director"] = text[0]
            # data["starring"] = text[1]
            # # 时间 地点 类型
            # data["year"] = re.findall("\d{4}", text)[0]
            # text = ''.join(text.split())
            # text = text.split("/")
            # data["countries"] = text[-2]
            # data["film_type"] = text[-1]
            # 保存数据
            # mongoDB数据库,批量操作性能优于频繁操作,可以列表先存着一次解决.
            # 如果全部都拷贝给一个列表保存,那么必须使用深拷贝,但使用深拷贝会栈溢出
            # data_temp = copy.deepcopy(data)
            # sql_data_list.append(data_temp)
            mongoDB(data)


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
# 获取TOP 250 图片 序号 导演 主演 标题 详情 评分 打分人数 简介 时间 地点 类型
if __name__ == '__main__':
    # data_parse()
    url_list = [
        f"https://movie.douban.com/top250?start={page}"
        for page in range(0, 275, 25)
    ]
    url_queue = queue.Queue()
    html_queue = queue.Queue()

    for url in url_list:
        url_queue.put(url)

    for idx in range(4):
        t = threading.Thread(target=do_crawler, args=(url_queue, html_queue))
        t.start()

    for idx in range(7):
        t = threading.Thread(target=do_parse, args=(html_queue, ))
        t.start()