#抓取https://appapi-pki.chehezhi.cn/customer/account/info/refreshApiToken中body里refreshToken值，多个换行隔开

#10积分=1元
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

#发布文章标题不能少于5个字
#发布后审核中的文章动态会导致爬取小圈失败
articleStatus = 1#不删除
#articleStatus=2 审核通过
#articleStatus=3 审核未通过
#articleStatus=1 审核中

#图片url
img_url_list = [
'https://netaprod-static.hozonauto.com/prod/20230517/16132798144353353.jpg', 
'https://netaprod-static.hozonauto.com/prod/20230522/16514711515740895.jpg', 
'https://netaprod-static.hozonauto.com/prod/20230521/16461068345723048.JPEG',
'https://netaprod-static.hozonauto.com/prod/20230521/16461067622375569.JPEG',
'https://netaprod-static.hozonauto.com/prod/20230521/16461153452870671.JPEG',
'https://netaprod-static.hozonauto.com/prod/20230518/16189995439662051.png',
'https://netaprod-static.hozonauto.com/f5/20230518/16166942859436635.png',
'https://netaprod-static.hozonauto.com/f5/20230524/16707968178729987.png',
'https://netaprod-static.hozonauto.com/f5/20230524/16707968226329724.png',
'https://netaprod-static.hozonauto.com/prod/20230524/16707771648482323.JPEG',
'https://netaprod-static.hozonauto.com/f5/20230524/16694422469325242.png',
'https://netaprod-static.hozonauto.com/f5/20230524/16694422539069658.png',
'https://netaprod-static.hozonauto.com/f5/20230524/16728853079399074.png',
'https://netaprod-static.hozonauto.com/prod/20230524/16726654887463964.JPEG',
'https://netaprod-static.hozonauto.com/prod/20230524/16725792513329671.JPEG',
'https://netaprod-static.hozonauto.com/prod/20230524/16725792772811866.jpg',
'https://netaprod-static.hozonauto.com/f4/20230525/16793187981771182.jpg',
'https://netaprod-static.hozonauto.com/prod/20230525/16791266038117651.JPEG',
'https://netaprod-static.hozonauto.com/prod/20230525/16772208898293088.JPEG',
'https://netaprod-static.hozonauto.com/prod/20230521/16432907577221826.jpg',
'https://netaprod-static.hozonauto.com/prod/20230525/16772269475936553.JPEG'
]

#标题
title_list = [
'开车出行，驾轻就熟',
'驾车游玩，发现更多精彩',
'行走大地，与开车为伴',
'见证美好，从开车开始',
'最美风景，都在开车路上',
'开着车，放飞心情',
'自由行走，开车是最佳出行方式',
'驾车出行，拥抱生活的美好',
'哪吒出行🚗',
'出发，顺利🚗',
'哪吒日常✨',
'出门全靠哪吒',
'开着哪吒去旅游',
'出发啦🙏🏻🙏🏻🙏🏻',
'哪吒汽车，让你的生活更美好',
'智慧出行，从哪吒开始',
'哪吒伴你，畅游城市',
'分享美好生活，哪吒与你同行',
'出发吧！和哪吒一起探索城市的美好',
'选择哪吒，留下精彩的回忆',
'品质生活，从哪吒开始',
'简单出行，贴心哪吒',
'未来智行，哪吒助你',
'哪吒出行，畅游城市',
'哪吒智能出行，新体验',
'哪吒智造，品质出行',
'哪吒共享，美好旅程',
'哪吒智慧，安心出行'
]

#内容
content_list = [
'与哪吒同行，发现城市之美',
'哪吒，开启城市出行的轻松模式'
'开着我的哪吒，又是愉快的一天',
'哪吒出行成本是真低',
'舒服的天气，美丽的心情，美好的一天',
'哪吒汽车丰富多彩',
'谁懂啊，哪吒真好。',
'哪吒车型布局还是那么的好看，双联平的设计，增添了车辆的科技感',
'我带着哪吒一起溜',
'哪吒车真是越看越喜欢',
'沿途风景美如画',
'开着哪吒每天在路上，心情真的不错呦',
'快乐出行，畅享美好',
'高性价比，哪吒值得拥有',
'天气宜人，心情满满，出行无忧',
'哪吒汽车多彩多姿，让你的出行更有趣',
'哪吒，一种绝妙的选择',
'科技感十足，哪吒汽车好评如潮',
'哪吒陪伴左右，幸福始终相随',
'哪吒车型设计感强，让你爱不释手',
'美景相伴，哪吒出行视野开阔',
'哪吒车上心情大好，驾驶更加愉快',
'哪吒汽车：让你的出行不再单调，感受别样人生',
'探索未知，迎接挑战，选择哪吒，开启新的出行旅程',
'一辆哪吒汽车，让你享受不一样的生活品质与驾驶乐趣'
]

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
    result = response.json()
    if "code" in result and result['code'] == 20000:
        print("刷新Authorization成功")
        global Authorization_new
        Authorization_new = result['data']['access_token']
        return result['data']['refresh_token']
    else:
        print("刷新Authorization失败")
        print(result)
        return None

#爬取小圈   
def traversal_xiaoquan():
    print("【遍历首页小圈板块】")
#    print(f"爬取首页小圈板块\n")
    url = 'https://appapi-pki.chehezhi.cn/hznz/app_article/common/article/rec/list?refreshType=open&category=xiaoquan'#首页
    
#    url2 = 'https://appapi-pki.chehezhi.cn/hznz/app_article/common/article/rec/list?refreshType=refresh&category=xiaoquan'#首页下滑刷新
   
    nonce = random.randint(1000000000, 9999999999)
    timestamp = str(int(time.time() * 1000))
    sign = f'GET%2Fhznz%2Fapp_article%2Fcommon%2Farticle%2Frec%2Flistappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}refreshtype%3Dopencategory%3Dxiaoquan8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'#小圈首页
#    sign = f'GET%2Fhznz%2Fapp_article%2Fcommon%2Farticle%2Frec%2Flistappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}refreshtype%3Dloadmorecategory%3Dxiaoquan8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'#小圈翻页    
#    sign =f'GET%2Fhznz%2Fapp_article%2Fcommon%2Farticle%2Frec%2Flistappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}refreshtype%3Drefreshcategory%3Dxiaoquan8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'#首页下滑刷新    
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
    for i in range(3):
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            break
        else:
            print(f'请求失败，响应状态码为{response.status_code}')
    result = response.json()
#    print(result)
    articleSubType_list = []
    group_id_list = []
    url_imgs_list = []
    createTime_list = []
    title_list = []
    content_list = []
    for item in result['data']:
        articleSubType_list.append(item['volcExtra']['articleSubType']) 
        group_id_list.append(item['article']['groupId'])
        url_imgs_list.append(item['volcExtra']['imgs'])
        createTime_list.append(item['volcExtra']['createTime'])
        title_list.append(item['article']['title'])
        content_list.append(item['content'])
    # print(f"Type列表(动态=1，文章=2)：\n{articleSubType_list}\n")
    # print(f"groupId列表：\n{group_id_list}\n")
    # print(f"url_imgs列表：\n{url_imgs_list}\n")
    # print(f"发帖时间列表：\n{createTime_list}\n")
    # print(f"标题列表：\n{title_list}\n")
    # print(f"内容列表：\n{content_list}\n")
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
            print(f"group_id_list：\n{group_id_list}\nopenId_id_list：\n{openId_id_list}")
            send("哪吒遍历头条翻页", f"账号{index + 1}")
            random_sleep(20, 40)
    indexs = random.randint(0, len(openId_id_list)-1)#把随机序列号存入变量
    openId = openId_id_list[indexs]
    groupId = group_id_list[indexs]
    print(f"帖子ID：{openId}，{groupId}")
    return openId,groupId
    
#爬头条评论
def traversal_comment(openId, groupId):
    print("【遍历头条评论】")
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
#    print(f"评论列表：\n{content_list}")
    if len(content_list) > 0:
        content = random.choice(content_list)
        print(f"评论内容：{content}")
        return content
    else:
        print(result)
        send("获取评论出错", f"账号{index + 1}")

#签到
def sign():
    print("\n【【【【【【【签到】】】】】】】\n")
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
    print("\n【【【【【【【转发】】】】】】】\n")
    groupId_list = traversal_xiaoquan()#小圈板块
    for i in range(3):
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
            random_sleep(20, 50)
    
#查询
def information():
    print("\n【【【【【【【查询】】】】】】】\n")
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
    print("\n【【【【【【【评论】】】】】】】\n")
    openId, groupId = traversal_toutiao()
    content = traversal_comment(openId, groupId)
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
#        print(data)
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
#    print(result)
    message = f"评论{openId}：{result['message']}\n"
    print(message)

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
    title_name = '哪吒汽车'
    msg = ""
    token_list = ""
    phone_list = ""
    index = 0
    quantity = ql_env(env_name)
    print (f"共找到{len(quantity)}个账号")
    for Authorization in quantity:
        print(f"------------正在执行第{index + 1}个账号----------------")
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
            print(f"第{index + 1}个账号运行完成\n")
        else:
            msg += "token失效或脚本待更新\n"
        index += 1
        if index < len(quantity):
            random_sleep(1, 200)
#    print(msg)
    msg += ql_env_put(env_name, token_list, title_name)
    msg += update_github_file(f"token/{title_name}/token_list.txt", token_list)
    msg += update_github_file(f"token/{title_name}/phone_list.txt", phone_list)
    send(title_name, msg)
