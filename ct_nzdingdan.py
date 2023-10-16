'''
cron: 6 13 * * *
new Env('哪吒订单查询');
'''
import requests
import os
import json
import time
import random
import hashlib
import io
import sys
import fcntl
import datetime
from sendNotify import send
from utils.github_api import update_github_file
appKey = 'e0ae89fb37b6151889c6de3ba6b84e0d3a67f52cd5767758d4186fefff8f763c'#headers参数
tenantid = '1501391403178266624'
sign_string = '8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'
appVersion = "5.5.2"

def refresh_Authorization():
    url = 'https://appapi-pki.chehezhi.cn/customer/account/info/refreshApiToken'
    for i in range(50):
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
                return
            else:
                print("刷新Authorization失败")
                print(result)
                send("刷新Authorization失败", f"账号{index + 1}")
                random_sleep(60, 80)
    send("刷新Authorization失败", f"账号{index + 1}")
    return None

def getMallToken():
    url = 'https://shop-wap.hozonauto.com/gateway/mallapi/userinfo/getMallToken'
    headers = {
        "Host": "shop-wap.hozonauto.com",
        "accessToken": f"Bearer {Authorization}",
        "tenant-id": tenantid,
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36",
        "client-type": "APP",
        "Content-Type": "application/json",
        "Origin": "https://shop-wap.hozonauto.com",
        "X-Requested-With": "com.hezhong.nezha",
        "Referer": f"https://shop-wap.hozonauto.com/pages/order/order-list/index?tenant_id={tenantid}",
    }
    response = requests.post(url=url, headers=headers)
    result = response.json()
    if result['code'] == 0:
        return result['data']['thirdSession']
    else:
        print(result)
        return None

def orderinfo():
    thirdsession = getMallToken()
    url = 'https://shop-wap.hozonauto.com/gateway/mallapi/orderinfo/page'
    params = {
        "searchCount": "false",
        "current": "1",
        "size": "10",
        "ascs": "",
        "descs": "create_time"
    }
    headers = {
        "Host": "shop-wap.hozonauto.com",
        "third-session": thirdsession,
        "tenant-id": tenantid,
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36",
        "Referer": f"https://shop-wap.hozonauto.com/pages/order/order-list/index?tenant_id={tenantid}"
    }
    response = requests.get(url=url, params=params, headers=headers)
    result = response.json()
   # print(result)
    records = result['data']['records'][0]
    total = result['data']['total']
    print("总订单数：" + str(total))
    printc(f"下单号码：{phone}({total})")
    printc(f"下单时间：{records['createTime']}")
    printc(f"商品名称：{records['name']}")
    printc("收货地址：{}，{}，{}".format(records['orderLogistics']['userName'], records['orderLogistics']['telNum'], records['orderLogistics']['address']))
    printc(f"快递状态：{records['statusDesc']} {records['updateTime']}")
    printc(f"订单状态：{records['listOrderItem'][0]['statusDesc']}")
    printc(f"快递单号：{records['orderLogistics']['logisticsNo']}\n")

def random_sleep(min_val, max_val):
    num = random.randint(min_val, max_val)
    print(f"等待{num}秒后继续>>>>>>>>>>>")
    time.sleep(num)

def sha256_encode(string):
    hash_object = hashlib.sha256(string.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig

def generate_random_number():
    random_number = ''.join(random.choices('0123456789', k=10))
    return random_number

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

def printc(text):
    print(text)  # 实时打印到控制台
    sys.stdout.flush()
    print(text, file=output)  # 存储到文件对象中
        
if __name__ == '__main__':
    output = io.StringIO()
    title_name = '哪吒汽车/下单日志'
    filepath = "/ql/data/env/nzqc.json"
    index = 0
    max_phone = ql_env("NZmy_phone")
    print(f"共找到{len(max_phone)}个账号")
    for max in max_phone:
        print(f"\n{'-' * 15}正在执行第{index + 1}个账号{'-' * 15}")
        file = open(filepath, 'r+')
        fcntl.flock(file.fileno(), fcntl.LOCK_EX)
        info_max = json.load(file)
        for info in info_max:
            if info['mobile'] == max:
                refresh_Authorization()
                file.seek(0)
                file.write(json.dumps(info_max))
                file.truncate()
                fcntl.flock(file.fileno(), fcntl.LOCK_UN)
                file.close()
                orderinfo()
                break
        index += 1
        if index < len(max_phone):
            random_sleep(1, 100)    
    msg = output.getvalue()
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    update_github_file(f"token/{title_name}/{current_time}.txt", msg)
    send('哪吒订单查询', msg)
