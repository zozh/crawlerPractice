from selenium import webdriver
import time

options = webdriver.ChromeOptions()

# 忽略无用的日志,解决谷歌试图读取usb的bug
options.add_experimental_option("excludeSwitches",
                                ['enable-automation', 'enable-logging'])
driver = webdriver.Chrome(
    chrome_options=options,
    executable_path='chromedriver_win32\chromedriver.exe')
# TODO 滑块处理


def login(username: str, password: str):
    url = 'https://login.taobao.com/member/login.jhtml'
    driver.get(url)
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(
        password)
    driver.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()
    time.sleep(10)


if __name__ == '__main__':
    login('123', '123')
