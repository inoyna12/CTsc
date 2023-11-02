'''
cron: 36 9 * * *
new Env('吉利汽车');
'''
import requests
import json
import time
import random
import datetime
import execjs
from sendNotify import send
from utils.github_api import update_github_file

js_code = open('utils/jlqc.js', 'r', encoding='utf-8').read()
js = execjs.compile(js_code)

#签到
def sign():
    print("【【【【【【【签到】】】】】】】")
    url = 'https://app.geely.com/api/v1/userSign/sign'
    for i in range(3):
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        current_timestamp = int(time.time())
        data = {
            "signDate": str(formatted_time),
            "ts": str(current_timestamp),
            "cId":"BLqo2nmmoPgGuJtFDWlUjRI2b1b"
        }
        headers = {
            'Host': 'app.geely.com',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36/geelyApp/android/geelyApp',
            'token': info['token'],
            'x-data-sign': js.call("enen", data),
            'content-type': 'application/json',
            'origin': 'https://app.geely.com',
            'referer': 'https://app.geely.com/app-h5/sign-in?showTitleBar=0',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        try:
            response = requests.post(url, headers=headers, json=data)
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
            if result['code'] == 'success':
                print(result['code'])
                if 'prizeName' in result['data']:
                    print(result['data']['prizeName'])
                info['sign'] = True
                return
            elif "已签到" in result['message']:
                print(result['message'])
                info['sign'] = True
                return
            elif i < 2:
                print(result)
                random_sleep(20, 40)
    msg_error.append(f"{index+1}签到异常")
        
#遍历
def queryForFollow():
    print("【遍历动态】")
    url = 'https://app.geely.com/api/v2/topicContent/queryForFollow'
    headers = {
        "Host": "app.geely.com",
        "accept": "application/json",
        "content-type": "application/json; charset=UTF-8",
        "devicesn": "356596585696247"
    }
    data = {
        "pageSize": 250,
        "followQueryType": 3,
        "pageNum": 1
    }
    for i in range(5):
        try:
            response = requests.post(url, headers=headers, json=data)
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
            for item in result['data']['list']:
                print("帖子内容：", item['content'])
                print(f"发帖时间：{item['createdTime']}，内容长度：{len(item['content'])}")
                if len(item['content']) > 5 and len(item['content']) < 25:
                    content_list.append(item['content'])
                else:
                    print("不加入")
            break
    print(content_list, len(content_list))

#发动态    
def create():
    print("【【【【【【【发布动态】】】】】】】")
    content = shiciapi()
    if content is None:
        print("随机一言获取失败，跳过发布动态")
        return
    url = 'https://app.geely.com/api/v2/topicContent/create'
    headers = {
        "Host": "app.geely.com",
        "accept": "application/json",
        "content-type": "application/json; charset=UTF-8",
        "devicesn": "356596585696247",
        "token": info['token']
    }
    data = {
        "circleId": None,
        "contentType": 1,
        "content": content,
        "fileList": [],
        "topicList": []
    }
    try:
        response = requests.post(url, headers=headers, json=data)
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
        if result['code'] == 'success':
            print(f"内容：{content} 发布结果：{result['code']}")
            return
        else:
            print(result)
    msg_error.append(f"{index+1}发布动态异常")
    
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
        "userId": "4634864725442756864",#需要改
        "pageNum": 1
    }
    for i in range(5):
        try:
            response = requests.post(url, headers=headers, json=data)
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
            if result['code'] == 'success':
                id_list = []
                for item in result['data']['list']:
                    id_list.append(item['id'])
                print(id_list)
                return id_list
            else:    
                print(result)
            break

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
        try:
            response = requests.post(url, headers=headers, json=data)
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
        "token": info['token'],
        "referer": "https://app.geely.com/app-h5/grow-up/?showTitleBar=0&needLogin=1&tabsIndex=0",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    for i in range(5):
        try:
            response = requests.get(url, headers=headers)
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
            if result['code'] == 'success':
                userId = result['data']['userId']#遍历发布的动态需要用到
                mobile = result['data']['ucMemberProfileDto']['mobile']
                print(f"用户ID：{userId}")
                print(f"手机号：{mobile}")
                info['mobile'] = mobile
                info['token_status'] = True
                return True
            elif result['code'] == 'token.unchecked':
                print(result)
                info['token_status'] = False
                msg_back.append(f"{info['mobile']}----{info['password']}")
                return False
            else:
                print(result)
                msg_error.append(f"{index+1}查询用户信息异常")
                return True
    return False
    
#查询吉分
def available():
    print("【【【【【【【查询吉分】】】】】】】")
    url = 'https://app.geely.com/api/v1/point/available'
    headers = {
        "Host": "app.geely.com",
        "accept": "application/json",
        "devicesn": "356596585696247",
        "token": info['token']
    }
    try:
        response = requests.get(url, headers=headers)
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
        if result['code'] == 'success':
            availablePoint = result['data']['availablePoint']
            acinfo = f"{info['mobile']}：{availablePoint}吉分"
            print(acinfo)
            info['availablePoint'] = availablePoint
            return
        else:
            print(result)
    msg_error.append(f"{index+1}查询吉分异常")

#查询任务状态
def access():
    print("【【【【【【【查询任务状态】】】】】】】")
    url = 'https://app.geely.com/api/v1/point/access'
    headers = {
        "Host": "app.geely.com",
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36/geelyApp/android/geelyApp",
        "token": info['token'],
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
    for i in range(5):
        try:
            response = requests.post(url, headers=headers, json=data)
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
            if result['code'] == 'success':
                for item in result['data']['dataList']:
                    print(f"{item['taskName']}：{item['isFinish']}")
                    if item['taskName'] == '发布动态/长图文':
                        info['create'] = item['isFinish'] 
            else:
                print(result)
            return

def random_sleep(min_val, max_val):
    num = random.randint(min_val, max_val)
    print(f"等待{num}秒后继续>>>>>>>>>>>")
    time.sleep(num)

def shiciapi():
    print("随机一言")
    url = "https://v1.jinrishici.com/all.json"
    try:
        response = requests.get(url)
        result = response.json()
    except Exception as e:
        print("异常:", e)
    else:
        if response.status_code == 200:
            return result['content']
        else:
            print(f"随机一言获取失败，状态码：{response.status_code}")
    return None

def msg_send():
    sorted_data = sorted(info_filtered, key=lambda x: float(x['availablePoint']), reverse=True)#从大到小排序
    for item in sorted_data:
        phone = item['mobile']
        availablePoint = item['availablePoint']
        password = item['password']
        msg.append(f"{phone}：{availablePoint}吉分")
        git_userpssd.append(phone + '----' + password)
        git_token.append(item['token'])
        git_phone.append(item['mobile'])
    send(f"{title_name}：{len(sorted_data)}", '\n'.join(msg))
    update_github_file(f"token/{title_name}/jlqc.json", info_filtered)
    update_github_file(f"token/{title_name}/phone_list.txt", '\n'.join(git_phone))
    update_github_file(f"token/{title_name}/token_list.txt", '\n'.join(git_token))
    update_github_file(f"token/{title_name}/账号密码.txt", '\n'.join(git_userpssd))
    if len(msg_error + msg_back) > 0:
        send(f"{title_name}异常", '\n'.join(msg_error + msg_back))
    
if __name__ == '__main__':
    title_name = '吉利汽车'
    filepath = "/ql/data/env/jlqc.json"
    msg = []
    msg_error = []
    msg_back = []
    git_token = []
    git_phone = []
    git_userpssd = []
    index = 0
    with open(filepath, 'r') as f:
        info_new = json.load(f)
    print(f"共找到{len(info_new)}个账号")
    for info in info_new:
        print(f"\n{'-' * 13}正在执行第{index + 1}个账号{'-' * 13}")
        if info['sign']:
            index += 1
            continue
        if current():
            sign() if not info['sign'] else print("已签到")
      #      create() if not info['create'] else print("已发布动态")
      #      random_sleep(20, 30)
      #      access()   
            available()
        with open(filepath, 'w') as f:
            json.dump(info_new, f)
        print(f"第{index + 1}个账号运行完成")
        index += 1
        if index < len(info_new):
            random_sleep(0, 100)
    info_filtered = [info for info in info_new if info["token_status"]]
    with open(filepath, 'w') as f:
        json.dump(info_filtered, f)
    msg_send()
