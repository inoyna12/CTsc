'''
cron: 36 9,12,14 * * *
new Env('哪吒汽车');
'''
import requests
import json
import os
import random
import time
import datetime
import hashlib
import urllib.parse
import uuid
from sendNotify import send
from os import environ
from utils.ql_api import get_envs, disable_env, post_envs, put_envs
from utils.github_api import update_github_file

appKey = 'e0ae89fb37b6151889c6de3ba6b84e0d3a67f52cd5767758d4186fefff8f763c'#headers参数
toutiao_openId_list = []
xiaoquan_openId_list = []

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
        nonce = generate_random_number()
        timestamp = str(int(time.time() * 1000))
        sign = f'POST%2Fcustomer%2Faccount%2Finfo%2FrefreshApiTokenappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}refreshtoken%3A{Authorization}8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'
        sign_sha256 = sha256_encode(sign)
        headers = {
            "Authorization": Authorization,
            "appId": "HOZON-B-xKrgEvMt",
            "appKey": appKey,
            "appVersion": "5.5.1",
            'login_channel': '1',
            'channel': 'android',
            "nonce": f"{nonce}",
            "phoneModel": "Redmi 22081212C",
            "timestamp": f"{timestamp}",
            "sign": sign_sha256,
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "appapi-pki.chehezhi.cn:18443"
        }
        data = {
            "refreshToken": f"{Authorization}"
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
                global Authorization_new
                Authorization_new = result['data']['access_token']
                return result['data']['refresh_token']
            else:
                print("刷新Authorization失败")
                print(result)
                send("刷新Authorization失败", f"账号{index + 1}")
                random_sleep(60, 80)
    send("刷新Authorization失败", f"账号{index + 1}")
    return None

def traversal_toutiao_1():
    print("【遍历头条翻页】")
    data_index = 0
    createTime_index = 0
    random_number = random.randint(300, 400)
    print(random_number)
    uuid = generate_random_uuid()
    print(uuid)
    url = f'https://appapi-pki.chehezhi.cn/hznz/app_article/common/article/rec/list?refreshType=loadmore&category=toutiao&uuid={uuid}'
    for i in range(50):
        print(f"第{i + 1}次请求")
        nonce = generate_random_number()
        timestamp = str(int(time.time() * 1000))
        sign = f'GET%2Fhznz%2Fapp_article%2Fcommon%2Farticle%2Frec%2Flistappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}refreshtype%3Dloadmorecategory%3Dtoutiaouuid%3D{uuid}8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'
    #  下滑3Drefreshcategory  
    # 翻页   3Dloadmorecategory
        headers = {
            'appId': 'HOZON-B-xKrgEvMt',
            'appKey': appKey,
            'appVersion': '5.5.1',
            'login_channel': '1',
            'channel': 'android',
            'nonce': f"{nonce}",
            'phoneModel': 'Redmi 22081212C',
            'timestamp': f"{timestamp}",
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
                data_index += 1
                print(result)
            for item in result['data']:
                print(f"发帖时间：{item['volcExtra']['createTime']}，评论数量：{item['commentCount']}")
                if item['commentCount'] > 10:
                    if item['article']['openId'] not in toutiao_openId_list:
                        toutiao_openId_list.append(item['article']['openId'])
                    else:
                        createTime_index += 1
                        print("已存在，不进行加入")
                else:
                    print("评论数量小于10，不进行加入")
            print(f"toutiao_openId_list数量：{len(toutiao_openId_list)}")
            if len(toutiao_openId_list) > random_number or createTime_index > 5 or data_index > 5:
                break
            random_sleep(5, 10)
    print(f"toutiao_openId_list数量：{len(toutiao_openId_list)}")

#爬取小圈   
def traversal_xiaoquan():
    print("【遍历首页小圈板块】")
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
        timestamp = str(int(time.time() * 1000))
        sign = f'GET%2Fhznz%2Fapp_article%2Fcommon%2Farticle%2Frec%2Flistappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}refreshtype%3Dloadmorecategory%3Dxiaoquanuuid%3D{uuid}8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'#小圈下滑刷新
        sign_sha256 = sha256_encode(sign)
        headers = {
            'appId': 'HOZON-B-xKrgEvMt',
            'appKey': appKey,
            'appVersion': '5.5.1',
            'login_channel': '1',
            'channel': 'android',
            'nonce': f"{nonce}",
            'phoneModel': 'Redmi 22081212C',
            'timestamp': f"{timestamp}",
            'sign': sign_sha256,
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
            if len(xiaoquan_openId_list) > random_number or createTime_index > 5 or data_index > 5:
                break
            random_sleep(20, 40)
    print(f"xiaoquan_openId_list数量：{len(xiaoquan_openId_list)}")
    
#爬头条评论
def traversal_comment():
    print("【遍历评论】")
    articleId = random.choice(toutiao_openId_list)
    for i in range(3):
        url = 'https://api.chehezhi.cn/hznz/app_article_comment/listParentComment'
        headers = {
            'Host': 'api.chehezhi.cn',
            'accept': 'application/json, text/plain, */*',
            'channel': 'h5',
            'authorization': f"Bearer {Authorization_new}",
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
            print(result)
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
    timestamp = str(int(time.time() * 1000))
    sign = f'GET%2Fhznz%2Fcustomer%2Fsignappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'
    sign_sha256 = sha256_encode(sign)
    headers = {
        'appId': 'HOZON-B-xKrgEvMt',
        'appKey': appKey,
        'appVersion': '5.5.1',
        'login_channel': '1',
        'channel': 'android',
        'nonce': f"{nonce}",
        'phoneModel': 'Redmi 22081212C',
        'timestamp': f"{timestamp}",
        'sign': sign_sha256,
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 12; zh-cn; 22081212C Build/SKQ1.220303.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
        'Authorization': f"Bearer {Authorization_new}",
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
  
# 转发  
def Share_essay():
    print("【【【【【【【转发】】】】】】】")
    if len(xiaoquan_openId_list) < 100:
        print("xiaoquan_openId_list数量小于100，不进行转发")
        return
    for i in range(2):
        articleId = random.choice(xiaoquan_openId_list)
        url = 'https://appapi-pki.chehezhi.cn/hznz/app_article/forwarArticle'
        nonce = generate_random_number()
        timestamp = str(int(time.time() * 1000))
        sign = f'PUT%2Fhznz%2Fapp_article%2FforwarArticleappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'
        sign_sha256 = sha256_encode(sign)
        headers = {
            'Accept': 'application/json',
            'appId': 'HOZON-B-xKrgEvMt',
            'appKey': appKey,
            'appVersion': '5.5.1',
            'login_channel': '1',
            'channel': 'android',
            'nonce': f"{nonce}",
            'phoneModel': 'Redmi 22081212C',
            'timestamp': f"{timestamp}",
            'sign': sign_sha256,
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 12; zh-cn; 22081212C Build/SKQ1.220303.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
            'Authorization': f"Bearer {Authorization_new}",
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
                break
            else:
                print(result)
                random_sleep(20, 40)
    
#查询
def information():
    print("【【【【【【【查询】】】】】】】")
    url = 'https://appapi-pki.chehezhi.cn/hznz/customer/getCustomer'
    for i in range(5):
        nonce = generate_random_number()
        timestamp = str(int(time.time() * 1000))
        sign = f'GET%2Fhznz%2Fcustomer%2FgetCustomerappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'
        sign_sha256 = sha256_encode(sign)
        headers = {
            'appId': 'HOZON-B-xKrgEvMt',
            'appKey': appKey,
            'appVersion': '5.5.1',
            'login_channel': '1',
            'channel': 'android',
            'nonce': f"{nonce}",
            'phoneModel': 'Redmi 22081212C',
            'timestamp': f"{timestamp}",
            'sign': sign_sha256,
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 12; zh-cn; 22081212C Build/SKQ1.220303.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
            'Authorization': f"Bearer {Authorization_new}",
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
            Phone = phone[:3] + "****" + phone[7:]
            msg = f"{phone}：{creditScore}积分\n"
            print(msg)
            return msg, phone
    print(result)
    send("查询失败", f"账号{index + 1}")
    return ''

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
    url = 'https://api.chehezhi.cn/hznz/app_article_comment/insertArtComment'
    headers = {
        'Host': 'api.chehezhi.cn',
        'accept': 'application/json, text/plain, */*',
        'channel': 'h5',
        'authorization': f"Bearer {Authorization_new}",
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

#发布动态
def addArticle_1():
    img_url = random.choice(img_url_list)
    img_url_list.remove(img_url)
    title = random.choice(title_list)
    title_list.remove(title)
    content = random.choice(content_list)
    content_list.remove(content)
    data = {
        "article_sub_type": 1,
        "content": content,
        "title": title,
        "img_url": img_url,
    }
    data_json = json.dumps(data)
    encoded_data = urllib.parse.quote(data_json)
    url = 'https://appapi-pki.chehezhi.cn/hznz/app_article/customer/addArticle'
    nonce = random.randint(1000000000, 9999999999)
    timestamp = str(int(time.time() * 1000))
    sign = f'POST%2Fhznz%2Fapp_article%2Fcustomer%2FaddArticleappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}json%3A{encoded_data}8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'
    sign_sha256 = sha256_encode(sign)
    headers = {
        'Accept': 'application/json',
        'appId': 'HOZON-B-xKrgEvMt',
        'appKey': appKey,
        'appVersion': '5.2.3',
        'login_channel': '1',
        'channel': 'android',
        'nonce': f"{nonce}",
        'phoneModel': 'Redmi 22081212C',
        'timestamp': f"{timestamp}",
        'sign': sign_sha256,
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 12; zh-cn; 22081212C Build/SKQ1.220303.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
        'Authorization': f"Bearer {Authorization_new}",
        'Content-Type': 'application/json',
        'Host': 'appapi-pki.chehezhi.cn:18443',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Cache-Control': 'no-cache'
    }
    response = requests.post(url, headers=headers, data=data_json)
    result = response.json()
#    print(result)
    print(f"发布动态：\n\n标题：{title}\n内容：{content}\nimg：{img_url}\n\n发布结果：{result['message']}\n")
    message = f"发布动态：{result['message']}\n"
    return message

#发布文章
def addArticle_2():
    img_url = random.choice(img_url_list)
    img_url_list.remove(img_url)
    title = random.choice(title_list)
    title_list.remove(title)
    content = random.choice(content_list)
    content_list.remove(content)
    data = {
        "article_sub_type": 2,
        "img_url": img_url,
        "title": title,
        "content": f"<p>{content}</p>"
    }
    data_json = json.dumps(data)
    encoded_data = urllib.parse.quote(data_json)
    url = 'https://appapi-pki.chehezhi.cn/hznz/app_article/customer/addArticle'
    nonce = random.randint(1000000000, 9999999999)
    timestamp = str(int(time.time() * 1000))
    sign = f'POST%2Fhznz%2Fapp_article%2Fcustomer%2FaddArticleappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}json%3A{encoded_data}'
    sign_sha256 = sha256_encode(sign)
    headers = {
        'Accept': 'application/json',
        'appId': 'HOZON-B-xKrgEvMt',
        'appKey': appKey,
        'appVersion': '5.2.3',
        'login_channel': '1',
        'channel': 'android',
        'nonce': f"{nonce}",
        'phoneModel': 'Redmi 22081212C',
        'timestamp': f"{timestamp}",
        'sign': sign_sha256,
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 12; zh-cn; 22081212C Build/SKQ1.220303.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
        'Authorization': f"Bearer {Authorization_new}",
        'Content-Type': 'application/json',
        'Host': 'appapi-pki.chehezhi.cn:18443',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Cache-Control': 'no-cache'
    }
    response = requests.post(url, headers=headers, data=data_json)
    result = response.json()
#    print(result)
    print(f"发布文章：\n\n标题：{title}\n内容：{content}\nimg：{img_url}\n\n发布结果：{result['message']}\n")
    message = f"发布文章：{result['message']}\n"
    return message

#删除
def del_article():
    id_list = article_id_list()
    url = "https://api.chehezhi.cn/hznz/app_article/delArticle"
    headers = {
        "Host": "api.chehezhi.cn",
        "content-length": "16",
        "accept": "application/json, text/plain, */*",
        "channel": "h5",
        "authorization": f"Bearer {Authorization_new}",
        "user-agent": "Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36",
        "content-type": "application/json;",
        "origin": "https://hozon-h5-prod.hozonauto.com",
        "x-requested-with": "com.hezhong.nezha",
        "sec-fetch-site": "cross-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    for ids in id_list:
        data = {"ids": [ids]}
        response = requests.post(url=url, headers=headers, json=data)
        result = response.json()
#        print(result)
        print(f"删除{ids}：{result['message']}")

#遍历个人主页 动态，文章id
def article_id_list():
    url = 'https://api.chehezhi.cn/hznz/app_article/customer/article/list?page=1&pageSize=10&articleSubType=1'#动态
    url2 = 'https://api.chehezhi.cn/hznz/app_article/customer/article/list?page=1&pageSize=10&articleSubType=2'#文章
    headers = {
        "Host": "api.chehezhi.cn",
        "accept": "application/json, text/plain, */*",
        "channel": "h5",
        "authorization": f"Bearer {Authorization_new}",
        "user-agent": "Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36",
        "origin": "https://hozon-h5-prod.hozonauto.com",
        "x-requested-with": "com.hezhong.nezha",
        "sec-fetch-site": "cross-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    response = requests.get(url=url, headers=headers)
    response2 = requests.get(url=url2, headers=headers)
    result = response.json()
    result2 = response2.json()
#    print(result)
    id_list = []#id列表
    for item in result['data']['rows']:
        id_list.append(item['id'])
    for item in result2['data']['rows']:
        id_list.append(item['id'])   
    articleStatus_list = []#审核状态列表
    for item in result['data']['rows']:
        articleStatus_list.append(item['articleStatus'])
    for item in result2['data']['rows']:
        articleStatus_list.append(item['articleStatus'])
    print(id_list)
    print(articleStatus_list)
    del_id_list = [id_list[i] for i in range(len(articleStatus_list)) if articleStatus_list[i] != articleStatus]
    print(f"需要删除的列表ID：{del_id_list}\n")
    return del_id_list

def ql_env(name):
    if name in os.environ:
        token_list = os.environ[name].split('\n')
        if len(token_list) > 0:
            return token_list
        else:
            print("变量未启用")
            sys.exit(1)
    else:
        print("未添加变量")
        sys.exit(0)

def ql_env_put(name, data, Remarks=None):
    fetch_env = get_envs(name)#查询环境变量信息
    if fetch_env:
        put_envs(fetch_env[0].get('id'), fetch_env[0].get('name'), data, Remarks)
        fetch2_env = get_envs(name)
        str_time = "变量修改时间：" + fetch2_env[0].get('timestamp') + "\n"
        return str_time
    else:
        print(f"未找到 {name} 变量")

if __name__ == '__main__':
    env_name = "NZtoken"#变量名
    env_phone = "NZphone"#变量名
    title_name = '哪吒汽车'
    msg = ""
    token_list = ""
    phone_list = ""
    index = 0
    quantity = ql_env(env_name)
    print (f"共找到{len(quantity)}个账号")
    traversal_toutiao_1()
#    traversal_xiaoquan()
    for Authorization in quantity:
        print(f"\n------------正在执行第{index + 1}个账号----------------")
        func = refresh_Authorization()
        if func is not None:
            sign()
            Share_essay()
            insertArtComment()
            creditScore, phones = information()
            msg += creditScore
            if len(token_list) > 0:
                token_list += '\n' + func
            else:
                token_list += func
            if len(phone_list) > 0:
                phone_list += '\n' + phones
            else:
                phone_list += phones
            print(f"第{index + 1}个账号运行完成")
        else:
            msg += "token失效或脚本待更新\n"
        index += 1
        if index < len(quantity):
            random_sleep(1, 100)
#    print(msg)
    msg += ql_env_put(env_name, token_list, title_name)
    msg += ql_env_put(env_phone, phone_list, title_name)
    msg += update_github_file(f"token/{title_name}/token_list.txt", token_list)
    msg += update_github_file(f"token/{title_name}/phone_list.txt", phone_list)
    send(title_name, msg)
