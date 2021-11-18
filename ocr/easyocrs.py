# 导入easyocr
import easyocr
# 创建reader对象
# this needs to run only once to load the model into memory
reader = easyocr.Reader(['sin', 'en'])
# 读取图像
result = reader.readtext('code.jpg')
# 结果
result