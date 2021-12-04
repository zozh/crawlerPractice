import random
import requests
from aip import AipOcr
# 配置文件
import config


def get_ua():
    """返回随机用户代理"""
    ua_headers = [
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    ]
    headers = {'user-agent': random.choice(ua_headers)}
    return headers


def get_ip():
    """获取快代理ip
    """
    # 新建config，放入你的api_url username password
    api_url = config.api_url
    proxy_ip = requests.get(api_url).text
    username = config.username
    password = config.password
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {
            "user": username,
            "pwd": password,
            "proxy": proxy_ip
        }
    }
    return proxies


def baiduOcr(img_path: str):
    """调用百度ocr文本识别

    Args:
        img_path (str): 图片路径
    """
    # 新建config，放入你的APP_ID API_KEY SECRET_KEY
    client = AipOcr(config.APP_ID, config.API_KEY, config.SECRET_KEY)
    with open(img_path, 'rb') as fp:
        image = fp.read()
        text_list = client.basicAccurate(image)['words_result']
        for text in text_list:
            # print(text['words'])
            return text['words']