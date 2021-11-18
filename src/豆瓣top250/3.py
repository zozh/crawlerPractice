import re
import bs4
from bs4 import BeautifulSoup

txt = """
<div class="star">
    <span class="rating45-t"></span>
    <span class="rating_num" property="v:average">9.1</span>
    <span property="v:best" content="10.0"></span>
    <span>963454人评价</span>
</div>
"""
temp_list = list()
soup = BeautifulSoup(txt, 'lxml')
div_star_temp = soup.find_all("div", class_="star")
div_star = BeautifulSoup(repr(div_star_temp), 'lxml')
for each in div_star.span.next_siblings:
    if isinstance(each, bs4.element.Tag):
        temp_list.append(each.string)
temp_list[2] = re.sub('[\u4e00-\u9fa5]', '', temp_list[2])
print(temp_list)
