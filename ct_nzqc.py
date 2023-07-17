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
from sendNotify import send
from os import environ
from utils.ql_api import get_envs, disable_env, post_envs, put_envs
from utils.github_api import update_github_file

appKey = 'e0ae89fb37b6151889c6de3ba6b84e0d3a67f52cd5767758d4186fefff8f763c'#headers参数

def random_sleep(min_val, max_val):
    num = random.randint(min_val, max_val)
    print(f"等待{num}秒后继续>>>>>>>>>>>")
    time.sleep(num)
    return num

def sha256_encode(string):
    hash_object = hashlib.sha256(string.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig

def refresh_Authorization():
    url = 'https://appapi-pki.chehezhi.cn/customer/account/info/refreshApiToken'
    for i in range(5):
        try:
            nonce = random.randint(1000000000, 9999999999)
            timestamp = str(int(time.time() * 1000))
            sign = f'POST%2Fcustomer%2Faccount%2Finfo%2FrefreshApiTokenappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}refreshtoken%3A{Authorization}8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'
            sign_sha256 = sha256_encode(sign)
            headers = {
                "Authorization": Authorization,
                "appId": "HOZON-B-xKrgEvMt",
                "appKey": appKey,
                "appVersion": "5.2.3",
                "login_channel": "1",
                "channel": "android",
                "nonce": f"{nonce}",
                "phoneModel": "Redmi 22081212C",
                "timestamp": f"{timestamp}",
                "sign": sign_sha256,
                "Content-Type": "application/x-www-form-urlencoded",
                "Content-Length": "613",
                "Host": "appapi-pki.chehezhi.cn:18443",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/4.9.3"
            }
            data = {
                "refreshToken": f"{Authorization}"
            }
            response = requests.post(url=url, headers=headers, data=data)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            print("请求失败:", e)
            send("刷新Authorization失败", f"账号{index + 1}")
            random_sleep(30, 60)
    result = response.json()
    if "code" in result and result['code'] == 20000:
        print("刷新Authorization成功")
        global Authorization_new
        Authorization_new = result['data']['access_token']
        return result['data']['refresh_token']
    else:
        print("刷新Authorization失败")
        print(result)
        send("刷新Authorization失败", f"账号{index + 1}")
        return None

#爬取小圈   
def traversal_xiaoquan():
    print("【遍历首页小圈板块】")
    for i in range(3):
        try:
            url = 'https://appapi-pki.chehezhi.cn/hznz/app_article/common/article/rec/list?refreshType=open&category=xiaoquan'#首页
            nonce = random.randint(1000000000, 9999999999)
            timestamp = str(int(time.time() * 1000))
            sign = f'GET%2Fhznz%2Fapp_article%2Fcommon%2Farticle%2Frec%2Flistappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}refreshtype%3Dopencategory%3Dxiaoquan8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'#小圈首页
            sign_sha256 = sha256_encode(sign)
            headers = {
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
                'Host': 'appapi-pki.chehezhi.cn:18443',
                'Connection': 'Keep-Alive'
            }
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            result = response.json()
            group_id_list = []
            for item in result['data']:
                group_id_list.append(item['article']['groupId'])
            if len(group_id_list) > 2:
                break
            else:
                print(result)
                send("遍历首页小圈", f"账号{index + 1}")
                random_sleep(30, 60)
        except requests.exceptions.RequestException as e:
            print("请求失败:", e)
            send("遍历小圈失败", f"账号{index + 1}")
            random_sleep(30, 60)
    return group_id_list

#爬取头条翻页
def traversal_toutiao():
    print("【遍历头条翻页】")
    url = 'https://appapi-pki.chehezhi.cn/hznz/app_article/common/article/rec/list?refreshType=loadmore&category=toutiao'
    for i in range(3):
        nonce = random.randint(1000000000, 9999999999)
        timestamp = str(int(time.time() * 1000))
        sign = f'GET%2Fhznz%2Fapp_article%2Fcommon%2Farticle%2Frec%2Flistappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}refreshtype%3Dloadmorecategory%3Dtoutiao8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'
        sign_sha256 = sha256_encode(sign)
        headers = {
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
            'Host': 'appapi-pki.chehezhi.cn:18443',
            'Connection': 'Keep-Alive'
        }
        response = requests.get(url=url, headers=headers)
        result = response.json()
        group_id_list = []
        openId_id_list = []
        for item in result['data']:
            group_id_list.append(item['article']['groupId'])
            openId_id_list.append(item['article']['openId'])
        if len(group_id_list) > 3:
            break
        else:
            print(result)
            print(f"group_id_list：\n{group_id_list}")
            print(f"openId_id_list：\n{openId_id_list}")
            send("哪吒遍历头条翻页", f"账号{index + 1}")
            random_sleep(20, 40)
    return openId_id_list, group_id_list
    
#爬头条评论
def traversal_comment():
    print("【遍历头条评论】")
    openId_id_list, group_id_list = traversal_toutiao()
    for i in range(3):
        indexs = random.randint(0, len(openId_id_list)-1)
        openId = openId_id_list[indexs]
        groupId = group_id_list[indexs]
        openId_id_list.remove(openId)
        group_id_list.remove(groupId)
        url = 'https://api.chehezhi.cn/hznz/app_article_comment/listParentComment'
        headers = {
            'Host': 'api.chehezhi.cn',
            'accept': 'application/json, text/plain, */*',
            'channel': 'h5',
            'authorization': f"Bearer {Authorization_new}",
            'user-agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36',
            'origin': 'https://hozon-h5-prod.hozonauto.com',
            'x-requested-with': 'com.hezhong.nezha',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        params = {
            'page': '1',
            'pageSize': '100',#评论数量
            'groupId': groupId,
            'openId': openId,
            'generateType': 'ugc_api'
        }
        response = requests.get(url=url, params=params, headers=headers)
        result = response.json()
        content_list = []
        for item in result['data']['rows']:
            content_list.append(item['content'])
        if len(content_list) > 0:
            content = random.choice(content_list)
            print(f"帖子ID：{openId}，{groupId}")
            print(f"评论内容：{content}")
            break
        elif len(content_list) == 0:
            print("评论内容为空")
            random_sleep(10, 20)
        else:
            print(result)
            random_sleep(40, 60)
            send("获取评论出错", f"账号{index + 1}")
    return openId, groupId, content

#签到
def sign():
    print("【【【【【【【签到】】】】】】】")
    url = 'https://appapi-pki.chehezhi.cn/hznz/customer/sign'
    nonce = random.randint(1000000000, 9999999999)
    timestamp = str(int(time.time() * 1000))
    sign = f'GET%2Fhznz%2Fcustomer%2Fsignappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'
    sign_sha256 = sha256_encode(sign)
    headers = {
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
        'Host': 'appapi-pki.chehezhi.cn:18443',
        'Connection': 'Keep-Alive'
    }
    response = requests.get(url=url, headers=headers)
    result = response.json()
#    print(result)
    print(result['message'])
  
# 转发  
def Share_essay():
    print("【【【【【【【转发】】】】】】】")
    groupId_list = traversal_xiaoquan()#小圈板块
    for i in range(2):
        groupId = random.choice(groupId_list)
        groupId_list.remove(groupId)
        url = 'https://appapi-pki.chehezhi.cn/hznz/app_article/forwarArticle'
        nonce = random.randint(1000000000, 9999999999)
        timestamp = str(int(time.time() * 1000))
        sign = f'PUT%2Fhznz%2Fapp_article%2FforwarArticleappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'
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
            'devicemac': '3e755c2e-1dc9-3f31-93e0-ecba7a567e1e',
            'Content-Type': 'application/json',
            'Content-Length': '48',
            'Host': 'appapi-pki.chehezhi.cn:18443',
            'Connection': 'Keep-Alive'
        }
        data = {
            'articleId': groupId,
            'forwardTo': '1'
        }
        response = requests.put(url, headers=headers, json=data)
        result = response.json()
        print(f"转发{groupId}：{result['message']}")
        if result['message'] == "转发成功，获得1积分":
            break
        else:
            send("转发", f"账号{index + 1}")
            print(result)
            random_sleep(40, 60)
    
#查询
def information():
    print("【【【【【【【查询】】】】】】】")
    url = 'https://appapi-pki.chehezhi.cn/hznz/customer/getCustomer'
    for i in range(3):
        try:
            nonce = random.randint(1000000000, 9999999999)
            timestamp = str(int(time.time() * 1000))
            sign = f'GET%2Fhznz%2Fcustomer%2FgetCustomerappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'
            sign_sha256 = sha256_encode(sign)
            headers = {
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
                'Host': 'appapi-pki.chehezhi.cn:18443',
                'Connection': 'Keep-Alive'
            }
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            print("请求失败:", e)
            send("nz查询", f"账号{index + 1}")
            random_sleep(20, 50)
    result = response.json()
    creditScore = result['data']['creditScore']
    phone = result['data']['phone']
    Phone = phone[:3] + "****" + phone[7:]
    msg = f"{Phone}：{creditScore}积分\n"
    print(msg)
    return msg, phone

#评论帖子
def insertArtComment():
    print("【【【【【【【评论】】】】】】】")
    openId, groupId, content = traversal_comment()
    url = 'https://api.chehezhi.cn/hznz/app_article_comment/insertArtComment'
    headers = {
        'Host': 'api.chehezhi.cn',
        'content-length': '135',
        'accept': 'application/json, text/plain, */*',
        'channel': 'h5',
        'authorization': f"Bearer {Authorization_new}",
        'user-agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36',
        'content-type': 'application/json;',
        'origin': 'https://hozon-h5-prod.hozonauto.com',
        'x-requested-with': 'com.hezhong.nezha',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    data = {
        "content": content,
        "parentId": None,
        "openId": openId,
        "groupId": groupId,
        "generateType": "ugc_api"
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
#    print(result)
    print(result['message'])

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
            random_sleep(1, 200)
#    print(msg)
    msg += ql_env_put(env_name, token_list, title_name)
    msg += ql_env_put(env_phone, phone_list, title_name)
    msg += update_github_file(f"token/{title_name}/token_list.txt", token_list)
    msg += update_github_file(f"token/{title_name}/phone_list.txt", phone_list)
    send(title_name, msg)
