import bs4
from bs4 import BeautifulSoup

txt = """
<div class="hd">
    <a href="https://movie.douban.com/subject/6786002/" class="">
        <span class="title">触不可及</span>
        <span class="title">&nbsp;/&nbsp;Intouchables</span>
        <span class="other">&nbsp;/&nbsp;闪亮人生(港) / 逆转人生(台)</span>
    </a>
    <span class="playable">[可播放]</span>
</div>
"""
soup = BeautifulSoup(txt, 'lxml')
print(soup.a.get("href"))