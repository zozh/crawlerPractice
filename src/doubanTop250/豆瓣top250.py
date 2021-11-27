# coding: utf8
import re

import bs4
import redis
import time
import json
import queue
import random
import pymongo
import requests
import threading
import config
from bs4 import BeautifulSoup


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
    # 新建configuration，放入你的api_url username password
    api_url = config.api_url
    proxy_ip = requests.get(api_url).text
    username = config.username
    password = config.password
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {
            "user": username,
            "pwd": password,
            "proxy": proxy_ip
        }
    }
    return proxies


def do_crawler(urls: queue.Queue, html_queue: queue.Queue):
    """获取源码

    Args:
        urls (queue.Queue):url队列
        html_queue (queue.Queue): html源码队列
    """
    while True:
        # while urls.qsize() > 0:
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
    """解析

    Args:
        html_queue (queue.Queue):html源码队列
    """

    while True:
        # while urls.qsize() != 0 and html_queue.qsize() != 0:
        html_doc = html_queue.get()
        soup = BeautifulSoup(html_doc, 'lxml')
        items = soup.find_all("div", "item")
        for each in items:
            data = dict()
            # 图片 序号
            div_pic = each.find("div", class_="pic")
            # 转数字,好检查数据
            data["serialNum"] = int(div_pic.em.string)
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
                # data["each"] = str(each)
                # print(data["serialNum"])
            # 导演 主演
            text = each.find("div", class_="bd").p
            text_list = list()
            for txt in text.strings:
                # 去除特殊符号
                txt = re.sub('\s', ' ', txt)
                text_list.append(txt)
            try:
                major_text = list(
                    re.findall("导演:(.*)(主演:|主)(.*)", str(text_list[0])))[0]
                data["starring"] = major_text[2].strip()
            except:
                major_text = list(re.findall("导演:(.*)", str(text_list[0])))[0]
                data["starring"] = "..."
            data["director"] = major_text[0].strip()
            # 时间 地点 类型
            other_text = re.findall("(.*)/(.*)/(.*)", str(text_list[1]))[0]
            # 去空格
            data["year"] = re.sub('\s', ' ', other_text[0])
            data["countries"] = other_text[1].strip()
            data["film_type"] = other_text[2].strip()
            # 连接redis
            r = redis.Redis(host="127.0.0.1",
                            port=6379,
                            db=0,
                            decode_responses=True)
            # redis 缓存会造成冗余
            r.lpush("doubanT250", json.dumps(data, ensure_ascii=False))
        # 去除数据存mongoDB
        data_list = r.lrange("doubanT250", 0, -1)
        data_list = list(map(lambda each: json.loads(each), data_list))
        mongoDB(data_list)
        r.delete("doubanT250")
        data_list.clear()


def save_json(data: dict, name: str):
    """字典数据保存到本地,并存数据库

    Args:
        sql_data (list): 数据字典
    """
    with open(r'src\豆瓣top250\json\a' + name + '.json', 'a',
              encoding='utf-8') as f:
        # 设置不转换成ascii  json字符串首缩进
        json_data = json.dumps(data, ensure_ascii=False, indent=2)
        f.write(json_data)


def mongoDB(data: list):
    """数据保存到mongoDB

    Args:
        sql_data (list): 数据
    """
    #1.连接本地数据库服务
    connection = pymongo.MongoClient('localhost')
    database = 'crawler'
    collection = 'try'
    #2.连接本地数据库 demo。没有会创建
    db = connection[database]
    #3.创建集合
    emp = db[collection]
    try:
        emp.insert_many(data)
    except:
        print(data)
    connection.close()


# TODO 测试
# 获取TOP 250 图片 序号 导演 主演 标题 详情 评分 打分人数 简介 时间 地点 类型
if __name__ == '__main__':
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
