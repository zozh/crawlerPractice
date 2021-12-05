import requests
import hadToClimb
import save
from lxml import etree


# TODO 被反爬
# 下载站长素材 psd
def get_data(url: str) -> object:
    """返回Response对象

    Args:
        url (str): [description]

    Returns:
        [type]: [description]
    """
    header = hadToClimb.get_ua()
    res = requests.get(url=url, headers=header)
    return res


def do_parsing(text: str, xpath: str) -> list:
    """返回xpath解析结果

    Args:
        text (str): 目标文本
        xpath (str): xpath表达式
    """
    parsing = etree.HTML(res.text)
    li_list = parsing.xpath(xpath)
    return li_list


url = 'https://sc.chinaz.com/psd/'
xpath = '//*[@id="container"]/div/a/@href'

res = get_data(url)
save.save_html(res.text)
a_list = do_parsing(res.text, xpath)
a_list = ['https:' + i for i in a_list]

xpath = '//*[@id="down"]/div[2]//li/a/@href'
for each in a_list:
    print(each)
    html = get_data(each).text
    save.save_file(html, 'html')
    download = do_parsing(html, xpath)
    rar = get_data(download).content
    save.save_file(rar, 'rar')
