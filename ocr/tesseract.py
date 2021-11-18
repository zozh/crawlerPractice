#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytesseract
from PIL import Image

file = r"idencode.png"

# 建议图像识别前，先对图像进行灰度化和 二值化，以提高文本识别率
image = Image.open(file)
Img = image.convert('L')  # 灰度化
#自定义灰度界限，这里可以大于这个值为黑色，小于这个值为白色。threshold可根据实际情况进行调整(最大可为255)。
threshold = 180
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
photo = Img.point(table, '1')  #图片二值化
#保存处理好的图片
newfile = "test1.png"
photo.save(newfile)

image = Image.open(newfile)
# 解析图片，lang='chi_sim'表示识别简体中文，默认为English
# 如果是只识别数字，可再加上参数config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789'
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
content = pytesseract.image_to_string(image, lang='chi_sim')
print(content)