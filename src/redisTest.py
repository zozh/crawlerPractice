import redis
import json
import random

r = redis.Redis(host="127.0.0.1", port=6379, db=0, decode_responses=True)
for i in range(100):
    r.sadd(
        "test",
        '{"serialNum":' + str(random.randint(1, 5)) + '}',
    )
lists = list(r.smembers("test"))
lists = list(map(lambda each: json.loads(each), lists))
print(lists)