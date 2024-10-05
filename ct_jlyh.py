'''
cron: 36 6 * * *
new Env('吉利银河');
'''
import requests
import datetime
import time
import uuid
import textwrap
import hmac
import hashlib
import base64
import json
import random
import string
import os
from urllib.parse import urlparse
from github import Github
from notify import send

title_name = "吉利银河"
appVersion = "1.22.1"

filepath = "/ql/data/env/jlyh.json"
with open(filepath, 'r') as f:
    all_data = json.load(f)

# 签到，分享，获取积分, 遍历帖子
key = {'x-ca-key': '204453306', 'secret-key': 'uUwSi6m9m8Nx3Grx7dQghyxMpOXJKDGu'}
# 刷新token
key2 = {'x-ca-key': '204179735', 'secret-key': 'UhmsX3xStU4vrGHGYtqEXahtkYuQncMf'}

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

class Jlyh:
    def __init__(self):
        self.date_md = datetime.datetime.now().strftime("%m-%d")
        self.id_list = self.get_id()
        self.fail = 0
        

    
    def newList(self, lst):
        new_lst = sorted(lst, key=lambda x: int(x['availablePoints']), reverse=True)
        return new_lst
                  
    def getProxy(self):
        url = 'http://v2.api.juliangip.com/company/postpay/getips?num=1&pt=1&result_type=json&trade_no=6130652715138961&sign=3b1896626239e61a182b00ac5582d07f'
        testurl = "https://www.juliangip.com/api/general/Test"
        for i in range(5):
            result = send_request('GET', url)
            if result:
                if result['code'] == 200:
                    proxy_ip = result['data']['proxy_list'][0]
                    print("代理：" + proxy_ip)
                    self.proxies = {
                      "http": proxy_ip,
                      "https": proxy_ip,
                    }
                    res = send_request('GET', testurl, proxies=self.proxies)
                    if res:
                        if res['state'] == 'ok':
                            return True
                    print(f"{self.proxies['http']}：连接失败！！！")
                else:
                    print(result)
            time.sleep(60)      
        send(title_name + "---异常", "获取代理IP失败！")
        exit()

    def hmacSHA256(self, key, message):
        hmac_obj = hmac.new(key.encode(), message.encode(), hashlib.sha256)
        hmac_digest = hmac_obj.digest()
        hmac_base64 = base64.b64encode(hmac_digest).decode()
        return hmac_base64

    def md5Base64(self, content):
        md5_hash = hashlib.md5(content.encode()).digest()
        base64_encoded = base64.b64encode(md5_hash).decode()
        return base64_encoded

    def s_s_info(self, str_dict):
        sweet_security_info = json.loads(str_dict)
        sweet_security_info['appVersion'] = appVersion
        sweet_security_info['battery'] = str(random.randint(20, 99))
        s_info = json.dumps(sweet_security_info, separators=(',', ':'))
        return s_info
            
    def refreshtoken(self, my_dict):
        url = f"https://galaxy-user-api.geely.com/api/v1/login/refresh?refreshToken={my_dict['refreshToken']}"
        now = datetime.datetime.now(datetime.timezone.utc)
        date = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
        x_ca_timestamp = str(int(now.timestamp() * 1000))
        x_ca_nonce = str(uuid.uuid4())
        url_path = urlparse(url).path
        x_ca_signature = textwrap.dedent(f"""\
            GET
            application/json; charset=utf-8
            
            application/x-www-form-urlencoded; charset=utf-8
            {date}
            x-ca-appcode:galaxy-app-user
            x-ca-key:{key2['x-ca-key']}
            x-ca-nonce:{x_ca_nonce}
            x-ca-timestamp:{x_ca_timestamp}
            {urlparse(url).path}?{urlparse(url).query}\
        """).strip()
        x_ca_signature = self.hmacSHA256(key2['secret-key'], x_ca_signature)
        headers = {
            'date': date,
            'x-ca-signature': x_ca_signature,
            'x-ca-appcode': 'galaxy-app-user',
            'x-ca-nonce': x_ca_nonce,
            'x-ca-key': key2['x-ca-key'],
            'ca_version': '1',
            'accept': 'application/json; charset=utf-8',
            'x-ca-timestamp': x_ca_timestamp,
            'tenantid': '569001701001',
            'host': 'galaxy-user-api.geely.com',
            'x-ca-signature-headers': 'x-ca-appcode,x-ca-nonce,x-ca-timestamp,x-ca-key',
            'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
            'user-agent': 'ALIYUN-ANDROID-UA',
            'deviceSN': "",
            'appId': 'galaxy-app',
            'appVersion': appVersion,
            'platform': 'Android',
            'Cache-Control': 'no-cache',
            'Connection': 'Keep-Alive'
        }
        result = send_request('GET', url, headers=headers, proxies=self.proxies)
        if result:
            print(f"刷新token：{result['message']}")
            if result['code'] == 'success' and result['message'] == '接口调用成功':
                self.token = result['data']['centerTokenDto']['token']
                my_dict['refreshToken'] = result['data']['centerTokenDto']['refreshToken']
                return True
            elif result['code'] == 'user_refresh_invalid_expired':
                invalid_list = gh_invalid.content
                for i in invalid_list:
                    if i['phone'] == my_dict['phone']:
                        print("号码已存在，不加入")
                        break
                else:
                    dict_new = {
                        'phone': my_dict['phone'],
                        'password': my_dict['password']
                    }
                    invalid_list.append(dict_new)
            else:
                print(result)
                send(title_name + "==停止运行", str(result))
                exit()
                
    def signAdd(self, my_dict):
        url = 'https://galaxy-app.geely.com/app/v1/sign/add'
        now = datetime.datetime.now(datetime.timezone.utc)
        date = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
        x_ca_timestamp = str(int(now.timestamp() * 1000))
        x_ca_nonce = str(uuid.uuid4())
        body = {
            "headers":{
                "appVersion":appVersion,
                "methodType":"6",
                "use_security":"true"
            },
            "signType":0
        }
        str_body = json.dumps(body, separators=(',', ':'))
        md5_base64 = self.md5Base64(str_body)
        x_ca_signature = textwrap.dedent(f"""\
            POST
            application/json; charset=utf-8
            {md5_base64}
            application/json; charset=utf-8
            {date}
            x-ca-appcode:SWGeelyCode
            x-ca-key:{key['x-ca-key']}
            x-ca-nonce:{x_ca_nonce}
            x-ca-timestamp:{x_ca_timestamp}
            {urlparse(url).path}\
        """).strip()
        x_ca_signature = self.hmacSHA256(key['secret-key'], x_ca_signature)
        
        headers = {
            'date': date,
            'x-ca-signature': x_ca_signature,
            'x-ca-appcode': 'SWGeelyCode',
            'x-ca-nonce': x_ca_nonce,
            'x-ca-key': key['x-ca-key'],
            'methodtype': '6',
            'ca_version': '1',
            'contenttype': 'application/json',
            'accept': 'application/json; charset=utf-8',
            'usetoken': '1',
            'content-md5': md5_base64,
            'x-ca-timestamp': x_ca_timestamp,
            'host': 'galaxy-app.geely.com',
            'x-ca-signature-headers': 'x-ca-appcode,x-ca-nonce,x-ca-key,x-ca-timestamp',
            'x-refresh-token': 'true',
            'user-agent': 'ALIYUN-ANDROID-UA',
            'token': self.token,
            'imei': my_dict['imei'],
            'os': '12',
            'sweet_security_info': self.sweet_security_info,
            'deviceSN': my_dict['deviceSN'],
            'appId': 'galaxy-app',
            'appVersion': appVersion,
            'platform': 'Android',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json; charset=utf-8',
            'Connection': 'Keep-Alive'
        }
        result = send_request('POST', url, headers=headers, data=str_body, proxies=self.proxies)
        if result:
            if result['msg'] == 'SUCCESS' and "success":
                if result['mysteryBoxPopFlag']:
                    print(f"签到：{result['mysteryBoxPopFlag'][0]['prizeContent']}")
                else:
                    print(f"签到：{result['msg']}")
                my_dict['signdate'] = self.date_md
                return
            elif result['msg'] == '今日已签到':
                my_dict['signdate'] = self.date_md
                print(result)
            else:
                print(result)
                exit()
            
    def get_id(self):
        url = 'https://galaxy-app.geely.com/app/v1/social/circle/channel/square/page'
        now = datetime.datetime.now(datetime.timezone.utc)
        date = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
        x_ca_timestamp = str(int(now.timestamp() * 1000))
        x_ca_nonce = str(uuid.uuid4())
        
        body = {
            "pageSize": 20,
            "type": 2,
            "pageNum": 1
        }
        str_body = json.dumps(body, separators=(',', ':'))
        md5_base64 = self.md5Base64(str_body)
        x_ca_signature = textwrap.dedent(f"""\
            POST
            application/json; charset=utf-8
            {md5_base64}
            application/json; charset=utf-8
            {date}
            x-ca-appcode:SWGeelyCode
            x-ca-key:{key['x-ca-key']}
            x-ca-nonce:{x_ca_nonce}
            x-ca-timestamp:{x_ca_timestamp}
            {urlparse(url).path}\
        """).strip()
        x_ca_signature = self.hmacSHA256(key['secret-key'], x_ca_signature)
        
        headers = {
            'date': date,
            'x-ca-signature': x_ca_signature,
            'x-ca-appcode': 'SWGeelyCode',
            'x-ca-nonce': x_ca_nonce,
            'x-ca-key': key['x-ca-key'],
            'ca_version': '1',
            'accept': 'application/json; charset=utf-8',
            'content-md5': md5_base64,
            'x-ca-timestamp': x_ca_timestamp,
            'host': 'galaxy-app.geely.com',
            'x-ca-signature-headers': 'x-ca-appcode,x-ca-nonce,x-ca-key,x-ca-timestamp',
            'x-refresh-token': 'true',
            'user-agent': 'ALIYUN-ANDROID-UA',
            'appId': 'galaxy-app',
            'appVersion': appVersion,
            'platform': 'Android',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json; charset=utf-8',
            'Connection': 'Keep-Alive'
        }
        result = send_request('POST', url, headers=headers, data=str_body)
        if result:
            id_list = []
            for i in result['data']['list']:
                text_data = i.get('longtext') or i.get('dynamic')
                if text_data:
                    createTime = text_data.get('createTime')
                    id_list.append(text_data['id'])
                    print(createTime)
                    print(len(id_list))
            if len(id_list) > 10:
                return id_list
        exit()
                
    def share(self, my_dict):
        content_id = random.choice(self.id_list)
        url = 'https://galaxy-app.geely.com/h5/v1/square/content/share'
        now = datetime.datetime.now(datetime.timezone.utc)
        date = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
        x_ca_timestamp = str(int(now.timestamp() * 1000))
        x_ca_nonce = str(uuid.uuid4())
        
        body = {
            "shareCode": "",
            "headers": {
                "appVersion": appVersion,
                "methodType": "5",
                "use_security": "true"
            },
            "openTimeStamp": int(x_ca_timestamp),
            "shareMethod": "2",
            "shareContentURL": f"https://galaxy-h5.geely.com/galaxy-app-h5/pages/dynamic_detail/dynamic_detail?isCordova=1&showTitleBar=0&id={content_id}",
            "shareContentType": 2
        }
        str_body = json.dumps(body, separators=(',', ':'))
        md5_base64 = self.md5Base64(str_body)
        x_ca_signature = textwrap.dedent(f"""\
            POST
            application/json; charset=utf-8
            {md5_base64}
            application/json; charset=utf-8
            {date}
            x-ca-appcode:SWGeelyCode
            x-ca-key:{key['x-ca-key']}
            x-ca-nonce:{x_ca_nonce}
            x-ca-timestamp:{x_ca_timestamp}
            {urlparse(url).path}\
        """).strip()
        x_ca_signature = self.hmacSHA256(key['secret-key'], x_ca_signature)
        
        headers = {
            'date': date,
            'x-ca-signature': x_ca_signature,
            'x-ca-appcode': 'SWGeelyCode',
            'x-ca-nonce': x_ca_nonce,
            'x-ca-key': key['x-ca-key'],
            'methodtype': '5',
            'ca_version': '1',
            'contenttype': 'application/json',
            'accept': 'application/json; charset=utf-8',
            'usetoken': '1',
            'content-md5': md5_base64,
            'x-ca-timestamp': x_ca_timestamp,
            'host': 'galaxy-app.geely.com',
            'x-ca-signature-headers': 'x-ca-appcode,x-ca-nonce,x-ca-key,x-ca-timestamp',
            'x-refresh-token': 'true',
            'user-agent': 'ALIYUN-ANDROID-UA',
            'token': self.token,
            'imei': my_dict['imei'],
            'os': '12',
            'sweet_security_info': self.sweet_security_info,
            'deviceSN': my_dict['deviceSN'],
            'appId': 'galaxy-app',
            'appVersion': appVersion,
            'platform': 'Android',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json; charset=utf-8',
            'Connection': 'Keep-Alive'
        }
        result = send_request('POST', url, headers=headers, data=str_body, proxies=self.proxies)
        if result:
            print(f"分享：{result['msg']}")
            if result['msg'] == 'SUCCESS' and "success":
                pass
            else:
                print(result)
                exit()
            
    def getPoints(self, my_dict):
        url = 'https://galaxy-app.geely.com/h5/v1/points/get'
        now = datetime.datetime.now(datetime.timezone.utc)
        date = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
        x_ca_timestamp = str(int(now.timestamp() * 1000))
        x_ca_nonce = str(uuid.uuid4())
        x_ca_signature = textwrap.dedent(f"""\
            GET
            application/json; charset=utf-8
            
            application/x-www-form-urlencoded; charset=utf-8
            {date}
            x-ca-appcode:SWGeelyCode
            x-ca-key:{key['x-ca-key']}
            x-ca-nonce:{x_ca_nonce}
            x-ca-timestamp:{x_ca_timestamp}
            {urlparse(url).path}\
        """).strip()
        x_ca_signature = self.hmacSHA256(key['secret-key'], x_ca_signature)
        headers = {
            'date': date,
            'x-ca-signature': x_ca_signature,
            'x-ca-appcode': 'SWGeelyCode',
            'x-ca-nonce': x_ca_nonce,
            'x-ca-key': key['x-ca-key'],
            'ca_version': '1',
            'contenttype': 'application/json',
            'accept': 'application/json; charset=utf-8',
            'usetoken': '1',
            'x-ca-timestamp': x_ca_timestamp,
            'host': 'galaxy-app.geely.com',
            'x-ca-signature-headers': 'x-ca-appcode,x-ca-nonce,x-ca-key,x-ca-timestamp',
            'x-refresh-token': 'true',
            'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
            'user-agent': 'ALIYUN-ANDROID-UA',
            'token': self.token,
            'deviceSN': my_dict['deviceSN'],
            'appId': 'galaxy-app',
            'appVersion': appVersion,
            'platform': 'Android',
            'Cache-Control': 'no-cache',
            'Connection': 'Keep-Alive'
        }
        result = send_request('GET', url, headers=headers, proxies=self.proxies)
        if result:
            if result['msg'] == 'SUCCESS':
                my_dict['availablePoints'] = result['data']['availablePoints']
                print(f"吉分：{result['data']['availablePoints']}")
            else:
                print(result)
                exit()
              
    def main(self, index, my_dict):
        if self.fail >= 20:
            exit()
        self.sweet_security_info = self.s_s_info(my_dict['sweet_security_info'])
        self.index = index
        self.getProxy()
        if self.refreshtoken(my_dict):
            self.signAdd(my_dict)
            self.share(my_dict)
            self.getPoints(my_dict)
            with open(filepath, 'w') as f:
                json.dump(all_data, f, indent=2)

if __name__ == '__main__':
    gh_jlyh = GithubFile('吉利银河/jlyh.json')
    gh_invalid = GithubFile('吉利银河/refreshTokenInvalid.json')
    jlyh = Jlyh()
    random.shuffle(all_data)
    for index, my_dict in enumerate(all_data, start = 1):
        print(f"\n{index}/{len(all_data)}{'➠'*10}{my_dict['phone']}：")
        if my_dict['signdate'] != jlyh.date_md:
            jlyh.main(index, my_dict)
            if index < len(all_data):
                randomSleep(30,60)
        else:
            print("已签到，跳过")
    gh_jlyh.update(jlyh.newList(all_data))
    if len(gh_invalid.content) > 0:
        gh_invalid.update(gh_invalid.content)
