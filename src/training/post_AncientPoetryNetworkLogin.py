import requests
import hadToClimb
from bs4 import BeautifulSoup

url = 'https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx'
headers = hadToClimb.get_ua()

# 获取隐藏域的值 viewstate viewstategenerator
response = requests.get(url=url, headers=headers)
content = response.text
soup = BeautifulSoup(content, 'lxml')
viewstate = soup.select('#__VIEWSTATE')[0].attrs.get('value')
viewstategenerator = soup.select('#__VIEWSTATEGENERATOR')[0].attrs.get('value')

# 验证码处理
code = soup.select('#imgCode')[0].attrs.get('src')
code_url = 'https://so.gushiwen.cn' + code
# 为什么不用requests.get()而是用requests.session()。
# requests.get()没错调用都会重开session对象
# requests.session()会重用session对象
session = requests.session()
response_code = session.get(code_url)
content_code = response_code.content
with open('code.jpg', 'wb') as fp:
    fp.write(content_code)
code_name = hadToClimb.baiduOcr("code.jpg")

# 点击登陆
url_post = 'https://so.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fso.gushiwen.cn%2fuser%2fcollect.aspx'
data_post = {
    '__VIEWSTATE': viewstate,
    '__VIEWSTATEGENERATOR': viewstategenerator,
    'from': 'http://so.gushiwen.cn/user/collect.aspx',
    'email': '595165358@qq.com',
    'pwd': 'action',
    'code': code_name,
    'denglu': '登录',
}
response_post = session.post(url=url, headers=headers, data=data_post)
content_post = response_post.text
with open('gushiwen.html', 'w', encoding=' utf-8') as fp:
    fp.write(content_post)
