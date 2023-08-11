'''
cron: 36 9 * * *
new Env('吉利汽车');
'''
import requests
import os
import json
import time
import random
import datetime
import execjs
from sendNotify import send
from utils.ql_api import get_envs, disable_env, post_envs, put_envs
from utils.github_api import update_github_file

content_list = []

#签到
def sign():
    print("【【【【【【【签到】】】】】】】")
    url = 'https://app.geely.com/api/v1/userSign/sign'
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    current_timestamp = int(time.time())
    data = {
        "signDate": str(formatted_time),
        "ts": str(current_timestamp),
        "cId":"BLqo2nmmoPgGuJtFDWlUjRI2b1b"
    }
    js_code = open('utils/jlqc.js', 'r', encoding='utf-8').read()
    js = execjs.compile(js_code)
    data_sign = js.call("enen", data)
    headers = {
        'Host': 'app.geely.com',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36/geelyApp/android/geelyApp',
        'token': token,
        'x-data-sign': data_sign,
        'content-type': 'application/json',
        'origin': 'https://app.geely.com',
        'referer': 'https://app.geely.com/app-h5/sign-in?showTitleBar=0',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    if result['code'] == 'success':
        print(result['code'])
        if 'prizeName' in result['data']:
            print(result['data']['prizeName'])
    else:
        print(result)

#遍历
def queryByCircleOrTopic():
    print("【遍历动态】")
    url = 'https://app.geely.com/api/v2/topicContent/queryByCircleOrTopic'
    headers = {
        "Host": "app.geely.com",
        "accept": "application/json",
        "content-type": "application/json; charset=UTF-8",
        "devicesn": "356596585696247"
    }
    data = {
        "topicId": None,
        "searchSource": 2,
        "pageSize": 100,
        "auditStatus": 3,
        "circleId": "1595443865836462081",
        "pageNum": 1
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    for item in result['data']['list']:
        print("帖子内容：", item['content'])
        print(f"发帖时间：{item['createdTime']}，内容长度：{len(item['content'])}")
        if len(item['content']) < 10:
            content_list.append(item['content'])
        else:
            print("不加入")
    print(content_list, len(content_list))

#发动态    
def create():
    print("【【【【【【【发布动态】】】】】】】")
    url = 'https://app.geely.com/api/v2/topicContent/create'
    headers = {
        "Host": "app.geely.com",
        "accept": "application/json",
        "content-type": "application/json; charset=UTF-8",
        "devicesn": "356596585696247",
        "token": token
    }
    content = random.choice(content_list)
    data = {
        "circleId": None,
        "contentType": 1,
        "content": content,
        "fileList": [],
        "topicList": []
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    if result['code'] == 'success':
        print(f"内容：{content}，发布结果：{result['code']}")
    else:
        print(result)
    
#遍历我的动态数量
def queryMy():
    print("【遍历我的动态数量】")
    url = 'https://app.geely.com/api/v2/topicContent/queryMy'
    headers = {
        "Host": "app.geely.com",
        "accept": "application/json",
        "content-type": "application/json; charset=UTF-8",
        "devicesn": "356596585696247",
        "token": token
    }
    data = {
        "pageSize": 20,
        "contentType": 1,
        "userId": "4634864725442756864",
        "pageNum": 1
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    if result['code'] == 'success':
        id_list = []
        for item in result['data']['list']:
            id_list.append(item['id'])
        print(id_list)
        return id_list
    else:    
        print(result)

#删除动态
def deleteContent():
    print("【【【【【【【删除动态】】】】】】】")
    id_list = queryMy()
    if len(id_list) == 0:
        print('动态数量为0，不进行删除')
        return
    url = 'https://app.geely.com/api/v2/topicContent/deleteContent'
    headers = {
        "Host": "app.geely.com",
        "accept": "application/json",
        "content-type": "application/json; charset=UTF-8",
        "devicesn": "356596585696247",
        "token": token
    }
    for id in id_list:
        data = {
            "id": id
        }
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        if result['code'] == 'success':
            print(f"删除{id}：{result['code']}")
        else:
            print(result)     

#查询用户信息
def current():
    print("【【【【【【【查询用户信息】】】】】】】")
    url = 'https://app.geely.com/api/v1/user/current'
    headers = {
        "Host": "app.geely.com",
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36/geelyApp/android/geelyApp",
        "token": token,
        "referer": "https://app.geely.com/app-h5/grow-up/?showTitleBar=0&needLogin=1&tabsIndex=0",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    if result['code'] == 'success':
        print(f"用户ID：{result['data']['userId']}")
        print(f"手机号：{result['data']['ucMemberProfileDto']['mobile']}")
        return result['data']['userId'], result['data']['ucMemberProfileDto']['mobile']
    else:
        send(title_name, f"账号{index + 1}：查询用户信息失败")
        print(result)
        return '', ''
    
#查询吉分
def available():
    print("【【【【【【【查询吉分】】】】】】】")
    url = 'https://app.geely.com/api/v1/point/available'
    headers = {
        "Host": "app.geely.com",
        "accept": "application/json",
        "devicesn": "356596585696247",
        "token": token
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    if result['code'] == 'success':
        assets = f"{phone}：{result['data']['availablePoint']}吉分\n"
        print(assets)
        return assets
    else:
        print(result)

#查询任务状态
def access():
    print("【【【【【【【查询任务状态】】】】】】】")
    url = 'https://app.geely.com/api/v1/point/access'
    headers = {
        "Host": "app.geely.com",
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36/geelyApp/android/geelyApp",
        "token": token,
        "content-type": "application/json",
        "origin": "https://app.geely.com",
        "referer": "https://app.geely.com/app-h5/grow-up/?showTitleBar=0&needLogin=1&tabsIndex=0",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    data = {
        "classify": 1,
        "taskClassifyId": 5,
        "pageIndex": "1",
        "pageSize": "20"
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    if result['code'] == 'success':
        for item in result['data']['dataList']:
            print(f"{item['taskName']}：{item['isFinish']}")
    else:
        print(result)
    
def ql_env_put(name, data, Remarks=None):
    fetch_env = get_envs(name)#查询环境变量信息
    if fetch_env:
        put_envs(fetch_env[0].get('id'), fetch_env[0].get('name'), data, Remarks)
        fetch2_env = get_envs(name)
        str_time = "变量修改时间：" + fetch2_env[0].get('timestamp') + "\n"
        return str_time
    else:
        print(f"未找到 {name} 变量")

def random_sleep(min_val, max_val):
    num = random.randint(min_val, max_val)
    print(f"等待{num}秒后继续>>>>>>>>>>>")
    time.sleep(num)

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
    
if __name__ == '__main__':
    env_name = "JLtoken"#变量名
    env_phone = "JLphone"#变量名
    title_name = '吉利汽车'
    msg = ""
    token_list = ""
    phone_list = ""
    index = 0
    quantity = ql_env(env_name)
    print (f"共找到{len(quantity)}个账号")
    queryByCircleOrTopic()
    for token in quantity:
        print(f"\n------------正在执行第{index + 1}个账号----------------")
        userId, phone = current()
        if len(userId) == 0:
            index += 1
            continue
        sign()
        create()
        random_sleep(10, 20)
        deleteContent()
        access()
        msg += available()
        if len(token_list) > 0 and len(phone_list) > 0:
            token_list += '\n' + token
            phone_list += '\n' + phone
        else:
            token_list += token
            phone_list += phone
        print(f"第{index + 1}个账号运行完成")
        index += 1
        if index < len(quantity):
            random_sleep(1, 200)
    msg += update_github_file(f"token/{title_name}/token_list.txt", token_list)
    msg += update_github_file(f"token/{title_name}/phone_list.txt", phone_list)
    send(title_name, msg)
