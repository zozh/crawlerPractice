# 获取前5页短租房源的名称、价格、评价数量、房屋类型、床数量和房客数量
#第一步，导入selenium模块的webdrivier包
from selenium import webdriver
#第二步，调用webdriver包的Chrome类，返回chrome浏览器对象
driver = webdriver.Chrome(
    executable_path='chromedriver_win32\chromedriver.exe')
#第三步，如使用浏览器一样开始对网站进行访问
#设置等待3秒后打开目标网页
driver.implicitly_wait(3)
url = "http://zh.airbnb.com/s/Shenzhen--China/homes"
driver.get(url)
# 找到盒子
# $$('._10ejfg4u > div > div > a')
content_box = driver.find_elements_by_css_selector(
    '._10ejfg4u > div > div > a')
for each in content_box:
    # 找到评论数量
    # $$('._1dir9an > div:nth-child(3) > div > div:nth-child(1) > div > span > span')
    try:
        comment = each.find_element_by_css_selector(
            '._1dir9an > div:nth-child(3) > div > div:nth-child(1) > div > span > span'
        )
        comment = comment.text
        evaluation = comment.split("·")[0]
        evaluation_number_of_people = comment.split("·")[1]
    except:
        comment = 0
    # 找到价格
    # $$('._1orel7j7 > div > span:nth-child(2)')
    price = each.find_element_by_css_selector(
        '._1orel7j7 > div > span:nth-child(2)')
    price = price.text.replace("每晚", "").replace("价格", "").replace("\n", "")
    # 找到名称
    # $$('._1dir9an > div:nth-child(2) > div > div')
    name = each.find_element_by_css_selector(
        '._1dir9an > div:nth-child(2) > div > div')
    name = name.text
    # 找到房屋类型，大小
    # $$('._1dir9an > div:nth-child(1) > div > div > span > span')
    details = each.find_element_by_css_selector(
        '._1dir9an > div:nth-child(1) > div > div > span > span')
    details = details.text
    house_type = details.split(" · ")[0]
    bed_number = details.split(" · ")[1]
    print(comment, price, name, house_type, bed_number)
    # print(comment, name, house_type, bed_number)
