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
import datetime
from fake_useragent import UserAgent
from notify import send
from tools.tool import rts, randomSleep
from tools.githubFile import GithubFile
from tools.proxy import xiequ

title_name = '吉利汽车'
version = "3.24.0"

class JLQC:
    def __init__(self):
        with open('utils/jlqc.js', 'r', encoding='utf-8') as file:
            js_code = file.read()
        self.js = execjs.compile(js_code)
        
        # 当前时间的"日"
        current_datetime = datetime.datetime.now()
        self.day = current_datetime.day
        
        # 签到状态数量
        self.sign_true = 0
        self.todaysign = 0
        
        # github
        self.gh_jlqc = GithubFile('吉利汽车/jlqc.json')
        self.gh_expired = GithubFile('吉利汽车/expired.json')
        self.gh_ap100 = GithubFile('吉利汽车/ap100.json')
        self.gh_ap150 = GithubFile('吉利汽车/ap150.json')
        self.accoutExpired_list = []

    def get_proxy(self):
        proxies = xiequ()
        if proxies:
            return proxies
        send(f"{title_name}_获取代理ip失败", "获取代理ip失败")
        exit()

    def sendMsg(self):
        msg = f'''
            账号总数：{my_length}
            成功签到：{self.sign_true}
            token失效：{len(self.accoutExpired_list)}
        '''
        return msg
    
    def newList(self, lst):
        new_list = sorted(lst, key=lambda x: float(x['availablePoint']), reverse=True)
        return new_list
        
    def newAp(self, lst, ap):
        ap_list = []
        for dct in lst:
            if float(dct['availablePoint']) >= ap:
                createdict = {
                    'phone': dct['phone'],
                    'password': dct['password'],
                    'availablePoint': dct['availablePoint']
                }
                ap_list.append(createdict)
        return self.newList(ap_list)
       
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

    def sign(self):
        url = 'https://app.geely.com/api/v1/userSign/sign/risk'
        for i in range(5):
            current_time = datetime.datetime.now()
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
                        msg = result['code']
                    elif 'id' in result['data']:
                        msg = result['data']['prizeName']
                elif result['message'] == '您已签到,请勿重复操作!':
                    msg = result['message']
                elif result['code'] == 'token.unchecked':
                    print(result)
                    createdict = {
                        'phone': my_dict['phone'],
                        'password': my_dict['password']
                    }
                    self.accoutExpired_list.append(createdict)
                    self.gh_expired.update(self.accoutExpired_list)
                    return False
                else:
                    print(result)
                    break
                print(f"签到：{msg}")
                self.sign_true += 1
                my_dict['signdate'] = today_date
                return True
            else:
                self.proxies = self.get_proxy()
        send(f"{title_name}_签到失败", "签到失败")
        exit()
            
    def available(self):
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
            else:
                print(result)
                send(title_name + "====停止运行", str(result))
                exit()
            
    def refresh_token(self):
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
                elif result['data'] in ['登录已过期，请重新登录', '您的账号已在其他设备登录，如非本人操作，请及时修改密码']:
                    print(result)
                    createdict = {
                        'phone': my_dict['phone'],
                        'password': my_dict['password']
                    }
                    self.accoutExpired_list.append(createdict)
                    self.gh_expired.update(self.accoutExpired_list)
                    return
                else:
                    print(result)
                    break
            else:
                self.proxies = self.get_proxy()
        send(f"{title_name}_刷新token失败", "刷新token失败")
        exit()
                
    def main(self):
        self.proxies = self.get_proxy()
        if my_dict['signdate'] == yesterday_date:
            if self.sign():
                self.available()
        elif self.todaysign < 85:
            if self.sign():
                self.available()
                self.todaysign += 1
        else:
            print("签到数量超过85，跳过")
         
        if self.day in (1, 15):
            self.refresh_token()
        
        # if self.sign(my_dict):
            # self.available(my_dict)
            # if self.day in (1, 15):
                # self.refresh_token(my_dict)

            # if self.error > 20:
                # send(f"{title_name}_错误次数过多", '\n'.join(self.error_list))
                # exit()
  
if __name__ == '__main__':
    today_date = datetime.datetime.now().strftime("%m-%d")
    yesterday_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%m-%d")

    
    filepath = "/ql/data/env/jlqc.json"
    with open(filepath, 'r') as f:
        my_list = json.load(f)
    my_length = len(my_list)
    jlqc = JLQC()
    random.shuffle(my_list)
    
    for index, my_dict in enumerate(my_list, start=1):
        print(f"\n{index}/{my_length}{'➠'*10}{my_dict['phone']}：")
        if my_dict['signdate'] != today_date:
            jlqc.main()
            with open(filepath, 'w') as f:
                json.dump(my_list, f, indent=2)
            if index < my_length:
                randomSleep(30,60)
        else:
            print("已完成，跳过")
    
    jlqc.gh_jlqc.update(jlqc.newList(my_list))
    jlqc.gh_ap100.update(jlqc.newAp(my_list, 100))
    jlqc.gh_ap150.update(jlqc.newAp(my_list, 150))
    send(title_name, jlqc.sendMsg())
