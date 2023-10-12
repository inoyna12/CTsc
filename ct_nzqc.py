'''
cron: 36 9,12,14 * * *
new Env('哪吒汽车');
'''
import requests
import json
import random
import time
import datetime
import hashlib
import urllib.parse
import uuid
from sendNotify import send
from utils.github_api import update_github_file

appVersion = "5.5.1"
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

def refresh_Authorization():
    url = 'https://appapi-pki.chehezhi.cn/customer/account/info/refreshApiToken'
    for i in range(50):
        now = datetime.datetime.now()
        formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
        nonce = generate_random_number()
        timestamp = int(time.time() * 1000)
        sign = f'POST%2Fcustomer%2Faccount%2Finfo%2FrefreshApiTokenappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}refreshtoken%3A{info['refresh_token']}{sign_string}'
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
                info['access_token_time'] = str(formatted_time)
                info['refresh_token'] = result['data']['refresh_token']
                info['refresh_token_time'] = str(formatted_time)
                return
            else:
                print("刷新Authorization失败")
                print(result)
                send("刷新Authorization失败", f"账号{index + 1}")
                random_sleep(60, 80)
    send("刷新Authorization失败", f"账号{index + 1}")
    return None

def toutiao_loadmore():
    print("【遍历头条翻页】")
    createTime_index = 0
    random_number = random.randint(100, 200)
    uuid = generate_random_uuid()
    print(uuid, random_number)
    url = f'https://appapi-pki.chehezhi.cn/hznz/app_article/common/article/rec/list?refreshType=loadmore&category=toutiao&uuid={uuid}'
    for i in range(50):
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
            random_sleep(30, 50)

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
    random_number = random.randint(100, 200)
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
            random_sleep(20, 40)
    print(f"xiaoquan_openId_list数量：{len(xiaoquan_openId_list)}")
    
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
            'pageSize': '100',#评论数量
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
                    print(f"帖子ID：{articleId} 评论内容：{content}")
                    return articleId, content
                else:
                    print("评论内容为空", '\n', result)
                    print(f"帖子ID：{articleId}")
                    random_sleep(60, 80)
    return [],[]

#签到
def sign():
    print("【【【【【【【签到】】】】】】】")
    url = 'https://appapi-pki.chehezhi.cn/hznz/customer/sign'
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
        info['sign'] = True
  
# 转发  
def forwarArticle():
    print("【【【【【【【转发】】】】】】】")
    if len(xiaoquan_openId_list) < 50:
        print("xiaoquan_openId_list数量小于50，不进行转发")
        return
    for i in range(2):
        articleId = random.choice(xiaoquan_openId_list)
        url = 'https://appapi-pki.chehezhi.cn/hznz/app_article/forwarArticle'
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
                return
            else:
                print(result)
                random_sleep(20, 40)

#评论帖子
def insertArtComment():
    print("【【【【【【【评论】】】】】】】")
    if len(toutiao_openId_list) < 100:
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

#查询
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
            info['mobile'] = phone
            info['creditScore'] = creditScore
            user_info = f"{phone}：{creditScore}积分"
            print(user_info)
            msg.append(user_info)
            if int(creditScore) >= fixed_creditScore and phone not in oneself:
                msg_phone.append(phone)
            return
    print(result)
    send("查询失败", f"账号{index + 1}")
    return None

# def send_new():
    # if len(toutiao_openId_list) < 200 or len(xiaoquan_openId_list) < 50:
        # send(title_name, f"头条数量：{len(toutiao_openId_list)}\n小圈数量：{len(xiaoquan_openId_list)}")

if __name__ == '__main__':
    title_name = '哪吒汽车'
    filepath = "/ql/data/env/nzqc.json"
    msg = []
    msg_phone = []
    toutiao_openId_list = []
    xiaoquan_openId_list = []
    index = 0
    toutiao_open()
    toutiao_loadmore()
    xiaoquan_loadmore()
    with open(filepath, "r") as f:
        info_new = json.load(f)
    print(f"共找到{len(info_new)}个账号")
    for info in info_new:
        print(f"\n{'-' * 15}正在执行第{index + 1}个账号{'-' * 15}")
        refresh_Authorization()
        sign() if not info['sign'] else print("已签到")
        forwarArticle() if i['share'] < 3 else print("转发已完成")
        insertArtComment() if i['comment'] < 3 else print("评论已完成")
        getCustomer()
        with open(filepath, "w") as f:
            json.dump(info_new, f)
        index += 1
        if index < len(info_new):
            random_sleep(1, 100)
    send(f"{title_name}：{index}", '\n'.join(msg))   
    send(f"{title_name}待下单账号：{len(msg_phone)}", '\n'.join(msg_phone))
    update_github_file(f"token/{title_name}/nzqc.json", info_new)
