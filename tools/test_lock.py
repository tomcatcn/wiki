# 模拟30个请求
# 发给 http：//127.0.0.1:8000/test
# 发给 http：//127.0.0.1:8001/test

import random
from threading import Thread
import requests

# 随机向8000或8001发请求
def get_request():
    url = 'http://127.0.0.1:8000/test'
    url2 = 'http://127.0.0.1:8000/test'
    get_url = random.choice([url,url2])
    res = requests.get(get_url)
    print('request OK')

t_list = []

for i in range(30):
    t = Thread(target=get_request)
    t_list.append(t)
    t.start()
    print(i)

for t in t_list:
    t.join()


