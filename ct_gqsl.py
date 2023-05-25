'''
cron: 21 9 * * *
new Env('广汽三菱');
'''

import requests
import os
import json
import time
import random
import hashlib
from sendNotify import send
from os import environ

#评论内容
text_list = ["真好，羡慕啊", "不错不错", "加油", "真漂亮", "赞👍", "赞一个", "挺好", "赞赞赞", "美好的一整天", "不错呢", "支持！顶", "给力了加油支持", "三菱汽车值得拥有！", "好好好好，赞赞赞赞，谢谢分享！", "不错嘛", "给力的", "美好生活"]

#签到
def sign():
    timestamp = (int(time.time() * 1000))
    sign = f"6b34c3a7b1c3f63c088defb563835aa1android3.0.0{timestamp}{authorization}"
    sign_md5 = get_md5_signature(sign)
    url = 'https://mspace.gmmc.com.cn/customer-app/task-mapi/sign-in?noLoad=true'
    headers = {
        'Host': 'mspace.gmmc.com.cn',
        'content-Length': '166',
        'accept': 'application/json, text/plain, */*',
        'authorization': authorization,
        'user-Agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046247 Mobile Safari/537.36 BundleId/com.gmmc.myspace DSApp/3.0.0 StatusBarHeight/26 BottomBarHeight/0',
        'content-Type': 'application/json;charset=UTF-8',
        'origin': 'https://mspace.gmmc.com.cn',
        'x-Requested-With': 'com.gmmc.myspace',
        'referer': 'https://mspace.gmmc.com.cn/points/points-task?goindex=1',
        'accept-Encoding': 'gzip, deflate, br',
        'accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    data = {
        'taskTypeCode': 'TASK-INTEGRAL-SIGN-IN',
        'step': 1,
        'sign': sign_md5,
        'timestamp': f"{timestamp}",
        'appVersion': '3.0.0',
        'operateSystem': 'android'
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
#    print (result)  
    if result['data']['isSignIn'] == True:
        isSignIn_day = f"成功签到第{result['data']['days']}天\n"  
    print (isSignIn_day)
    return isSignIn_day

#点赞
def liked_dynamic():
    status = ""
    url = "https://mspace.gmmc.com.cn/social-cms-app/frontend/dynamic/liked"
    headers = {
        "Host": "mspace.gmmc.com.cn",
        "accept": "application/json",
        "operatesystem": "android",
        "appversion": "3.0.0",
        "authorization": authorization,
        "dataencrypt": "false",
        "content-type": "application/json; charset=UTF-8",
        "content-length": "32",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.8.1"
    }
    dynamicId_list = query_community_content()
    for i in range(5):
        dynamicId = random.choice(dynamicId_list)
        data = {
        "dynamicId": dynamicId,
        "status": 1
        }
        dynamicId_list.remove(dynamicId)
        response = requests.post(url, headers=headers, data=json.dumps(data))
        result = response.json()
#        print (result)
        if result['data']['status'] == 1:
            print(f"点赞{dynamicId}：成功")
            status += f"点赞{dynamicId}：成功\n"
        if i < 4:
            random_sleep(20, 40)
    return status

#评论
def add_comment():
    url = "https://mspace.gmmc.com.cn/social-cms-app/frontend/comment/add"
    headers = {
        "Host": "mspace.gmmc.com.cn",
        "content-length": "95",
        "accept": "application/json, text/plain, */*",
        "authorization": authorization,
        "user-agent": "Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046247 Mobile Safari/537.36 BundleId/com.gmmc.myspace DSApp/3.0.0 StatusBarHeight/26 BottomBarHeight/0",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://mspace.gmmc.com.cn",
        "x-requested-with": "com.gmmc.myspace",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://mspace.gmmc.com.cn/topics/dynamic-detail?dynamicId=1832647&goindex=1",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    dynamicId_list = query_community_content()
    dynamicId = random.choice(dynamicId_list)
    data = {
    "commentContent": random.choice(text_list),
    "commentType": 2,
    "commentTypeBusinessId": dynamicId
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()
#    print (result)
    if result['success'] == True:
        success = f"评论{dynamicId}：成功\n"
    print (success)
    return success

#发动态
def add_dynamic():
    url = "https://mspace.gmmc.com.cn/social-cms-app/frontend/dynamic/add"
    headers = {
        "Host": "mspace.gmmc.com.cn",
        "accept": "application/json",
        "operatesystem": "android",
        "appversion": "3.0.0",
        "authorization": authorization,
        "dataencrypt": "false",
        "content-type": "application/json; charset=UTF-8",
        "content-length": "196",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.8.1"
    }
    content = juzi()
    data = {
    "activityId": 0,
    "backgroundContent": content,
    "btype": 0,
    "content": content,
    "lat": 0.0,
    "lng": 0.0
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()
#    print (result)
    if result['msg'] == "发布成功！":
        msg = f"发动态：{result['msg']}\n"
    print (msg)
    return msg

def user_info():
    url = "https://mspace.gmmc.com.cn/customer-app/customer/user/info"
    headers = {
        "Host": "mspace.gmmc.com.cn",
        "cache-control": "public, max-age=1",
        "accept": "application/json",
        "operatesystem": "android",
        "appversion": "3.0.0",
        "authorization": authorization,
        "dataencrypt": "false",
        "content-length": "0",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.8.1"
    }
    response = requests.post(url, headers=headers)
    result = response.json()
#    print (result)
    mobile = result['data']['mobile']
    integral = result['data']['integral']
    new_Phone = mobile[:3] + "****" + mobile[7:]
    info = f"{new_Phone}：{integral}积分\n"
    return info

#遍历社区最新动态id
def query_community_content():
    url = "https://mspace.gmmc.com.cn/social-cms-app/frontend/communityContent/queryByPage"
    headers = {
        "Host": "mspace.gmmc.com.cn",
        "accept": "application/json",
        "operatesystem": "android",
        "appversion": "3.0.0",
        "authorization": authorization,
        "dataencrypt": "false",
        "content-type": "application/json; charset=UTF-8",
        "content-length": "40",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.8.1"
    }
    data = {"queryType":1,"pageNo":1,"pageSize":20}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    result = response.json()
#    print (result)
    dynamicId_list = []#动态id列表
    for item in result['data']['list']:
        dynamicId_list.append(item['dynamicModel']['dynamicId'])
#    print (f"社区最新动态ID列表：\n{dynamicId_list}\n")
    return dynamicId_list
    
def random_sleep(min_val, max_val):
    num = random.randint(min_val, max_val)
    print(f"等待{num}秒后继续>>>>>>>>>>>")
    time.sleep(num)

def get_md5_signature(input_str):
    # 创建一个 hashlib.md5() 对象
    m = hashlib.md5()
    # 将输入字符串编码成 bytes 类型，并进行 MD5 计算
    m.update(input_str.encode('utf-8'))
    # 返回计算结果的十六进制表示
    return m.hexdigest()

def juzi():
    url = 'https://apis.tianapi.com/sentence/index?key=df2f1255dbccfadd606cf04d66aae277'
    response = requests.get(url=url)
    result = response.json()
    return result['result']['content']

def ql_env():
    if "gqsltoken" in os.environ:
        token_list = os.environ['gqsltoken'].split('\n')
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
    for authorization in quantity:
        print (f"------------正在执行第{index + 1}个账号----------------")
        msg += f"第{index + 1}个账号运行结果: \n"
        print("【签到】")
        msg += sign()
        random_sleep(20, 40)
        print("【点赞】")
        msg += liked_dynamic()
        random_sleep(20, 40)
        print("【评论】")
        msg += add_comment()
        random_sleep(20, 40)
        print("【发动态】")
        msg +=add_dynamic()
        random_sleep(20, 40)
        print("【查询】")
        msg += user_info()
        print(f"第{index + 1}个账号运行完成\n")
        index += 1
        if index < len(quantity):
            random_sleep(120, 240)
#    print(msg)
    send('广汽三菱', msg)