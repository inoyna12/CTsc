'''
cron: 36 6 * * *
new Env('吉利银河');
'''
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
from tools.tool import rts, randomSleep
from tools.githubFile import GithubFile
from tools.proxy import juliang
from urllib.parse import urlparse
from notify import send

title_name = "吉利银河"
appVersion = "1.23.1"

today_date = datetime.datetime.now().strftime("%m-%d")

filepath = "/ql/data/env/jlyh.json"
with open(filepath, 'r') as f:
    jlyh_list = json.load(f)

# 签到，分享，获取积分, 遍历帖子
key = {'x-ca-key': '204453306', 'secret-key': 'uUwSi6m9m8Nx3Grx7dQghyxMpOXJKDGu'}
# 刷新token
key2 = {'x-ca-key': '204179735', 'secret-key': 'UhmsX3xStU4vrGHGYtqEXahtkYuQncMf'}

class Jlyh:
    def __init__(self, expired):
        self.expired = expired
        self.expired_list = self.expired.lst
        self.error = 0
        self.error_list = []
        self.sign_success = 0
        self.share_success = 0
        self.id_list = self.get_id()
        
    def sendMsg(self):
        msg = f'''
            账号总数：{jlqc_length}
            成功签到：{self.sign_success}
            成功分享：{self.share_success}
        ''' + "\n\n" + '\n'.join(self.error_list)
        return msg  

    def get_proxy(self):
        proxies = juliang()
        if proxies:
            return proxies
        send(f"{title_name}_获取代理ip失败", "获取代理ip失败")
        exit()

    def newList(self, lst):
        new_lst = sorted(lst, key=lambda x: int(x['availablePoints']), reverse=True)
        return new_lst

    def hmacSHA256(self, key, message):
        hmac_obj = hmac.new(key.encode(), message.encode(), hashlib.sha256)
        hmac_digest = hmac_obj.digest()
        hmac_base64 = base64.b64encode(hmac_digest).decode()
        return hmac_base64

    def md5Base64(self, content):
        md5_hash = hashlib.md5(content.encode()).digest()
        base64_encoded = base64.b64encode(md5_hash).decode()
        return base64_encoded

    def new_s_s_info(self, str_dict):
        sweet_security_info = json.loads(str_dict)
        sweet_security_info['appVersion'] = appVersion
        sweet_security_info['battery'] = str(random.randint(20, 99))
        s_info = json.dumps(sweet_security_info, separators=(',', ':'))
        return s_info

    def get_id(self):
        url = 'https://galaxy-app.geely.com/app/v1/social/circle/channel/square/page'
        now = datetime.datetime.now(datetime.timezone.utc)
        date = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
        x_ca_timestamp = str(int(now.timestamp() * 1000))
        x_ca_nonce = str(uuid.uuid4())
        
        body = {
            "pageSize": 80,
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
        result = rts('post', url, headers=headers, data=str_body)
        if result:
            id_list = []
            for i in result['data']['list']:
                text_data = i.get('longtext') or i.get('dynamic')
                if text_data:
                    createTime = text_data.get('createTime')
                    id_list.append(text_data['id'])
                    print(createTime)
                    print(len(id_list))
            if len(id_list) > 50:
                return id_list
        send(f"{title_name}_获取id列表失败", "获取id列表失败")
        exit()
            
    def refreshtoken(self, my_dict):
        url = f"https://galaxy-user-api.geely.com/api/v1/login/refresh?refreshToken={my_dict['refreshToken']}"
        for i in range(5):
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
            result = rts('get', url, headers=headers, proxies=self.proxies)
            if result:
                print(f"刷新token：{result['code']}")
                if result['code'] == 'success' and result['message'] == '接口调用成功':
                    self.token = result['data']['centerTokenDto']['token']
                    my_dict['refreshToken'] = result['data']['centerTokenDto']['refreshToken']
                    return True
                elif result['code'] == 'user_refresh_invalid_expired':
                    for expired in self.expired_list:
                        if expired['phone'] == my_dict['phone']:
                            print("号码已存在，不加入")
                            break
                    else:
                        createdict = {
                            'phone': my_dict['phone'],
                            'password': my_dict['password']
                        }
                        self.expired_list.append(createdict)
                        self.expired.update(self.expired_list)
                else:
                    print(result)
                    break
            else:
                self.proxies = self.get_proxy()
        send(f"{title_name}_刷新token失败", "刷新token失败")
        exit()
                
    def signAdd(self, my_dict):
        url = 'https://galaxy-app.geely.com/app/v1/sign/add'
        for i in range(5):
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
            result = rts('port', url, headers=headers, data=str_body, proxies=self.proxies)
            if result:
                self.signStatus(result, my_dict)
                return
            else:
                self.proxies = self.get_proxy()
        send(f"{title_name}_签到失败", "签到失败")
        exit()

    def signStatus(self, result, my_dict):
        print(f"签到：{result['msg']}")
        if result['msg'] == 'SUCCESS' and "success":
            if result['data']['mysteryBoxPopFlag']:
                for box in result['data']['mysteryBoxPops']:
                    if box['mysteryBoxTitle'] == '7天签到盲盒(循环)':
                        print(f"{box['mysteryBoxTitle']}：{box['prizeContent']}")
                    elif box['mysteryBoxTitle'] == '30天签到盲盒':
                        self.openMysteryBox(my_dict, box['id'])
        elif result['msg'] == '今日已签到':
            pass
        else:
            print(result)
            send(f"{title_name}_签到失败", "未知响应体")
            exit()
        self.sign_success += 1
        my_dict['signdate'] = today_date

    def openMysteryBox(self, my_dict, userMysteryBoxId):
        url = 'https://galaxy-app.geely.com/app/v1/sign/openMysteryBox'
        for i in range(5):
            now = datetime.datetime.now(datetime.timezone.utc)
            date = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
            x_ca_timestamp = str(int(now.timestamp() * 1000))
            x_ca_nonce = str(uuid.uuid4())
            body = {
                "isLoading": False,
                "headers": {
                    "appVersion": appVersion,
                    "methodType": "7",
                    "use_security": "true"
                },
                "id": userMysteryBoxId
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
                'methodtype': '7',
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
                'deviceSN': my_dict['deviceSN'],
                'appId': 'galaxy-app',
                'appVersion': appVersion,
                'platform': 'Android',
                'Cache-Control': 'no-cache',
                'imei': my_dict['imei'],
                'os': '12',
                'sweet_security_info': self.sweet_security_info,
                'Content-Type': 'application/json; charset=utf-8',
                'Connection': 'Keep-Alive'
            }
            result = rts('post', url, headers=headers, data=str_body, proxies=self.proxies)
            if result:
                print(result)
                return
            else:
                self.proxies = self.get_proxy()
        send(f"{title_name}_开启宝箱失败", "开启宝箱失败")
        exit()
                
    # 获取盲盒状态
    def getBaseData(self, my_dict):
        url = 'https://galaxy-app.geely.com/app/v1/sign/getBaseData?isLoading=false'
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
            {urlparse(url).path + '?' + urlparse(url).query}\
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
        result = rts('GET', url, headers=headers, proxies=self.proxies)
        if result:
            for boxVos in result['data']['boxVos']:
                if boxVos['title'] == '30天签到盲盒':
                    if boxVos['mysteryBoxState'] == 1 and boxVos['mysteryBoxOpenState'] == 0:
                        print(result)
                        self.openMysteryBox(my_dict, boxVos['userMysteryBoxId'])
                
    def share(self, my_dict):
        url = 'https://galaxy-app.geely.com/h5/v1/square/content/share'
        for i in range(5):
            content_id = random.choice(self.id_list)
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
            result = rts('post', url, headers=headers, data=str_body, proxies=self.proxies)
            if result:
                print(f"分享：{result['msg']}")
                if result['msg'] == 'SUCCESS' and "success":
                    self.share_success += 1
                    return
            else:
                self.proxies = self.get_proxy()
        send(f"{title_name}_分享失败", "分享失败")
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
        result = rts('get', url, headers=headers, proxies=self.proxies)
        if result:
            if result['msg'] == 'SUCCESS':
                my_dict['availablePoints'] = result['data']['availablePoints']
                print(f"吉分：{result['data']['availablePoints']}")
                return
            else:
                print(result)
        self.error += 1
        self.error_list.append(f"{self.index}：查询积分失败")
              
    def main(self, index, my_dict):
        self.index = index
        self.proxies = self.get_proxy()
        self.sweet_security_info = self.new_s_s_info(my_dict['sweet_security_info']) 
        if self.refreshtoken(my_dict):
            self.signAdd(my_dict)
            self.share(my_dict)
            self.getPoints(my_dict)
            
        if self.error > 20:
            send(f"{title_name}_错误次数过多", '\n'.join(self.error_list))
            exit()

if __name__ == '__main__':
    jlqc_length = len(jlyh_list)
    random.shuffle(jlyh_list)
    gh_jlyh = GithubFile('吉利银河/jlyh.json')
    gh_expired = GithubFile('吉利银河/expired.json')
    jlyh = Jlyh(gh_expired)
    for index, my_dict in enumerate(jlyh_list, start = 1):
        print(f"\n{index}/{jlqc_length}{'➠'*10}{my_dict['phone']}：")
        if my_dict['signdate'] != today_date:
            jlyh.main(index, my_dict)
            with open(filepath, 'w') as f:
                json.dump(jlyh_list, f, indent=2)
            if index < jlqc_length:
                randomSleep(30,60)
        else:
            print("已签到，跳过")
     
    gh_jlyh.update(jlyh.newList(jlyh_list))
    send(title_name, jlyh.sendMsg())
