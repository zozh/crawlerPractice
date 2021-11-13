from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


# 初始化
def init():
    # 定义为全局变量，方便其他模块使用
    global url, browser, username, password, wait
    # 登录界面的url
    url = 'https://passport.bilibili.com/login'
    # 实例化一个chrome浏览器
    browser = webdriver.Chrome()
    # 用户名
    username = '***********'
    # 密码
    password = '***********'
    # 设置等待超时
    wait = WebDriverWait(browser, 20)


from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# 登录
def login():
    # 打开登录页面
    browser.get(url)
    # 获取用户名输入框
    user = wait.until(EC.presence_of_element_located(
        (By.ID, 'login-username')))
    # 获取密码输入框
    passwd = wait.until(EC.presence_of_element_located(
        (By.ID, 'login-passwd')))
    # 输入用户名
    user.send_keys(username)
    # 输入密码
    passwd.send_keys(password)


from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import re
from PIL import Image


# 获取图片信息
def get_image_info(img):
    '''
    :param img: (Str)想要获取的图片类型：带缺口、原始
    :return: 该图片(Image)、位置信息(List)
    '''

    # 将网页源码转化为能被解析的lxml格式
    soup = BeautifulSoup(browser.page_source, 'lxml')
    # 获取验证图片的所有组成片标签
    imgs = soup.find_all('div', {'class': 'gt_cut_' + img + '_slice'})
    # 用正则提取缺口的小图片的url，并替换后缀
    img_url = re.findall('url\(\"(.*)\"\);',
                         imgs[0].get('style'))[0].replace('webp', 'jpg')
    # 使用urlretrieve()方法根据url下载缺口图片对象
    urlretrieve(url=img_url, filename=img + '.jpg')
    # 生成缺口图片对象
    image = Image.open(img + '.jpg')
    # 获取组成他们的小图片的位置信息
    position = get_position(imgs)
    # 返回图片对象及其位置信息
    return image, position


# 获取小图片位置
def get_position(img):
    '''
    :param img: (List)存放多个小图片的标签
    :return: (List)每个小图片的位置信息
    '''

    img_position = []
    for small_img in img:
        position = {}
        # 获取每个小图片的横坐标
        position['x'] = int(
            re.findall('background-position: (.*)px (.*)px;',
                       small_img.get('style'))[0][0])
        # 获取每个小图片的纵坐标
        position['y'] = int(
            re.findall('background-position: (.*)px (.*)px;',
                       small_img.get('style'))[0][1])
        img_position.append(position)
    return img_position


from PIL import Image


# 裁剪图片
def Corp(image, position):
    '''
    :param image:(Image)被裁剪的图片
    :param position: (List)该图片的位置信息
    :return: (List)存放裁剪后的每个图片信息
    '''

    # 第一行图片信息
    first_line_img = []
    # 第二行图片信息
    second_line_img = []
    for pos in position:
        if pos['y'] == -58:
            first_line_img.append(
                image.crop((abs(pos['x']), 58, abs(pos['x']) + 10, 116)))
        if pos['y'] == 0:
            second_line_img.append(
                image.crop((abs(pos['x']), 0, abs(pos['x']) + 10, 58)))
    return first_line_img, second_line_img


# 拼接大图
def put_imgs_together(first_line_img, second_line_img, img_name):
    '''
    :param first_line_img: (List)第一行图片位置信息
    :param second_line_img: (List)第二行图片信息
    :return: (Image)拼接后的正确顺序的图片
    '''

    # 新建一个图片，new()第一个参数是颜色模式，第二个是图片尺寸
    image = Image.new('RGB', (260, 116))
    # 初始化偏移量为0
    offset = 0
    # 拼接第一行
    for img in first_line_img:
        # past()方法进行粘贴，第一个参数是被粘对象，第二个是粘贴位置
        image.paste(img, (offset, 0))
        # 偏移量对应增加移动到下一个图片位置,size[0]表示图片宽度
        offset += img.size[0]
    # 偏移量重置为0
    x_offset = 0
    # 拼接第二行
    for img in second_line_img:
        # past()方法进行粘贴，第一个参数是被粘对象，第二个是粘贴位置
        image.paste(img, (x_offset, 58))
        # 偏移量对应增加移动到下一个图片位置，size[0]表示图片宽度
        x_offset += img.size[0]
    # 保存图片
    image.save(img_name)
    # 返回图片对象
    return image