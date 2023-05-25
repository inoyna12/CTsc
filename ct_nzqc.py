#10积分=1元
'''
cron: 36 9 * * *
new Env('哪吒汽车');
'''
import requests
import json
import os
import random
import time
import hashlib
import urllib.parse
from sendNotify import send
from os import environ

def tihuan(url_picture, title, content):
    data = '{"article_sub_type":2,"img_url":"https:\/\/netaprod-static.hozonauto.com\/f4\/20230523\/16619043269420214.png","title":"标题","content":"<p>内容<\/p>"}'
    url_zhuan = str(url_picture[0]).replace('/', '\/')
    data_url = data.replace('https:\/\/netaprod-static.hozonauto.com\/f4\/20230523\/16619043269420214.png', url_zhuan)
    data_url_title = data_url.replace('标题', title[0])
    data_url_title_content = data_url_title.replace('内容', content[0])
    return data_url_title_content

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
    global Authorization_new
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
    if result['success'] == True:
        print("刷新Authorization成功")
        Authorization_new = result['data']['access_token']
    return result['success']

#爬取小圈板块
def traversal_xiaoquan():
    url = 'https://appapi-pki.chehezhi.cn/hznz/app_article/common/article/rec/list?refreshType=open&category=xiaoquan'
    nonce = random.randint(1000000000, 9999999999)
    timestamp = str(int(time.time() * 1000))
    sign = f'GET%2Fhznz%2Fapp_article%2Fcommon%2Farticle%2Frec%2Flistappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}refreshtype%3Dopencategory%3Dxiaoquan8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'
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
    print(result)
    group_id_list = []
    for item in result['data']:
        group_id_list.append(item['article']['groupId'])
    print(f"小圈groupId列表：\n{group_id_list}\n")
    return group_id_list

#爬取头条翻页
def traversal_toutiao():
    msg = ""
    url = 'https://appapi-pki.chehezhi.cn/hznz/app_article/common/article/rec/list?refreshType=loadmore&category=toutiao'
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
#    print(result)
    group_id_list = []
    for item in result['data']:
        group_id_list.append(item['article']['groupId'])
    print(f"头条groupId列表：\n{group_id_list}\n")
#    return group_id_list
    openId_id_list = []
    for item in result['data']:
        openId_id_list.append(item['article']['openId'])
    print(f"头条openId列表：\n{openId_id_list}\n")
    return openId_id_list,group_id_list
    

#爬头条评论
def traversal_comment(openId, groupId):
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
        'pageSize': '10',
        'groupId': groupId,
        'openId': openId,
        'generateType': 'ugc_api'
    }
    response = requests.get(url, headers=headers, params=params)
    result = response.json()
#    print(result)
    content_list = []
    for item in result['data']['rows']:
        content_list.append(item['content'])
    print(f"头条content列表：\n{content_list}\n")
    return random.choice(content_list)

#签到
def sign():
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
    message = f"{result['message']}\n"
    print(message)
    return message
  
# 分享   
def Share_essay():
    groupId = traversal_xiaoquan()
    msg = ""
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
    success_count = 0 # 记录成功次数
    total_count = 0   # 记录总共尝试次数
    while success_count < 3 and total_count < 6:
        selected = random.choice(groupId)
        data = {
            'articleId': selected,
            'forwardTo': '1'
        }
        groupId.remove(selected)
        response = requests.put(url, headers=headers, json=data)
        result = response.json()
#        print(result)
        if result['message'] == "转发成功，获得1积分":
            message = f"转发{data['articleId']}：{result['message']}\n"
            print(message)
            msg += message
            success_count += 1
        elif result['message'] == "转发成功" or "成功":
            print(f"转发{data['articleId']}：重复转发或当日任务已完成，未获得积分")
        total_count += 1
        if success_count < 3 and total_count < 6:
            random_sleep(30, 60)
    return msg

#查询
def information():
    url = 'https://appapi-pki.chehezhi.cn/hznz/customer/getCustomer'
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
    result = response.json()
#    print(result)
    addUpScore = result['data']['addUpScore']
    phone = result['data']['phone']
    Phone = phone[:3] + "****" + phone[7:]
    msg = f"{Phone}：{addUpScore}积分\n"
    print(msg)
    return msg

#评论帖子
def insertArtComment():
    msg = ""
    openId_id_list,group_id_list = traversal_toutiao()
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
    for i in range(3):
        openId = openId_id_list.pop(0)
        groupId = group_id_list.pop(0)
        content = traversal_comment(openId, groupId)
        print(f"获取评论内容：{content}")
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
        message = f"评论{groupId}：{result['message']}\n"
        print(message)
        msg += message
        if i < 2: 
            random_sleep(60, 120)
    return msg

#发布文章
def addArticle():
    url_picture = ['https://netaprod-static.hozonauto.com/prod/20230517/16132798144353353.jpg']
    title = ['终于下班啦']#标题
    content = ['又是愉快的一天，开着我的哪吒回家啦']#内容
    data = {
        "article_sub_type": 2,
        "img_url": f"{url_picture[0]}",
        "title": f"{title[0]}",
        "content": f"<p>{content[0]}</p>"
    }
    data1 = json.dumps(data)
    encoded_data = urllib.parse.quote(data1)
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
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()
    print(result)

def ql_env():
    if "NZtoken" in os.environ:
        token_list = os.environ['NZtoken'].split('\n')
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
    index = 1
    quantity = ql_env()
    print (f"共找到{len(quantity)}个账号")
    for cookie in quantity:
        appKey = cookie.split('&')[0]
        Authorization = cookie.split('&')[1]
        print(f"------------正在执行第{index}个账号----------------")
        msg += f"第{str(index)}个账号运行结果: \n"
        if refresh_Authorization() == True:
            msg += sign()
            msg += Share_essay()
            msg += insertArtComment()
            msg += information()
            print(f"第{str(index)}个账号运行完成\n")
        else:
            msg += "token失效或脚本待更新\n"
        index += 1
    send('哪吒汽车', msg)


#traversal_xiaoquan()  #爬小圈帖子
#traversal_toutiao()  #爬头条帖子
#traversal_comment()   #爬头条评论