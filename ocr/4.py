import requests
import random

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.56",
}


def get_code():
    url = "http://icode.renren.com/getcode.do?t=web_login&rnd={}".format(
        random.random())
    # 使用random.random()格式化url地址
    res = requests.get(url, headers=headers)

    # 保存图片，二进制写入
    with open('code.jpg', 'wb') as fp:
        fp.write(res.content)
        fp.flush()  # 不用回车就往里写
    """
    识别验证码区域代码(待完成)
    """


def login(code):
    # 通过fiddler抓取相关参数和传入参数的地址
    url = "http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=202063121980"
    data = {
        'email': '账号',
        'password': '密码',
        'icode': code,  # 识别出的验证码结果
        'origURL': 'http://www.renren.com/home',
        'domain': 'renren.com',
        'kwy_id': 1,
        'captcha_type': 'web_login',
        'f': 'http://www.renren.com/974712722',  # 跳转地址
    }
    res = session.post(url, headers=headers, data=data)
    # session对象保存了我们登陆后的信息，后期请求个人中心是携带着登陆信息的
    res = res.content.decode()
    print(res)


def get_profile():
    url = "http://www.renren.com/974712722/profile"
    res = session.get(url, headers=headers)
    result = res.content.decode()
    print(result)


if __name__ == '__main__':
    session = requests.session()  # 创建一个session对象存放会话数据
    # 获取验证码图片，交给第三方打码平台进行识别
    code = get_code()
    # 登录
    login(code)
    # 获取个人中心页
    get_profile()
