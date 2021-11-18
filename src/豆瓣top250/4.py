import bs4
import re
import time
import json
from bs4 import BeautifulSoup
from 豆瓣top250 import get_html

txt = str()
with open(r'src\豆瓣top250\text.html', 'r', encoding='utf-8') as f:
    txt = f.read()
soup = BeautifulSoup(txt, 'lxml')
items = soup.find_all("div", "item")
count = int()
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
        director = soup.select("#info > span:nth-child(1) > span.attrs")[0]
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