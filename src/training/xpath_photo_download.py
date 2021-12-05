import requests
import hadToClimb
import save
from lxml import etree
# 下载图片
url = 'https://www.4klike.com/'
header = hadToClimb.get_ua()
res = requests.get(url=url, headers=header)
save.save_html(res.text)
parsing = etree.HTML(res.text)
img_list = parsing.xpath('//*[@id="main"]/div[5]/ul//a/img/@src')
for each in img_list:
    html = requests.get(url=each, headers=header)
    save.sava_photo(html.content)