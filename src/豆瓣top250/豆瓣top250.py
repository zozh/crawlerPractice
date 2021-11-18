# coding: utf8
import datetime
import json
import os
import re
import time
import bs4
import requests
from bs4 import BeautifulSoup
from ua_pool import ua_info


def get_html_obj(url: str) -> str:
    # 测试http网站 httpbin.org
    # 构建headers，模拟真实浏览器，防418
    headers = {'user-agent': ua_info()}
    try:
        html_obj = requests.get(url=url, headers=headers, timeout=1)
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


def print_file(item: object):
    """打印输出到文件
    """
    f = open("project\log.txt", "w", encoding="utf-8")
    print(item, file=f)


def text():
    count = int()
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
            # div_information = each.find("div", class_="bd")
            # text = div_information.p.get_text()
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
            with open(r'src\豆瓣top250\json\a' + str(count) + '.json',
                      'w',
                      encoding='utf-8') as f:
                # 设置不转换成ascii  json字符串首缩进
                json_data = json.dumps(data, ensure_ascii=False, indent=2)
                f.write(json_data)
                count += 1
    # count = int()
    # for i in range(10):
    #     url = "https://movie.douban.com/top250" + "?start=" + str(i * 25)
    #     html_doc = get_html(url)
    #     time.sleep(3)
    #     # 解析界面主题
    #     soup_temp = BeautifulSoup(html_doc, 'lxml')
    #     content = soup_temp.find("div", class_="article")
    #     content_soup = BeautifulSoup(str(content), 'lxml')
    #     # 保存数据

    #     # 图片
    #     img_data = list()
    #     div_img = content_soup.find_all("div", class_="pic")
    #     for each in div_img:
    #         img_data.append(each.img.get("src"))
    #         # data["photo"] = each.img.get("src")
    #         # 下载图片
    #         # download_img(each.img.get("src"))
    #     # 标题 详情
    #     details_data = list()
    #     title_data = list()
    #     div_title = content_soup.find_all("div", class_="hd")
    #     for each in div_title:
    #         details_data.append(each.a.get("href"))
    #         title_data.append(each.a.span.string)
    #         # data["details"] = each.a.get("href")
    #         # data["title"] = each.a.span.string
    #     # 导演 主演 时间 地点 类型
    #     div_information = content_soup.find_all("div", class_="bd")
    #     director_data = list()
    #     starring_data = list()
    #     year_data = list()
    #     countries_data = list()
    #     film_type_data = list()
    #     for each in div_information:
    #         text = each.p.get_text()
    #         # print("=======")
    #         # print(text)
    #         # print("=======")
    #         temp_list = re.findall("导演:(.*)主演:(.*).", text)
    #         # 部分导演过长,主演无法捕获,引发报错
    #         try:
    #             temp_list = list(temp_list[0])
    #             # 去除数据中的'\xa0\xa0\xa0\xa'
    #             temp_list[0] = "".join(temp_list[0].split())
    #             temp_list[1] = "".join(temp_list[1].split())
    #             director_data.append(temp_list[0])
    #             starring_data.append(temp_list[1])
    #             # data["director"] = temp_list[0]
    #             # data["starring"] = temp_list[1]
    #         except:
    #             time.sleep(1)
    #             # 去详情页爬取
    #             # html_doc = get_html(data["details"])
    #             html_doc = get_html(details_data[-1])
    #             soup = BeautifulSoup(html_doc, 'lxml')
    #             director = soup.select(
    #                 "#info > span:nth-child(1) > span.attrs")[0]
    #             director_list = list()
    #             for each in director.contents:
    #                 if isinstance(each, bs4.element.Tag):
    #                     director_list.append(each.string)
    #             director_data.append(director_list.append(each.string))
    #             starring = soup.select("#info > span.actor > span.attrs")[0]
    #             starring_list = list()
    #             for each in starring.contents:
    #                 if isinstance(each, bs4.element.Tag):
    #                     starring_list.append(each.string)
    #             starring_data.append(starring_list)
    #         year_data.append(re.findall("\d{4}", text)[0])
    #         # data["year"] = re.findall("\d{4}", text)[0]
    #         text = ''.join(text.split())
    #         text = text.split("/")
    #         countries_data.append(text[-2])
    #         film_type_data.append(text[-1])
    #         # data["countries"] = text[-2]
    #         # data["film_type"] = text[-1]
    #     # 评价
    #     # 获取大块后遍历
    #     temp_list = list()
    #     div_star_temp = content_soup.find_all("div", class_="star")
    #     div_star = BeautifulSoup(repr(div_star_temp), 'lxml')
    #     star_data = list()
    #     starNum_data = list()
    #     for each in div_star.span.next_siblings:
    #         if isinstance(each, bs4.element.Tag):
    #             # print("=======")
    #             # print(each.string)
    #             # print("=======")
    #             temp_list.append(each.string)
    #     # 去除评价人数的中文,只留数字
    #     temp_list[2] = re.sub('[\u4e00-\u9fa5]', '', temp_list[2])
    #     star_data.append(temp_list[0])
    #     starNum_data.append(temp_list[2])
    #     # data["star"] = temp_list[0]
    #     # data["starNum"] = temp_list[2]
    #     # 简介
    #     inq_data = list()
    #     inq = content_soup.find_all("span", "inq")
    #     for each in inq:
    #         inq_data.append(each.string)
    #         # data["inq"] = each.string
    # # 字典转换成json 存入本地文件

    #     data = dict()
    #     with open(r'src\豆瓣top250\json\a' + str(count) + '.json',
    #               'a',
    #               encoding='utf-8') as f:
    #         # 设置不转换成ascii  json字符串首缩进
    #         json_data = json.dumps(data, ensure_ascii=False, indent=2)
    #         f.write(json_data)
    #         count += 1


# 获取TOP 250 电影的英文名、港台名、导演、主演、上映年份、电影分类以及评分。
if __name__ == '__main__':
    text()
