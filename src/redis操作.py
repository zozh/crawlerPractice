#!/usr/bin/env python
#encoding: utf-8

import redis
# 连接redis,decode_responses=True返回字符串不再是二进制的
r = redis.Redis(host="127.0.0.1", port=6379, db=0, decode_responses=True)

#查看当前数据库大小
print('dbsize: %s' % r.dbsize())

#ping查询
print('ping %s' % r.ping())

# 存数据 string类型
r.set('tao_627', '35')
# 读数据
print(r.get('tao_627'))

r.set('age', '20')
print(r.get('age'))

r.set('sex', 'male')
print(r.get('sex'))
# 获取所有键
keys = r.keys()
print(keys)
# 删除age键
r.delete("age")
# 删除所有键 慎用
# r.delete(*keys)

print(r.get('sex'))
print(r.get('age'))
print(r.get('tao_627'))
