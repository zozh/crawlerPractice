# # 导演: 弗兰克·德拉邦特 Frank Darabont
# # 主演: 蒂姆·罗宾斯 Tim Robbins
# # 1994 / 美国 /
# # 犯罪 剧情
import re

# txt = "导演: 陈凯歌 Kaige Chen   主演: 张国荣 Leslie Cheung / 张丰毅 Fengyi Zha"
# # ret = re.match("导演:(.*)主演:(.*)//", txt)
# # print(ret.group())
# print(re.findall("导演:(.*)主演:(.*)/", txt))
from bs4 import BeautifulSoup

txt = """
<p class="">
                            导演: 刘镇伟 Jeffrey Lau&nbsp;&nbsp;&nbsp;主演: 周星驰 Stephen Chow / 吴孟达 Man Tat Ng...<br>
                            1995&nbsp;/&nbsp;中国香港 中国大陆&nbsp;/&nbsp;喜剧 爱情 奇幻 古装
                        </p>
"""
# 获取后遍历
out = list()
soup = BeautifulSoup(txt, 'lxml')
text = soup.p.get_text()
print(re.findall("导演:(.*)主演:(.*).", text))
print(re.findall("\d{4}", text))
text = ''.join(text.split())
text = text.split("/")
print(text[-1])
print(text[-2])