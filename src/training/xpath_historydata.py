import requests
import hadToClimb
import save
from lxml import etree

url = 'https://www.aqistudy.cn/historydata/'
xpath = '//div[3]//div//div//div//a/text()'
header = hadToClimb.get_ua()
res = requests.get(url=url, headers=header)
save.save_html(res.text)
parsing = etree.HTML(res.text)
li_list = parsing.xpath(xpath)
print(li_list)
