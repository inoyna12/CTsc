'''
cron: 36 6 * * *
new Env('吉利汽车');
'''
import requests
import json
import os
import time
import random
import execjs
from datetime import datetime
from fake_useragent import UserAgent
from notify import send
from tools.tool import rts, randomSleep
from tools.githubFile import GithubFile
from tools.proxy import xiequ

title_name = '吉利汽车'
version = "3.24.0"

today_date = datetime.now().strftime("%m-%d")

filepath = "/ql/data/env/jlqc.json"
with open(filepath, 'r') as f:
    jlqc_list = json.load(f)
    
class Jlqc:
    def __init__(self):
        with open('utils/jlqc.js', 'r', encoding='utf-8') as file:
            js_code = file.read()
        self.js = execjs.compile(js_code)
        
        # 当前时间的"日"
        current_datetime = datetime.now()
        self.day = current_datetime.day
        
        
        self.expired_list = []
        self.error_list = []
        self.error = 0
        
        # 签到状态数量
        self.success = 0
        self.prize = 0
        self.id1 = 0
        self.id2 = 0
        self.id3 = 0
        self.tokenInvalid = 0

    def get_proxy(self):
        proxies = xiequ()
        if proxies:
            return proxies
        send(f"{title_name}_获取代理ip失败", "获取代理ip失败")
        exit()

    def sendMsg(self):
        msg = f'''
            账号总数：{jlqc_length}
            成功签到：{self.success}
            获得吉分：{self.prize}
            8吉分：{self.id1}
            16吉分：{self.id2}
            66吉分：{self.id3}
            token失效：{self.tokenInvalid}
        ''' + "\n\n" + '\n'.join(self.error_list)
        return msg
    
    def newList(self, lst):
        new_list = sorted(lst, key=lambda x: float(x['availablePoint']), reverse=True)
        return new_list
       
    def sign_UA(self):
        android_version = str(random.randint(7, 14))
        device_code = ''.join(random.choices('0123456789ABCDEF', k=8))
        build_number = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))
        return f"Dalvik/2.1.0 (Linux; U; Android {android_version}; {device_code} Build/{build_number})"  
        
    def available_UA(self):
        ua = UserAgent()
        base_ua = ua.chrome
        custom_ua = f"{base_ua} MQQBrowser/6.2 TBS/046281 Mobile Safari/537.36/android/geelyApp"
        return custom_ua   

    def sign(self, my_dict):
        url = 'https://app.geely.com/api/v1/userSign/sign/risk'
        for i in range(5):
            current_time = datetime.now()
            signDate = current_time.strftime("%Y-%m-%d %H:%M:%S")
            ts = int(time.time())
            body = {
                "signDate": str(signDate),
                "ts": ts,
                "cId":"BLqo2nmmoPgGuJtFDWlUjRI2b1b"
            }
            headers = {
                'Host': 'app.geely.com',
                'accept': 'application/json, text/plain, */*',
                'token': my_dict['token'],
                'version': version,
                'x-data-sign': self.js.call("enen", body),
                'User-Agent': self.sign_UA(),
                'content-type': 'application/json',
                'origin': 'https://app.geely.com',
                'referer': 'https://app.geely.com/app-h5/sign-in?showTitleBar=0',
                'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
            }
            result = rts('post', url, headers=headers, json=body, proxies=self.proxies)
            if result:
                if result['code'] == 'success' and 'msg' not in result['data']:
                    if not result['data']:
                        print("签到：" + result['code'])
                    elif 'id' in result['data']:
                        print("签到：" + result['data']['prizeName'])
                    self.success += 1
                    my_dict['signdate'] = today_date
                    return True
                elif result['message'] == '您已签到,请勿重复操作!':
                    my_dict['signdate'] = today_date
                    return True
                elif result['code'] == 'token.unchecked':
                    print(result)
                    createdict = {
                        'phone': my_dict['phone'],
                        'password': my_dict['password']
                    }
                    self.expired_list.append(createdict)
                    gh_expired.update(self.expired_list)
                    return False
                else:
                    print(result)
                    break
            else:
                self.proxies = self.get_proxy()
        send(f"{title_name}_签到失败", "签到失败")
        exit()
            
    def available(self, my_dict):
        url = 'https://app.geely.com/api/v1/point/available'
        headers = {
            "Host": "app.geely.com",
            "accept": "application/json, text/plain, */*",
            "user-agent": self.available_UA(),
            "token": my_dict['token'],
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        result = rts('get', url, headers=headers, proxies=self.proxies)
        if result:
            if result['code'] == "success":
                my_dict['availablePoint'] = result['data']['availablePoint']
                print(f"吉分：{result['data']['availablePoint']}")
                return
            else:
                print(result)
                send(title_name + "====停止运行", str(result))
                exit()      
        self.error += 1
        self.error_list.append(f"{self.index}：查询吉分失败")
            
    def refresh_token(self, my_dict):
        url = "https://app.geely.com/api/v1/user/refresh"
        params = {
            'refreshToken': my_dict['refreshToken']
        }
        headers = {
            "Host": "app.geely.com",
            "x-refresh-token": "true",
            "token": my_dict['token'],
            "appversion": version,
            "platform": "Android"
        }
        for i in range(5):
            result = rts('get', url, params=params, headers=headers, proxies=self.proxies)
            if result:
                if result['code'] == "success":
                    my_dict['token'] = result['data']['token']
                    my_dict['refreshToken'] = result['data']['refreshToken']
                    print(f"刷新token：{result['code']}")
                    return
                elif result['data'] == '登录已过期，请重新登录':
                    print(result)
                    createdict = {
                        'phone': my_dict['phone'],
                        'password': my_dict['password']
                    }
                    self.expired_list.append(createdict)
                    gh_expired.update(self.expired_list)
                    return
                else:
                    print(result)
                    break
            else:
                self.proxies = self.get_proxy()
        send(f"{title_name}_刷新token失败", "刷新token失败")
        exit()
                
    def main(self, index, my_dict):
        self.index = index
        self.proxies = self.get_proxy()
        
        if self.sign(my_dict):
            self.available(my_dict)
            if self.day in (1, 15):
                self.refresh_token(my_dict)

            if self.error > 20:
                send(f"{title_name}_错误次数过多", '\n'.join(self.error_list))
                exit()
  
if __name__ == '__main__':
    jlqc_length = len(jlqc_list)
    jlqc = Jlqc()
    gh_jlqc = GithubFile('吉利汽车/jlqc.json')
    gh_expired = GithubFile('吉利汽车/expired.json')
    random.shuffle(jlqc_list)
    for index, jlqc_dict in enumerate(jlqc_list, start=1):
        print(f"\n{index}/{jlqc_length}{'➠'*10}{jlqc_dict['phone']}：")
        if jlqc_dict['signdate'] != today_date:
            jlqc.main(index, jlqc_dict)
            with open(filepath, 'w') as f:
                json.dump(jlqc_list, f, indent=2)
            if index < jlqc_length:
                randomSleep(30,60)
        else:
            print("已签到，跳过")
    
    gh_jlqc.update(jlqc.newList(jlqc_list))
    send(title_name, jlqc.sendMsg())
