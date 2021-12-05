import random
import requests
from aip import AipOcr
# 配置文件
import config
import json


def get_ua():
    """返回随机用户代理"""
    ua_headers = []
    with open(r"src\user_agents.json", "r", encoding="utf-8") as f:
        txt = f.read()
        ua_headers = json.loads(txt)["ua_list"]
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