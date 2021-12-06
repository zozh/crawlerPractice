from selenium import webdriver
import time

options = webdriver.ChromeOptions()

# 忽略无用的日志,解决谷歌试图读取usb的bug
options.add_experimental_option("excludeSwitches",
                                ['enable-automation', 'enable-logging'])
bro = webdriver.Chrome(chrome_options=options,
                       executable_path='chromedriver_win32\chromedriver.exe')
url = 'http://scxk.nmpa.gov.cn:81/xk/'
bro.get(url)
time.sleep(2)
txt = bro.page_source
print(txt)
time.sleep(100)
