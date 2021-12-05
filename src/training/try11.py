import requests
import hadToClimb
import save
from lxml import etree


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


# <a href="https://downsc.chinaz.net/Files/DownLoad/psd1/202111/psd33417.rar" target="_blank">福建电信下载</a>
rar = get_data(
    'https://downsc.chinaz.net/Files/DownLoad/psd1/202111/psd33417.rar'
).content
print(type(rar))
