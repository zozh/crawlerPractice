from selenium import webdriver
import time
import random
import hadToClimb


def login(username: str, password: str):
    url = 'https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx'
    driver.get(url)
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="email"]').send_keys(username)
    time.sleep(random.randint(1, 2))
    driver.find_element_by_xpath('//*[@id="pwd"]').send_keys(password)
    time.sleep(random.randint(1, 2))
    # 对验证码截图
    driver.find_element_by_xpath('//*[@id="imgCode"]').screenshot('capts.png')
    code = hadToClimb.baiduOcr('capts.png')
    driver.find_element_by_xpath('//*[@id="code"]').send_keys(code)
    time.sleep(random.randint(1, 2))
    driver.find_element_by_xpath('//*[@id="denglu"]').click()
    time.sleep(100)


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    # 忽略无用的日志,解决谷歌试图读取usb的bug
    options.add_experimental_option("excludeSwitches",
                                    ['enable-automation', 'enable-logging'])
    driver = webdriver.Chrome(
        chrome_options=options,
        executable_path='chromedriver_win32\chromedriver.exe')
    email = '595165358@qq.com'
    pwd = 'action'
    login(email, pwd)
