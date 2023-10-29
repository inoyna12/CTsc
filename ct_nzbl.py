'''
cron: 16 8 * * *
new Env('哪吒汽车遍历');
'''
import requests
import json
import random
import time
import datetime
import hashlib
import uuid
from sendNotify import send
from utils.ql_api import get_envs, put_envs

appVersion = "5.6.1"
appKey = 'e0ae89fb37b6151889c6de3ba6b84e0d3a67f52cd5767758d4186fefff8f763c'#headers参数
sign_string = '8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'

def generate_random_uuid():
    random_uuid = str(uuid.uuid4())
    return random_uuid

def random_sleep(min_val, max_val):
    num = random.randint(min_val, max_val)
    print(f"等待{num}秒后继续>>>>>>>>>>>")
    time.sleep(num)

def generate_random_number():
    random_number = ''.join(random.choices('0123456789', k=10))
    return random_number

def sha256_encode(string):
    hash_object = hashlib.sha256(string.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig


def toutiao_loadmore():
    print("【遍历头条翻页】")
    createTime_index = 0
    random_number = random.randint(700, 1000)
    uuid = generate_random_uuid()
    print(uuid, random_number)
    url = f'https://appapi-pki.chehezhi.cn/hznz/app_article/common/article/rec/list?refreshType=loadmore&category=toutiao&uuid={uuid}'
    for i in range(100):
        print(f"第{i + 1}次请求")
        nonce = generate_random_number()
        timestamp = int(time.time() * 1000)
        sign = f'GET%2Fhznz%2Fapp_article%2Fcommon%2Farticle%2Frec%2Flistappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}refreshtype%3Dloadmorecategory%3Dtoutiaouuid%3D{uuid}{sign_string}'
        headers = {
            'appId': 'HOZON-B-xKrgEvMt',
            'appKey': appKey,
            'appVersion': appVersion,
            'login_channel': '1',
            'channel': 'android',
            'nonce': str(nonce),
            'phoneModel': 'Redmi 22081212C',
            'timestamp': str(timestamp),
            'sign': sha256_encode(sign),
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 12; zh-cn; 22081212C Build/SKQ1.220303.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
            'Host': 'appapi-pki.chehezhi.cn:18443',
            'Connection': 'Keep-Alive'
        }
        try:
            response = requests.get(url=url, headers=headers, timeout=20)
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.RequestException as e:
            print("请求异常:", e)
            random_sleep(10, 20)
        except json.JSONDecodeError as e:
            print("JSON 解码异常:", e)
            random_sleep(10, 20)
        except Exception as e:
            print("其他异常:", e)
            random_sleep(10, 20)
        else:
            if 'data' not in result:
                print("result中不存在data键值")
                random_sleep(20, 40)
                continue
            elif len(result['data']) == 0:
                print(result)
                return
            for item in result['data']:
                print(f"发帖时间：{item['volcExtra']['createTime']}，评论数量：{item['commentCount']}")
                if item['commentCount'] >= 10:
                    if item['article']['openId'] not in toutiao_openId_list:
                        toutiao_openId_list.append(item['article']['openId'])
                    else:
                        createTime_index += 1
                        print("已存在，不进行加入")
                else:
                    print("评论数量小于10，不进行加入")
            print(f"toutiao_openId_list数量：{len(toutiao_openId_list)}")
            if len(toutiao_openId_list) > random_number or createTime_index >= 5:
                return
            random_sleep(10, 20)

def toutiao_open():
    print("【遍历头条首页】")
    uuid = generate_random_uuid()
    url = f'https://appapi-pki.chehezhi.cn/hznz/app_article/common/article/rec/list?refreshType=open&category=toutiao&uuid={uuid}'
    print(uuid)
    nonce = generate_random_number()
    timestamp = int(time.time() * 1000)
    sign = f'GET%2Fhznz%2Fapp_article%2Fcommon%2Farticle%2Frec%2Flistappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}refreshtype%3Dopencategory%3Dtoutiaouuid%3D{uuid}{sign_string}'
    headers = {
        'appId': 'HOZON-B-xKrgEvMt',
        'appKey': appKey,
        'appVersion': appVersion,
        'login_channel': '1',
        'channel': 'android',
        'nonce': str(nonce),
        'phoneModel': 'Redmi 22081212C',
        'timestamp': str(timestamp),
        'sign': sha256_encode(sign),
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 12; zh-cn; 22081212C Build/SKQ1.220303.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
        'Host': 'appapi-pki.chehezhi.cn:18443',
        'Connection': 'Keep-Alive'
    }
    try:
        response = requests.get(url=url, headers=headers, timeout=20)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        print("请求异常:", e)
        random_sleep(10, 20)
    except json.JSONDecodeError as e:
        print("JSON 解码异常:", e)
        random_sleep(10, 20)
    except Exception as e:
        print("其他异常:", e)
        random_sleep(10, 20)
    else:
        print(result['message'])

#爬取小圈   
def xiaoquan_loadmore():
    print("【遍历小圈翻页】")
    data_index = 0
    createTime_index = 0
    random_number = random.randint(200, 300)
    print(random_number)
    uuid = generate_random_uuid()
    print(uuid)
    for i in range(50):
        print(f"第{i + 1}次请求")
        url = f'https://appapi-pki.chehezhi.cn/hznz/app_article/common/article/rec/list?refreshType=loadmore&category=xiaoquan&uuid={uuid}'
        nonce = generate_random_number()
        timestamp = int(time.time() * 1000)
        sign = f'GET%2Fhznz%2Fapp_article%2Fcommon%2Farticle%2Frec%2Flistappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}refreshtype%3Dloadmorecategory%3Dxiaoquanuuid%3D{uuid}{sign_string}'#小圈下滑刷新
        headers = {
            'appId': 'HOZON-B-xKrgEvMt',
            'appKey': appKey,
            'appVersion': appVersion,
            'login_channel': '1',
            'channel': 'android',
            'nonce': str(nonce),
            'phoneModel': 'Redmi 22081212C',
            'timestamp': str(timestamp),
            'sign': sha256_encode(sign),
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 12; zh-cn; 22081212C Build/SKQ1.220303.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
            'Host': 'appapi-pki.chehezhi.cn:18443',
            'Connection': 'Keep-Alive'
        }
        try:
            response = requests.get(url=url, headers=headers, timeout=20)
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.RequestException as e:
            print("请求异常:", e)
            random_sleep(10, 20)
        except json.JSONDecodeError as e:
            print("JSON 解码异常:", e)
            random_sleep(10, 20)
        except Exception as e:
            print("其他异常:", e)
            random_sleep(10, 20)
        else:
            if 'data' not in result:
                random_sleep(20, 40)
                continue
            elif len(result['data']) == 0:
                data_index += 1
                print(result)
            for item in result['data']:
                print(f"发帖时间：{item['volcExtra']['createTime']}")
                if item['article']['openId'] not in xiaoquan_openId_list:
                    xiaoquan_openId_list.append(item['article']['openId'])
                else:
                    createTime_index += 1
                    print("已存在，不进行加入")
            print(f"xiaoquan_openId_list数量：{len(xiaoquan_openId_list)}")
            if len(xiaoquan_openId_list) > random_number or createTime_index > 20 or data_index > 5:
                break
            random_sleep(10, 20)
    print(f"xiaoquan_openId_list数量：{len(xiaoquan_openId_list)}")
      
if __name__ == '__main__':
    title_name = '哪吒汽车遍历'
    tt = 'toutiao_openId_list'
    xq = 'xiaoquan_openId_list'
    toutiao_openId_list = []
    xiaoquan_openId_list = []
    toutiao_open()
    toutiao_loadmore()
    xiaoquan_loadmore()
    put_envs(get_envs(tt)[0].get('id'), tt, '\n'.join(toutiao_openId_list))
    put_envs(get_envs(xq)[0].get('id'), xq, '\n'.join(xiaoquan_openId_list))
    send(title_name, f"头条数量：{len(toutiao_openId_list)}\n小圈数量：{len(xiaoquan_openId_list)}")
