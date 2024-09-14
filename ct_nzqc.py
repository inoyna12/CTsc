'''
cron: 6 13 * * *
new Env('哪吒汽车');
'''
import requests
import os
import json
import time
import random
import hashlib
import datetime
import base64
import pandas as pd
from github import Github
from notify import send

title_name = '哪吒汽车'
appVersion = "6.4.2"

filepath = "/ql/data/env/nzqc.json"
with open(filepath, 'r') as f:
    all_data = json.load(f)

def randomSleep(min_val, max_val):
    num = random.randint(min_val, max_val)
    print(f"随机等待{num}秒后继续>>>>>>>>>>>")
    time.sleep(num)

def send_request(method, url, **kwargs):
    time_out = 10  # 请求超时
    try:
        method = method.upper()
        if method not in ['GET', 'POST', 'PUT']:
            raise ValueError(f"不支持 {method} 请求方法")
            return False
        response = requests.request(method, url, timeout=time_out, **kwargs)
        result = response.json()
        return result
    except requests.exceptions.Timeout as e:
        print("请求超时:", str(e))
    except requests.exceptions.RequestException as e:
        print("请求错误:", str(e))
    except ValueError as e:
        return response.text
    except Exception as e:
        print("其他错误:", str(e))
    return False

class GithubFile:
    def __init__(self, file_path):
        self.gh = Github(os.getenv('github_token'))
        self.repo = self.gh.get_repo('inoyna12/updateTeam')
        self.file_path = file_path
        self.commit_message = "Updated the file"
        self.file_info = self.repo.get_contents(self.file_path)

        # 检查文件大小
        if self.file_info.size > 1048576:  # 1MB 限制
            print(f"文件 {self.file_path} 大小超过限制，无法直接读取。")
            self.content = None
        else:
            self.content = json.loads(self.file_info.decoded_content.decode('utf-8'))
            print(f"读取 github {self.file_path} 文件成功！")

    def update(self, new_content):
        encoded_file_content = json.dumps(new_content, indent=2).encode('utf-8')

        try:
            self.repo.update_file(self.file_path, self.commit_message, encoded_file_content, self.file_info.sha)
            print(f"更新 github {self.file_path} 文件成功！")
        except Exception as e:
            print(f"更新文件时出错: {e}")

class Nzqc:
    def __init__(self):
        self.appKey = 'e0ae89fb37b6151889c6de3ba6b84e0d3a67f52cd5767758d4186fefff8f763c'
        self.sign_str = '8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'
        self.tenant_id = '1501391403178266624'
        self.orderKey = 'HOZON-AES-KEY-EN'
        self.date_md = datetime.datetime.now().strftime("%m-%d")
        self.brand_model = pd.read_csv('utils/brand_model.csv')

    def sha256encode(self, mystr):
        hash_object = hashlib.sha256(mystr.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def xiequProxy(self):
        url = 'http://api.xiequ.cn/VAD/GetIp.aspx?act=get&uid=148434&vkey=1FB88D53032912792BD945D41B22AD0B&num=1&time=30&plat=0&re=0&type=2&so=1&ow=1&spl=1&addr=&db=1'
        testurl = "https://www.xiequ.cn/OnlyIp.aspx?yyy=123"
        for i in range(5):
            result = send_request('GET', url)
            if result:
                if result['code'] == 0:
                    proxy_ip = result['data'][0]['IP']
                    proxy_port = result['data'][0]['Port']
                    print("代理：" + proxy_ip)
                    proxyMeta = "http://%(host)s:%(port)s" % {
                      "host" : proxy_ip,
                      "port" : proxy_port,
                    }
                    self.proxies = {
                      "http": proxyMeta,
                      "https": proxyMeta,
                    }
                    resp = send_request('GET', testurl, proxies=self.proxies)
                    if resp:
                        return True
                    print(f"{self.proxies['http']}：连接失败！！！")
                elif '白名单' in result['msg']:
                    print(result)
                    break
                else:
                    print(result)
            time.sleep(60)
        send(title_name + "---停止运行", "获取代理IP失败！")
        exit()

    def newList(self, lst):
        new_lst = sorted(lst, key=lambda x: x['creditScore'], reverse=True)
        return new_lst

    def refreshApiToken(self, mydict):
        url = 'https://appapi-pki.chehezhi.cn/customer/account/info/refreshApiToken'
        nonce  = ''.join(random.choices('0123456789', k=10))
        timestamp = int(time.time() * 1000)
        sign = f"POST%2Fcustomer%2Faccount%2Finfo%2FrefreshApiTokenappid%3AHOZON-B-xKrgEvMtappkey%3A{self.appKey}nonce%3A{nonce}timestamp%3A{timestamp}refreshtoken%3A{mydict['refresh_token']}{self.sign_str}"
        headers = {
                "Authorization": mydict['refresh_token'],
                "appId": "HOZON-B-xKrgEvMt",
                "appKey": self.appKey,
                "appVersion": appVersion,
                'login_channel': '1',
                'channel': 'android',
                "nonce": str(nonce),
                "phoneModel": f"{self.brand} {self.model}",
                "timestamp": str(timestamp),
                "sign": self.sha256encode(sign),
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "appapi-pki.chehezhi.cn:18443"
        }
        data = f"refreshToken={mydict['refresh_token']}"
        result = send_request('POST', url, headers=headers, data=data, proxies=self.proxies)
        if result:
            print(f"刷新token：{result['success']}")
            if result['code'] == 20000:
                self.Authorization = result['data']['access_token']
                mydict['refresh_token'] = result['data']['refresh_token']
                return True
            else:
                print(result)
                send(title_name + "---停止运行", "刷新token失败")
                exit()

    def sign(self, mydict):
        url = 'https://appapi-pki.chehezhi.cn/hznz/customer/sign'
        nonce  = ''.join(random.choices('0123456789', k=10))
        timestamp = int(time.time() * 1000)
        sign = f'GET%2Fhznz%2Fcustomer%2Fsignappid%3AHOZON-B-xKrgEvMtappkey%3A{self.appKey}nonce%3A{nonce}timestamp%3A{timestamp}{self.sign_str}'
        headers = {
            'appId': 'HOZON-B-xKrgEvMt',
            'appKey': self.appKey,
            'appVersion': appVersion,
            'login_channel': '1',
            'channel': 'android',
            'nonce': str(nonce),
            'phoneModel': f"{self.brand} {self.model}",
            'timestamp': str(timestamp),
            'sign': self.sha256encode(sign),
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': f'Mozilla/5.0 (Linux; U; Android 12; zh-cn; {self.model} Build/SKQ1.220303.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
            'Authorization': f"Bearer {self.Authorization}",
            'Host': 'appapi-pki.chehezhi.cn:18443',
            'Connection': 'Keep-Alive'
        }
        result = send_request('GET', url, headers=headers, proxies=self.proxies)
        if result:
            print(f"签到：{result['message']}")
            if result['code'] == 200 and "连续" in result['message']:
                mydict['signdate'] = self.date_md
            elif result['message'] == "请不要重复签到":
                pass
            else:
                print(result)
                send(title_name + "---停止运行", "签到失败")
                exit()

    def getCustomer(self, mydict):
        url = 'https://appapi-pki.chehezhi.cn/hznz/customer/getCustomer'
        nonce  = ''.join(random.choices('0123456789', k=10))
        timestamp = int(time.time() * 1000)
        sign = f'GET%2Fhznz%2Fcustomer%2FgetCustomerappid%3AHOZON-B-xKrgEvMtappkey%3A{self.appKey}nonce%3A{nonce}timestamp%3A{timestamp}{self.sign_str}'
        headers = {
            'appId': 'HOZON-B-xKrgEvMt',
            'appKey': self.appKey,
            'appVersion': appVersion,
            'login_channel': '1',
            'channel': 'android',
            'nonce': str(nonce),
            'phoneModel': f"{self.brand} {self.model}",
            'timestamp': str(timestamp),
            'sign': self.sha256encode(sign),
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': f'Mozilla/5.0 (Linux; U; Android 12; zh-cn; {self.model} Build/SKQ1.220303.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
            'Authorization': f"Bearer {self.Authorization}",
            'Host': 'appapi-pki.chehezhi.cn:18443',
            'Connection': 'Keep-Alive'
        }
        result = send_request('GET', url, headers=headers, proxies=self.proxies)
        if result:
            if result['message'] == "成功":
                creditScore = result['data']['creditScore']
                print(f"积分：{creditScore}")
                mydict['creditScore'] = creditScore
            else:
                print(result)

    def main(self, index, mydict):
        random_row = self.brand_model.sample(n=1)
        self.brand = random_row['brand'].values[0]
        self.model = random_row['model'].values[0]
        self.index = index
        self.xiequProxy()
        if self.refreshApiToken(mydict):
            self.sign(mydict)
            self.getCustomer(mydict)
            with open(filepath, 'w') as f:
                json.dump(all_data, f, indent=2)
     
if __name__ == '__main__':
    nzqc = Nzqc()
    gh_nzqc = GithubFile('哪吒汽车/nzqc.json')
    random.shuffle(all_data)
    for index, my_dict in enumerate(all_data, start = 1):
        print(f"\n{index}/{len(all_data)}{'➠'*10}{my_dict['mobile']}：")
        if my_dict['signdate'] != nzqc.date_md:
            nzqc.main(index, my_dict)
            if index < len(all_data):
                randomSleep(10,20)
        else:
            print("已签到，跳过")
    gh_nzqc.update(nzqc.newList(all_data))
