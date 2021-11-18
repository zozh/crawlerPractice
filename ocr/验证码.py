#引入截图软件，获取文件到本地端,并识别图片文字，最后打包
import keyboard  #控制键盘
from PIL import ImageGrab  #保存图片
import time
from aip import AipOcr
""" 你的 APPID AK SK """
APP_ID = '25184094'
API_KEY = '71S5xOvjNs3R7zLkj8hp3cVt'
SECRET_KEY = '1iNWgI3npqlVB7NO4b2u3nCGzllMv5nG'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def baiduOcr(img_path: str):
    """调用百度ocr文本识别

    Args:
        img_path (str): 图片路径
    """
    with open(img_path, 'rb') as fp:
        image = fp.read()
        text_list = client.basicAccurate(image)['words_result']
        for text in text_list:
            print(text['words'])