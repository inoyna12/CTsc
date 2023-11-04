'''
cron: 36 9 * * *
new Env('哪吒汽车');
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
from sendNotify import send
from utils.github_api import update_github_file

appVersion = "5.6.1"
appKey = 'e0ae89fb37b6151889c6de3ba6b84e0d3a67f52cd5767758d4186fefff8f763c'#headers参数
sign_string = '8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'
oneself = ["15050425338", "13291164580", "19941326235"]
fixed_creditScore = 690

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
    for i in range(10):
        now = datetime.datetime.now()
        formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
        nonce = generate_random_number()
        timestamp = int(time.time() * 1000)
        sign = f"POST%2Fcustomer%2Faccount%2Finfo%2FrefreshApiTokenappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}refreshtoken%3A{info['refresh_token']}{sign_string}"
        headers = {
            "Authorization": info['refresh_token'],
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
            "refreshToken": info['refresh_token']
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
                info['access_token'] = result['data']['access_token']
                info['refresh_token'] = result['data']['refresh_token']
                info['token_time'] = str(formatted_time)
                git_token.append(result['data']['refresh_token'])
                return True
            else:
                print("刷新Authorization失败")
                print(result)
                send("刷新Authorization失败", f"账号{index}")
                return False
    send("刷新Authorization失败", f"账号{index}")
    return False
    
#爬头条评论
def traversal_comment():
    print("【遍历评论】")
    for i in range(3):
        articleId = random.choice(toutiao_openId_list)
        url = 'https://api.chehezhi.cn/hznz/app_article/listParentComment'
        headers = {
            'Host': 'api.chehezhi.cn',
            'accept': 'application/json, text/plain, */*',
            'channel': 'h5',
            'user-agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36',
            'origin': 'https://hozon-h5-prod.hozonauto.com',
            'x-requested-with': 'com.hezhong.nezha',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        params = {
            'page': '1',
            'pageSize': '200',#评论数量
            'articleId': articleId
        }
        try:
            response = requests.get(url=url, params=params, headers=headers, timeout=10)
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
            content_list = []
            if 'data' in result and 'rows' in result['data']:
                for item in result['data']['rows']:
                    content_list.append(item['content'])
                if len(content_list) > 0:
                    content = random.choice(content_list)
                    print(f"评论数量：{len(content_list)}")
                    print(f"帖子ID：{articleId} 评论内容：{content}")
                    return articleId, content
                else:
                    print("评论内容为空", '\n', result)
                    print(f"帖子ID：{articleId}")
                    toutiao_openId_list.remove(articleId)
                    random_sleep(10, 20)
    return [],[]

#签到
def sign():
    print("【【【【【【【签到】】】】】】】")
    url = 'https://appapi-pki.chehezhi.cn/hznz/customer/sign'
    for i in range(3):
        nonce = generate_random_number()
        timestamp = int(time.time() * 1000)
        sign = f'GET%2Fhznz%2Fcustomer%2Fsignappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}{sign_string}'
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
            if "积分" in result['message']:
                info['sign'] = True
                return
            elif result['message'] == "请不要重复签到":
                info['sign'] = True
                msg_error.append(f"{info['mobile']}：{result['message']}")
                return
            elif i < 2:
                random_sleep(20, 40)
    msg_error.append(f"{index}签到异常")
            
# 转发  
def forwarArticle():
    print("【【【【【【【转发】】】】】】】")
    url = 'https://appapi-pki.chehezhi.cn/hznz/app_article/forwarArticle'
    id_list = random.sample(xiaoquan_openId_list, 5)
    inx = 0
    for articleId in id_list:
        nonce = generate_random_number()
        timestamp = int(time.time() * 1000)
        sign = f'PUT%2Fhznz%2Fapp_article%2FforwarArticleappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}{sign_string}'
        headers = {
            'Accept': 'application/json',
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
            'devicemac': '3e755c2e-1dc9-3f31-93e0-ecba7a567e1e',
            'Content-Type': 'application/json',
            'Content-Length': '48',
            'Host': 'appapi-pki.chehezhi.cn:18443',
            'Connection': 'Keep-Alive'
        }
        data = {
            'articleId': articleId,
            'forwardTo': '1'
        }
        try:
            response = requests.put(url, headers=headers, json=data, timeout=10)
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
            print(f"转发{articleId}：{result['message']}")
            if result['message'] == "转发成功，获得1积分":
                info['share'] = info['share'] + 1
            else:
                inx = inx + 1
                print(result)
                if inx == 3:
                    info['share'] = 3
                    break
            if info['share'] < 3:
                random_sleep(10, 20)
            else:
                return
    msg_error.append(f"{index}.{info['mobile']}：转发异常") 

#评论帖子
def insertArtComment():
    print("【【【【【【【评论】】】】】】】")
    if len(toutiao_openId_list) < 300:
        print("toutiao_openId_list数量小于100，不进行评论")
        return
    articleId, content = traversal_comment()
    if len(content) == 0:
        print("content数量为0，不进行评论")
        return
    url = 'https://api.chehezhi.cn/hznz/app_article/insertArtComment'
    headers = {
        'Host': 'api.chehezhi.cn',
        'accept': 'application/json, text/plain, */*',
        'channel': 'h5',
        'authorization': f"Bearer {Authorization}",
        'user-agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36',
        'content-type': 'application/json;',
        'origin': 'https://hozon-h5-prod.hozonauto.com',
        'x-requested-with': 'com.hezhong.nezha',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    data = {
        "articleId": articleId,
        "content": content
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        print("请求异常:", e)
    except json.JSONDecodeError as e:
        print("JSON 解码异常:", e)
    except Exception as e:
        print("其他异常:", e)
    else:
        print(f"评论结果：{result['message']}")
        if result['message'] == "成功":
            info['comment'] = info['comment'] + 1
        else:
            print(result)
            msg_error.append(f"{index}评论异常")

#查询
def getCustomer():
    print("【【【【【【【查询】】】】】】】")
    url = 'https://appapi-pki.chehezhi.cn/hznz/customer/getCustomer'
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
        if result['message'] == "成功":
            creditScore = result['data']['creditScore']
            phone = result['data']['phone']
            info['mobile'] = phone
            info['creditScore'] = creditScore
            git_phone.append(phone)
            user_info = f"{phone}：{creditScore}积分"
            print(user_info)
        else:
            print(result)
            msg_error.append(f"{index}查询异常")

def openrw():
    with open(filepath, "r") as f:
        info_new_phone = json.load(f)
        for i in info_new_phone:
            max_phone.append(i['mobile'])

def msg_send():
    # sorted_data = sorted(info_max, key=lambda x: x['creditScore'])#从小到大排序
    sorted_data = sorted(info_max, key=lambda x: x['creditScore'], reverse=True)#从大到小排序
    for item in sorted_data:
        phone = item['mobile']
        creditScore = item['creditScore']
        msg.append(f"{phone}：{creditScore}积分")
        if creditScore >= fixed_creditScore and phone not in oneself:
            msg_phone.append(f"{phone}：{creditScore}积分")
    send(f"{title_name}：{index}", '\n'.join(msg))   
    send(f"{title_name}待下单账号：{len(msg_phone)}", '\n'.join(msg_phone))
    update_github_file(f"token/{title_name}/nzqc.json", info_max)
    update_github_file(f"token/{title_name}/phone_list.txt", '\n'.join(git_phone))
    update_github_file(f"token/{title_name}/token_list.txt", '\n'.join(git_token))
    if len(msg_error) > 0:
        send(f"{title_name}异常", '\n'.join(msg_error))

if __name__ == '__main__':
    title_name = '哪吒汽车'
    filepath = "/ql/data/env/nzqc.json"
    xiaoquan_openId_list = ql_env('nz_xq')
    msg = []
    msg_phone = []
    msg_error = []
    git_token = []
    git_phone = []
    max_phone = []
    index = 1
    openrw()
    random.shuffle(max_phone)
    print(f"小圈板块ID数量：{len(xiaoquan_openId_list)}")
    print(f"共找到{len(max_phone)}个账号")
    for max in max_phone:
        print(f"\n{'-' * 13}正在执行第{index}个账号{'-' * 13}")
        or_sleep = True
        file = open(filepath, 'r+')
        fcntl.flock(file.fileno(), fcntl.LOCK_EX)
        info_max = json.load(file)
        for info in info_max:
            if info['mobile'] == max:
                if info['sign'] and info['share'] >= 3:
                    git_token.append(info['refresh_token'])
                    git_phone.append(info['mobile'])
                    index += 1
                    or_sleep = False
                    break
                if refresh_Authorization():
                    sign() if not info['sign'] else print("签到已完成")
                    forwarArticle() if info['share'] < 3 else print("转发已完成")
                    getCustomer()
                    break      
        file.seek(0)
        file.write(json.dumps(info_max))
        file.truncate()
        fcntl.flock(file.fileno(), fcntl.LOCK_UN)
        file.close()
        if index < len(max_phone) and or_sleep:
            index += 1
            random_sleep(1, 60)    
    msg_send()
