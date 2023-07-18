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
from sendNotify import send
from os import environ
appKey = 'e0ae89fb37b6151889c6de3ba6b84e0d3a67f52cd5767758d4186fefff8f763c'#headers参数
tenantid = '1501391403178266624'

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
#            send("刷新Authorization失败", f"账号{index + 1}")
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
#        send("刷新Authorization失败", f"账号{index + 1}")
        return None

def getMallToken():
    url = 'https://shop-wap.hozonauto.com/gateway/mallapi/userinfo/getMallToken'
    headers = {
        "Host": "shop-wap.hozonauto.com",
        "accessToken": f"Bearer {Authorization_new}",
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
#    print(result)
    orders = result['data']['records']  # 获取订单列表
    results = ''  # 初始化保存结果的变量
    for order in orders:
        order_item = order['listOrderItem'][0]  # 获取订单商品信息
        order_logistics = order['orderLogistics']  # 获取订单物流信息
        results += "商品名称：{}\n".format(order_item['spuName'])
        results += "收货地址：{}，{}，{}\n".format(order_logistics['userName'], order_logistics['telNum'], order_logistics['address'])
        results += "订单状态：{}\n".format(order['statusDesc'])
        results += "快递单号：{}\n".format(order_logistics['logisticsNo'])
        results += "状态：{}\n\n".format(order_item['statusDesc'])
    print(results)
    return results

def random_sleep(min_val, max_val):
    num = random.randint(min_val, max_val)
    print(f"等待{num}秒后继续>>>>>>>>>>>")
    time.sleep(num)

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
            print("变量未启用")
            sys.exit(1)
    else:
        print("未添加变量")
        sys.exit(0)
        
if __name__ == '__main__':
    Authorization_list = []
    msg = ''
    quantity1 = ql_env("NZmy_phone")
    quantity2 = ql_env("NZphone")
    quantity3 = ql_env("NZtoken")
    if len(quantity2) != len(quantity3):
        print("变量列表数量不相等")
        exit() # 停止运行
    credentials = dict(zip(quantity2, quantity3))
    print(credentials)
    for phone in quantity1:
        if phone in credentials:
            Authorization_list.append(credentials[phone])
        else:
            print(phone, "未找到此号码")
    if len(Authorization_list) > 0:
        print (f"共找到{len(Authorization_list)}个账号")
        for Authorization in Authorization_list:
            refresh_Authorization()
            msg += orderinfo()
        send('哪吒订单查询', msg)
