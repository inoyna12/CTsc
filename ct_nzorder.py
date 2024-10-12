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
import base64
import textwrap
import pandas as pd
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from notify import send

appVersion = "6.4.2"

filepath = "/ql/data/env/nzqc.json"
phone_lst = os.getenv("nzphone").split('\n')
with open(filepath, 'r') as f:
    all_data = json.load(f)

def send_request(method, url, **kwargs):
    time_out = 10  # 请求超时
    try:
        method = method.upper()
        if method not in ['GET', 'POST', 'PUT']:
            raise ValueError(f"不支持 {method} 请求方法")
            return False
        response = requests.request(method, url, timeout=time_out, **kwargs)
        return response.json()
    except requests.exceptions.Timeout as e:
        print("请求超时:", str(e))
    except requests.exceptions.RequestException as e:
        print("请求错误:", str(e))
    except ValueError as e:
        print("值错误:", str(e))
    except Exception as e:
        print("其他错误:", str(e))
    return False

def days_difference(time_str):
    """
    计算当前时间与传入时间的整数天数差异。

    :param time_str: 时间字符串，格式为 'YYYY-MM-DDTHH:MM:SS'
    :return: 当前时间比传入时间大的整数天数，如果传入时间在未来，则返回负数
    """
    # 定义时间格式
    time_format = "%Y-%m-%dT%H:%M:%S"
    
    try:
        # 将字符串转换为 datetime 对象
        given_time = datetime.strptime(time_str, time_format)
        
        # 获取当前时间
        current_time = datetime.now()
        
        # 计算时间差
        time_difference = current_time - given_time
        
        # 将时间差转换为整数天数
        days_diff = time_difference.days
        
        return days_diff
    
    except ValueError as e:
        print(f"时间格式错误: {e}")
        return None

class Order:
    def __init__(self):
        self.appKey = 'e0ae89fb37b6151889c6de3ba6b84e0d3a67f52cd5767758d4186fefff8f763c'
        self.sign_str = '8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'
        self.tenant_id = '1501391403178266624'
        self.orderKey = 'HOZON-AES-KEY-EN'
        self.brand_model = pd.read_csv('utils/brand_model.csv')

    def sha256_encode(self, mystr):
        hash_object = hashlib.sha256(mystr.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def aes_ecb_decrypt(self, key, encrypted_text):
        key_bytes = key.encode('utf-8')
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        decrypted_padded = cipher.decrypt(base64.b64decode(encrypted_text))
        decrypted = unpad(decrypted_padded, AES.block_size)
        return decrypted.decode('utf-8')

    def refreshApiToken(self, refreshToken):
        url = 'https://appapi-pki.chehezhi.cn/customer/account/info/refreshApiToken'
        random_row = self.brand_model.sample(n=1)
        brand = random_row['brand'].values[0]
        self.model = random_row['model'].values[0]
        nonce = random_number = ''.join(random.choices('0123456789', k=10))
        timestamp = int(time.time() * 1000)
        sign = f"POST%2Fcustomer%2Faccount%2Finfo%2FrefreshApiTokenappid%3AHOZON-B-xKrgEvMtappkey%3A{self.appKey}nonce%3A{nonce}timestamp%3A{timestamp}refreshtoken%3A{refreshToken}{self.sign_str}"
        headers = {
                "Authorization": refreshToken,
                "appId": "HOZON-B-xKrgEvMt",
                "appKey": self.appKey,
                "appVersion": appVersion,
                'login_channel': '1',
                'channel': 'android',
                "nonce": str(nonce),
                "phoneModel": f"{brand} {self.model}",
                "timestamp": str(timestamp),
                "sign": self.sha256_encode(sign),
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "appapi-pki.chehezhi.cn:18443"
        }
        data = f"refreshToken={refreshToken}"
        result = send_request('POST', url, headers=headers, data=data)
        if result:
            if result['code'] == 20000:
                self.Authorization = result['data']['access_token']
                return True
 
    def getorderinfo(self):
        url = "https://shop-wap.hozonauto.com/gateway/mallapi/orderinfo/page?searchCount=false&current=1&size=10&descs=create_time"
        headers = {
            "Host": "shop-wap.hozonauto.com",
            "Connection": "keep-alive",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Android WebView";v="127", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?1",
            "Authorization": f"Bearer {self.Authorization}",
            "User-Agent": f"Mozilla/5.0 (Linux; Android 12; {self.model} Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.103 Mobile Safari/537.36",
            "third-session": "",
            "app-id": "",
            "tenant-id": self.tenant_id,
            "client-type": "H5",
            "sec-ch-ua-platform": '"Android"',
            "Accept": "*/*",
            "X-Requested-With": "com.hezhong.nezha",
            "Sec-Fetch-Site": "same-origin",
            "Referer": "https://shop-wap.hozonauto.com/review/pages/order/list",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        result = send_request('GET', url, headers=headers)
        if result:
            if result['code'] == 0:
                results = json.loads(self.aes_ecb_decrypt(self.orderKey, result['data']))
                for i in results['records']:
                    orderStatus = i['listOrderItem'][0]['statusDesc']
                    quantity = i['listOrderItem'][0]['quantity']
                    userName = i['orderLogistics']['userName']
                    telNum = i['orderLogistics']['telNum']
                    address = i['orderLogistics']['address']
                    createTime = i['orderLogistics']['createTime']
                    if i['status'] == '3' or days_difference(createTime) > 7:
                        """
                        ['status']：
                        1：待发货
                        2：待收货
                        3：已完成
                        5：已取消
                        """
                        continue
                    print(f"商品：{i['name']}*{quantity}")
                    print(f"收货地址：{userName} {telNum} {address}")
                    print(f"订单状态：{orderStatus}")
                    if i['status'] == '1':
                        print(f"快递状态：{i['statusDesc']}")
                    elif i['status'] == '2':
                        print(f"快递状态：{i['orderLogistics']['logisticsDesc']} {i['orderLogistics']['logisticsNo']}")
                    elif i['status'] == '5':
                        pass
                    else:
                        print(results)
                        exit()

    def main(self, refreshtoken):
        if self.refreshApiToken(refreshtoken):
            self.getorderinfo()
     
if __name__ == '__main__':
    order = Order()
    for phone in phone_lst:
        print(f"\n{phone}：")
        for dct in all_data:
            if dct['mobile'] == phone:
                order.main(dct['refresh_token'])
        time.sleep(3)
