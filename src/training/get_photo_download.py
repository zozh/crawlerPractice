# 下载糗事百科图片
import requests
import hadToClimb
import time
from bs4 import BeautifulSoup

url = 'https://www.qiushibaike.com/imgrank/'
img_list = list()
headers = hadToClimb.get_ua()
res = requests.get(url=url, headers=headers)
soup = BeautifulSoup(res.text, 'lxml')
photos = soup.find_all("div", class_="thumb")
for photo in photos:
    img_list.append('http:' + photo.a.img.get('src'))
for each in img_list:
    html = requests.get(url=each, headers=headers)
    with open(str(time.time()) + '.jpg', 'wb') as f:
        f.write(html.content)