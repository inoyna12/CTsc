'''
cron: 36 9,12,14 * * *
new Env('哪吒汽车fffff');
'''
import requests
import json
import random
import time
import datetime
import hashlib
import uuid
import fcntl
import sys
import os

appVersion = "5.5.1"
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

def ql_env(name):
    if name in os.environ:
        token_list = os.environ[name].split('\n')
        if len(token_list) > 0:
            return token_list
        else:
            print("变量未启用" + name)
            sys.exit(1)
    else:
        print("未添加变量" + name)
        sys.exit(0)

def refresh_Authorization():
    url = 'https://appapi-pki.chehezhi.cn/customer/account/info/refreshApiToken'
    for i in range(50):
        now = datetime.datetime.now()
        formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
        nonce = generate_random_number()
        timestamp = int(time.time() * 1000)
        sign = f"POST%2Fcustomer%2Faccount%2Finfo%2FrefreshApiTokenappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}refreshtoken%3A{account_dict['refresh_token']}{sign_string}"
        headers = {
            "Authorization": account_dict['refresh_token'],
            "appId": "HOZON-B-xKrgEvMt",
            "appKey": appKey,
            "appVersion": appVersion,
            'login_channel': '1',
            'channel': 'android',
            "nonce": str(nonce),
            "phoneModel": "Redmi 22081212C",
            "timestamp": str(timestamp),
            "sign": sha256_encode(sign),
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "appapi-pki.chehezhi.cn:18443"
        }
        data = {
            "refreshToken": account_dict['refresh_token']
        }
        try:
            response = requests.post(url=url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.RequestException as e:
            print("请求异常:", e)
            random_sleep(30, 50)
        except json.JSONDecodeError as e:
            print("JSON 解码异常:", e)
            random_sleep(30, 50)
        except Exception as e:
            print("其他异常:", e)
            random_sleep(30, 50)
        else:
            if "code" in result and result['code'] == 20000:
                print("刷新Authorization成功")
                global Authorization
                Authorization = result['data']['access_token']
                account_dict['access_token'] = result['data']['access_token']
                account_dict['refresh_token'] = result['data']['refresh_token']
                account_dict['token_time'] = str(formatted_time)
                return
            else:
                print("刷新Authorization失败")
                print(result)
    return None

def getCustomer():
    print("【【【【【【【查询】】】】】】】")
    url = 'https://appapi-pki.chehezhi.cn/hznz/customer/getCustomer'
    for i in range(5):
        nonce = generate_random_number()
        timestamp = int(time.time() * 1000)
        sign = f'GET%2Fhznz%2Fcustomer%2FgetCustomerappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}{sign_string}'
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
            'Authorization': f"Bearer {Authorization}",
            'Host': 'appapi-pki.chehezhi.cn:18443',
            'Connection': 'Keep-Alive'
        }
        try:
            response = requests.get(url=url, headers=headers, timeout=10)
            result = response.json()
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("请求异常:", e)
            random_sleep(20, 40)
        except json.JSONDecodeError as e:
            print("JSON 解码异常:", e)
            random_sleep(20, 40)
        except Exception as e:
            print("其他异常:", e)
            random_sleep(20, 40)
        else:
            creditScore = result['data']['creditScore']
            phone = result['data']['phone']
            account_dict['mobile'] = phone
            account_dict['creditScore'] = creditScore
            user_info = f"{phone}：{creditScore}积分"
            print(user_info)
            return
    print(result)
    return None
    
if __name__ == '__main__':
    index = 0
    filepath = "/ql/data/env/nzqc.json"
    aaaa = ql_env('aaaa')
    print(f"共找到{len(aaaa)}个账号")
    with open(filepath, 'r') as f:
        info_new = json.load(f)
    print(f"共找到{len(info_new)}个账号")
    for refreshToken in aaaa:
        print(f"\n{'-' * 13}正在执行第{index + 1}个账号{'-' * 13}")
        account_dict = {
            "mobile": None,
            "refresh_token": refreshToken,
            "access_token": None,
            "token_time": None,
            "sign": False,
            "share": 0,
            "comment": 0,
            "creditScore": 0,
            "reserve": None,
            "reserve2": None
        }
        refresh_Authorization()
        getCustomer()
        print(account_dict)
        info_new.append(account_dict)
        index += 1
        if index < len(aaaa):
            random_sleep(1, 100)
    with open(filepath, 'w') as f:
        json.dump(info_new, f)
    print(f"共找到{len(info_new)}个账号")
