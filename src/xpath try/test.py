import os
from lxml import etree
# 谷歌浏览器开发者里的源码并非网页真实的源码，而是经过谷歌修改过的源码。检查页面源码获得真实源码
filePath = r'src\xpath try\html.html'
with open(filePath, 'r', encoding='utf8') as f:
    text = f.read()
xpath = '//*[@id="main"]/div/div[3]/div[3]/a[2]/@class'
parsing = etree.HTML(text)
li_list = parsing.xpath(xpath)
print(li_list)