# 爬取58二手防房源
# 标题//*[@id="global"]/table/tbody//td/a
import requests
import hadToClimb
import save
from lxml import etree

url = 'https://www.58.com/ershoufang/'
header = hadToClimb.get_ua()
res = requests.get(url=url, headers=header)
save.save_html(res.text)
parsing = etree.HTML(res.text)
li_list = parsing.xpath('//*[@id="global"]//table//td/a/text()')
print(li_list)
