'''
cron: 22 10 * * *
new Env('日产智联');
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

body_list = ['打卡', '不错', '非常棒', '非常不错', '赞一个', '好', '可以哦', '永远的经典', '加油！', '优秀', '赞', '内容不错，欢迎回访', '看上去不错。', '漂亮', '不错不错', '挺好', '点赞', '好车值得拥有']

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

def sign():
    print("\n【【【【【【【签到】】】】】】】\n")
    url = 'https://oneapph5.dongfeng-nissan.com.cn/mb-gw/vmsp-me/ly/busicen/member/reward/pointsreturn/memberPointsRechargetRequestSign'
    noncestr = generate_random_string()
    requestId = generate_random_string()
    timestamp = (int(time.time() * 1000))
    headers = headers_new(noncestr, timestamp)
    data = {
        'version': '202304',
        "requestId":requestId
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    print(result['msg'])

def like():
    print("\n【【【【【【【点赞】】】】】】】\n")
    noncestr = generate_random_string()
    timestamp = (int(time.time() * 1000))
    headers = headers_new(noncestr, timestamp)
    data = {}
    id_list, _ = new_list()
    for i in range(3):
        id = id_list.pop(0)
        url = f'https://oneapph5.dongfeng-nissan.com.cn/mb-gw/dndc-gateway/community/api/v2/feeds/{id}/like'
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
#        print(result)
        print(f"点赞{id}：{result['msg']}")
        if i < 2:
            random_sleep(2, 5)

def comments():
    print("\n【【【【【【【评论】】】】】】】\n")
    url = 'https://oneapph5.dongfeng-nissan.com.cn/mb-gw/dndc-gateway/community/api/v2/comments'
    noncestr = generate_random_string()
    timestamp = (int(time.time() * 1000))
    headers = headers_new(noncestr, timestamp)
    commentable_id_list, _ = new_list()
    success_count = 0 # 记录成功次数
    total_count = 0   # 记录总共尝试次数
    while success_count < 3 and total_count < 6:
        commentable_id = commentable_id_list.pop(5)
        data = {
            "commentable_type": "feeds",
            "commentable_id": commentable_id,
            "body": random.choice(body_list)
        }
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
#        print(result)
        if '评论成功' in result['msg']:
            success_count += 1
        print(f"评论{commentable_id}：{result['msg']}")
        total_count += 1
        if success_count < 3 and total_count < 6:
            random_sleep(60, 80)

def followings():
    print("\n【【【【【【【关注】】】】】】】\n")
    _, user_id = new_list()
    url = f'https://oneapph5.dongfeng-nissan.com.cn/mb-gw/dndc-gateway/community/api/v2/user/followings/{user_id}'
    noncestr = generate_random_string()
    timestamp = (int(time.time() * 1000))
    headers = headers_new(noncestr, timestamp)
    data = {}
    response = requests.put(url, headers=headers, json=data)
    result = response.json()
#    print(result)
    print(f"关注{user_id}：{result['msg']}")

def feedtopics():
    print("\n【【【【【【【入圈】】】】】】】\n")
    id = topics()
    url = f'https://oneapph5.dongfeng-nissan.com.cn/mb-gw/dndc-gateway/community/api/v2/user/feed-topics/{id}'
    noncestr = generate_random_string()
    timestamp = (int(time.time() * 1000))
    headers = headers_new(noncestr, timestamp)
    data = {}
    response = requests.put(url, headers=headers, json=data)
    result = response.json()
#    print(result)
    print(f"入圈{id}：{result['msg']}")

def remain():
#    print("\n【【【【查询抽奖次数】】】】\n")
    url = 'https://oneapph5.dongfeng-nissan.com.cn/mb-gw/vmsp-me/rest/business-service/point/draw/remain'
    noncestr = generate_random_string()
    timestamp = (int(time.time() * 1000))
    headers = headers_new(noncestr, timestamp)
    response = requests.get(url, headers=headers)
    result = response.json()
#    print(result)
#    print(f"可抽奖次数：{result['rows']['remain']}")
    return result['rows']['remain']

def info():
    print("\n【【【【【【【查询】】】】】】】\n")
    url = 'https://oneapph5.dongfeng-nissan.com.cn/mb-gw/dfn-growth/rest/ly-mp-growth-service/ly/mgs/rights/info'
    noncestr = generate_random_string()
    timestamp = (int(time.time() * 1000))
    headers = headers_new(noncestr, timestamp)
    data = {
        "isReminder": "0",
        "channel": "1",
        "networkType": "3",
        "brandCode": "1"
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
#    print(result)
    remains = remain()
    user_info = f"{new_Phone}：{result['data']['cardUserPoint']}积分，{remains}抽奖次数\n"
    print(user_info)
    return user_info

def new_list():
    print("【遍历最新帖子】")
    url = 'https://oneapph5.dongfeng-nissan.com.cn/mb-gw/dndc-gateway/community/api/v2/feeds/new_list'
    noncestr = generate_random_string()
    timestamp = (int(time.time() * 1000))
    headers = headers_new(noncestr, timestamp)
    params = {
        'dt': '22081212C',
        'os': 'Android',
        'device_brand': 'Redmi',
        'os_version': '12',
        'limit': '20',
        'use_volc': '1',
        'page': '1',
        'clientVersion': '2.2.8'
    }
    response = requests.get(url, params=params, headers=headers)
    result = response.json()
#    print(result)
    share_web_url_list = []
    id_list = []#帖子id，点赞、评论任务
    user_id_list = []#用户id，关注任务
    for item in result['rows']['rows']:
        share_web_url_list.append(item['share_web_url'])
        user_id_list.append(item['user_id'])
    for item in share_web_url_list:
        id = item.split('=')[-1]
        id_list.append(id)
    return id_list, random.choice(user_id_list)

#城市圈，车型圈，兴趣圈，大咖圈
def topics():
    print("【遍历圈子】")
    url_list = ['https://oneapph5.dongfeng-nissan.com.cn/mb-gw/dndc-gateway/community/api/v2/feed/topics?limit=50&page=1&category_id=9', 'https://oneapph5.dongfeng-nissan.com.cn/mb-gw/dndc-gateway/community/api/v2/feed/topics?limit=50&page=1&category_id=5', 'https://oneapph5.dongfeng-nissan.com.cn/mb-gw/dndc-gateway/community/api/v2/feed/topics?limit=50&page=1&category_id=4', 'https://oneapph5.dongfeng-nissan.com.cn/mb-gw/dndc-gateway/community/api/v2/feed/topics?limit=20&page=1&category_id=10']
    noncestr = generate_random_string()
    timestamp = (int(time.time() * 1000))
    headers = headers_new(noncestr, timestamp)
    id_list = []
    for url in url_list:
        response = requests.get(url, headers=headers)
        result = response.json()
#        print(result)
        for row in result["rows"]["rows"]:
            if row["followers_audit"] == 0:
                id_list.append(row["id"])
#    print(id_list)
    return random.choice(id_list)
    
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
        sign()
        like()
        comments()
        followings()
        feedtopics()
        msg += info()
        print(f"第{index + 1}个账号运行完成\n")
        index += 1
        if index < len(quantity):
            random_sleep(120, 240)
#    print(msg)
    send('日产智联', msg)