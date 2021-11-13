# coding: utf8
import os
import random
import time
import datetime
import requests
from urllib import error
from bs4 import BeautifulSoup


def ua_info():
    """返回随机用户代理"""
    ua_headers = {
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
    }
    return random.choice(list(ua_headers))


def get_html_obj(url: str) -> str:
    # 测试http网站 httpbin.org
    # 构建headers，模拟真实浏览器，防418
    headers = {'user-agent': ua_info()}
    try:
        html_obj = requests.get(url=url, headers=headers, timeout=1)
    except error.HTTPError as e:
        print(e.code)
    except error.URLError as e:
        print(e.reason)
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


def directory(path: str):
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


# 图片,影片名字,导演,主演,时间,国家类型,评分，多少人评价,简介
def parse_html_doc(html_doc: str):
    soup = BeautifulSoup(html_doc, 'html.parser')
    print(soup.find_all("div", class_="item"))


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


def print_file(item: object):
    f = open("project\log.txt", "w", encoding="utf-8")
    print(item, file=f)


def text():
    for i in range(10):
        url = "https://movie.douban.com/top250" + "?start=" + str(i * 25)
        html_doc = get_html(url)
        time.sleep(1)
        # 解析界面
        # TODO 导演评价无法解析
        soup = BeautifulSoup(html_doc, 'lxml')
        # 图片
        div_img = soup.find_all("div", class_="pic")
        for each in div_img:
            download_img(each.img.get("src"))
        # 标题
        div_title = soup.find_all("div", class_="hd")
        for each in div_title:
            print(each.a.span.string)
        # 导演主演
        div_information = soup.find_all("div", class_="bd")
        for each in div_information:
            print(each.p.string)
        # 评价
        div_star = soup.find_all("div", class_="star")
        for each in div_star:
            print(each.span.string)
        # 简介
        inq = soup.find_all("span", "inq")
        for each in inq:
            print(each.string)


# 获取TOP 250电影的英文名、港台名、导演、主演、上映年份、电影分类以及评分。
if __name__ == '__main__':
    text()
