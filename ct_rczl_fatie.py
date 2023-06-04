'''
cron: 0,1,2,3 0 * * *
new Env('日产智联发帖');
'''
#变量填写 手机号&token&算法助手里sha512加密的最后37位，37位中最后4位是手机尾号，这37位应该是跟账号绑定不会变的

import requests
import os
import json
import time
import random
import string
import hashlib
from sendNotify import send
from os import environ

def headers_new(noncestr, timestamp):
    sign = sha512_encode(f"nissanapp{timestamp}{token}{noncestr}{token_sha512}")
    headers = {
        'appVersion': '2.2.8',
        'clientid': 'nissanapp',
        'Accept': 'application/json',
        'sign': sign,
        'range': '1',
        'noncestr': f"{noncestr}",
        'token': token,
        'From-Type': '2',
        'appSkin': 'NISSANAPP',
        'appcode': 'nissan',
        'timestamp': f"{timestamp}",
        'channelCode': 'N_ariya_as_0013',
        'Host' :'oneapph5.dongfeng-nissan.com.cn',
        'Content-Type': 'application/json',
        'User-Agent': 'okhttp/3.12.0',
        'Connection': 'Keep-Alive'
    }
    return headers

def feeds():
    print("\n【【【【【【【发帖】】】】】】】\n")
    url = 'https://oneapph5.dongfeng-nissan.com.cn/mb-gw/dndc-gateway/community/api/v2/feeds'
    noncestr = generate_random_string()
    timestamp = (int(time.time() * 1000))
    headers = headers_new(noncestr, timestamp)
    title, content = tianhang_api()
    data = {
        "feed_mark": f"{timestamp}",
        "feed_title": title,
        "themes": [],
        "feeds_type": 2,
        "feed_from": 2,
        "app_feed_content": [
            {
                "content": {"height": 0, "text": contents, "width": 0},
                "type": 1
            }
        ]
    }
    print(f"标题：{title}\n内容：{content}")
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
#    print(result)
    msg = f"{new_Phone}：{result['msg']}"
    print(msg)
    return msg

def tianhang_api():
    key = 'df2f1255dbccfadd606cf04d66aae277'
    url = f'https://apis.tianapi.com/lzmy/index?key={key}'
    response = requests.get(url=url)
    result = response.json()
#    print(result)
    title = result['result']['saying']
    content = result['result']['transl']
#    print(title, content)
    return title, content

def tianhang_api_sentence():
    apikey = 'df2f1255dbccfadd606cf04d66aae277'
    url = f'https://apis.tianapi.com/sentence/index?key={apikey}'#精美句子
    response = requests.get(url=url)
    result = response.json()
    return result['result']['content']
   
def random_sleep(min_val, max_val):
    num = random.randint(min_val, max_val)
    print(f"等待{num}秒后继续>>>>>>>>>>>")
    time.sleep(num)  

def sha512_encode(string):
    sha512 = hashlib.sha512()
    sha512.update(string.encode('utf-8'))
    result = sha512.hexdigest()
    return result

def generate_random_string(length=32):
    mix = string.ascii_lowercase + string.digits
    rand_str = ''.join(random.sample(mix, length))
    return rand_str

def ql_env():
    if "rczltoken" in os.environ:
        token_list = os.environ['rczltoken'].split('\n')
        if len(token_list) > 0:
            return token_list
        else:
            print("变量未启用")
            sys.exit(1)
    else:
        print("未添加变量")
        sys.exit(0)

if __name__ == '__main__':
    msg = ""
    index = 0
    quantity = ql_env()
    print (f"共找到{len(quantity)}个账号")
    for token_new in quantity:
        Phone = token_new.split('&')[0]
        token = token_new.split('&')[1]
        token_sha512 = token_new.split('&')[2]
        new_Phone = Phone[:3] + "****" + Phone[7:]
        print (f"------------正在执行第{index + 1}个账号----------------")
        msg += f"第{index + 1}个账号运行结果: \n"
        msg += feeds()
        print(f"第{index + 1}个账号运行完成\n")
        index += 1
        if index < len(quantity):
            random_sleep(120, 240)
#    print(msg)
    send('日产智联发帖', msg)