# 爬取三国演义全本
import requests
import hadToClimb
import json
from bs4 import BeautifulSoup
import bs4


def get_data(url):
    # url = 'https://www.shicimingju.com//book//sanguoyanyi.html'
    headers = hadToClimb.get_ua()
    res = requests.get(url=url, headers=headers)
    res.encoding = "utf8"
    return res.text


txt = get_data('https://www.shicimingju.com//book//sanguoyanyi.html')
soup = BeautifulSoup(txt, 'lxml')
box = soup.find("div", class_="book-mulu")
a_list = list()
title_list = list()
for each in box.ul.contents:
    if isinstance(each, bs4.element.Tag):
        a_list.append('https://www.shicimingju.com/' + each.a.get('href'))
        title_list.append(each.string)
dictionary = dict(zip(title_list, a_list))
for title, a in dictionary.items():
    text = get_data(dictionary[title])
    text_soup = BeautifulSoup(text, 'lxml')
    box = text_soup.find("div", class_="chapter_content")
    if isinstance(box, bs4.element.Tag):
        dictionary[title] = box.text
with open('txt.json', 'w', encoding='utf8') as f:
    f.write(json.dumps(dictionary, indent=4, ensure_ascii=False))
