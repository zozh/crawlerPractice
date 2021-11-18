#endcoding: utf-8

# 获取文件的时间属性

# 用到的知识

#   os.getcwd() 方法用于返回当前工作目录

#   os.path.getatime(file) 输出文件访问时间

#   os.path.getctime(file) 输出文件的创建时间

#   os.path.getmtime(file) 输出文件最近修改时间

import time

import os


def fileTime(file):

    return [
        time.ctime(os.path.getatime(file)),
        time.ctime(os.path.getmtime(file)),
        time.ctime(os.path.getctime(file))
    ]


times = fileTime(os.getcwd())

print(times)

print(type(times))