import bs4
from bs4 import BeautifulSoup

txt = """
<div id="info">
    <span>
        <span class="pl">导演</span>:
        <span class="attrs">
            <a href="/celebrity/1001404/" rel="v:directedBy">奥利维埃·纳卡什</a> /
            <a href="/celebrity/1010884/" rel="v:directedBy">埃里克·托莱达诺</a>
        </span>
    </span>
    <br>
    <span>
        <span class="pl">编剧</span>:
        <span class="attrs">
            <a href="/celebrity/1001404/">奥利维埃·纳卡什</a>
            / <a href="/celebrity/1010884/">埃里克·托莱达诺</a>
        </span>
    </span>
    <br>
    <span class="actor">
        <span class="pl">主演</span>:
        <span class="attrs">
            <a href="/celebrity/1050210/" rel="v:starring">弗朗索瓦·克鲁塞</a> /
            <a href="/celebrity/1220507/" rel="v:starring">奥玛·希</a> /
            <a href="/celebrity/1289597/" rel="v:starring">安娜·勒尼</a> /
            <a href="/celebrity/1317872/" rel="v:starring">奥德雷·弗勒罗</a> /
            <a href="/celebrity/1318339/" rel="v:starring">托马·索利韦尔</a>
        </span>
    </span>
    <br>
    <span class="pl">类型:</span>
    <span property="v:genre">剧情</span> /
    <span property="v:genre">喜剧</span>
    <br>
    <span class="pl">制片国家/地区:</span>
    法国
    <br>
    <span class="pl">语言:</span>
    法语
    <br>
    <span class="pl">上映日期:</span>
    <span property="v:initialReleaseDate" content="2011-11-02(法国)">2011-11-02(法国)</span>
    <br>
    <span class="pl">片长:</span>
    <span property="v:runtime" content="112">112分钟</span>
    <br>
    <span class="pl">又名:</span>
    闪亮人生(港) / 逆转人生(台) / 无法触碰 / 最佳拍档 / 不可触碰 / 不可触摸 / Untouchable / The Intouchables
    <br>
    <span class="pl">IMDb:</span>
    tt1675434
    <br>
</div>
"""
soup = BeautifulSoup(txt, 'lxml')
out1 = list()
out2 = list()
director = soup.select("#info > span:nth-child(1) > span.attrs")[0]
for each in director.contents:
    if isinstance(each, bs4.element.Tag):
        out1.append(each.string)
starring = soup.select("#info > span.actor > span.attrs")[0]
for each in starring.contents:
    if isinstance(each, bs4.element.Tag):
        out2.append(each.string)
print(out1)
print(out2)
# print(soup.select("#info > span:nth-child(1) > span.attrs"))
# print(soup.select("#info > span.actor > span.attrs"))