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
from tools.tool import rts, randomSleep, proxy
from tools.githubFile import GithubFile

title_name = '吉利汽车'
version = "3.24.0"

juliang_url='http://v2.api.juliangip.com/postpay/getips?auto_white=1&num=1&pt=1&result_type=text&split=1&trade_no=6837909473421528&sign=783ee998438307f6d236ecc99dff6bc0'
juliang_testUrl='ttps://www.juliangip.com/api/general/Test'
xuequ_url='http://api.xiequ.cn/VAD/GetIp.aspx?act=get&uid=148434&vkey=1FB88D53032912792BD945D41B22AD0B&num=1&time=30&plat=1&re=1&type=2&so=1&ow=1&spl=1&addr=&db=1'
xiequ_testUrl='https://www.xiequ.cn/OnlyIp.aspx?yyy=123'

# 全局代理
def global_proxy(get_proxy_url, testUrl):
    proxies = proxy(juliang_url, juliang_testUrl)
    if proxies:
        os.environ["HTTP_PROXY"] = proxies['http']
        os.environ["HTTPS_PROXY"] = proxies['https']
        print(os.environ["HTTP_PROXY"], os.environ["HTTPS_PROXY"])
        return
    send(f"{title_name}_获取代理ip失败", "获取代理ip失败")
    exit()

def updateGithubFiles(data: list):
    availablePoint_50 = []
    availablePoint_100 = []
    new_data = sorted(data, key=lambda x: int(float(x['availablePoint'])), reverse=True)
    for i in new_data:
        if int(float(i['availablePoint'])) >= 100 and 'status' not in i:
            availablePoint_100.append(i)
        if int(float(i['availablePoint'])) >= 50 and i['password'] == '' and 'status' not in i:
            availablePoint_50.append(i)
    gh_jlqc.update(new_data)
    gh_availablePoint_50.update(availablePoint_50)
    gh_availablePoint_100.update(availablePoint_100)

class JLQC:
    def __init__(self):
        with open('utils/jlqc.js', 'r', encoding='utf-8') as file:
            js_code = file.read()
        self.js = execjs.compile(js_code)
        
        # 当前时间的"日"
        current_datetime = datetime.datetime.now()
        self.day = current_datetime.day
        
        # 签到成功数量
        self.sign_true = 0
        # 签到失败数量
        self.sign_fail = 0
        # 今日签到数量
        self.todaysign = 0
        # 账号跳过数量
        self.accout_skip = 0
        # token失效列表
        self.tokenExpired_list = []
        
    def get_proxy(self):
        proxies = juliang()
        if proxies:
            return proxies
        send(f"{title_name}_获取代理ip失败", "获取代理ip失败")
        exit()

    def sendMsg(self):
        msg = f'''
            账号总数：{my_length}
            成功签到：{self.sign_true}
            失败签到：{self.sign_fail}
            token失效：{len(self.tokenExpired_list)}
            跳过：{self.accout_skip}
            
            可用账号(50)：{len(gh_availablePoint_50.cont)}
            可用账号(100)：{len(gh_availablePoint_100.cont)}
        '''
        return msg
       
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
            ts = str(int(time.time()))
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
            result = rts('post', url, headers=headers, json=body)
            if result:
                print(result)
                if result['code'] == 'success' and 'msg' not in result['data'] or result['message'] == '您已签到,请勿重复操作!':
                    self.sign_true += 1
                    my_dict['signdate'] = today_date
                    return True
                elif result['code'] == 'token.unchecked':
                    my_dict['status'] = 'sign：token.unchecked'
                print("签到失败")
                self.sign_fail += 1
                return False
            else:
                global_proxy()
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
        result = rts('get', url, headers=headers)
        if result:
            if result['code'] == "success":
                availablePoint = result['data']['availablePoint']
                my_dict['availablePoint'] = availablePoint
                print(f"吉分：{availablePoint}")
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
            result = rts('get', url, params=params, headers=headers)
            if result:
                if result['code'] == "success":
                    my_dict['token'] = result['data']['token']
                    my_dict['refreshToken'] = result['data']['refreshToken']
                    print(f"刷新token：{result['code']}")
                    return
                elif result['data'] in ['登录已过期，请重新登录', '您的账号已在其他设备登录，如非本人操作，请及时修改密码']:
                    print(result)
                    my_dict['status'] = 'refreshToken expired'
                    self.tokenExpired_list.append(my_dict)
                    gh_expired.update(self.tokenExpired_list)
                    return
                else:
                    print(result)
                    break
            else:
                global_proxy()
        send(f"{title_name}_刷新token失败", "刷新token失败")
        exit()
                
    def main(self):
        global_proxy()
        if self.sign():
            self.available()
            if self.day in (1, 15):
                self.refresh_token()
                
        if self.sign_fail >= 10 or len(self.tokenExpired_list) >= 20:
            send(f"{title_name}_异常次数过多", "异常次数过多")
            exit()

        # self.proxies = self.get_proxy()
        # if my_dict['signdate'] == yesterday_date:
            # if self.sign():
                # self.available()
        # elif self.todaysign < 70:
            # if self.sign():
                # self.available()
                # self.todaysign += 1
        # else:
            # print("签到数量超过70，跳过")
         
        # if self.day in (1, 15):
            # self.refresh_token()
  
if __name__ == '__main__':
    jlqc = JLQC()
    gh_jlqc = GithubFile('吉利汽车/jlqc.json')
    gh_expired = GithubFile('吉利汽车/expired.json')
    gh_availablePoint_50 = GithubFile('吉利汽车/availablePoint_50.json')
    gh_availablePoint_100 = GithubFile('吉利汽车/availablePoint_100.json')

    today_date = datetime.datetime.now().strftime("%m-%d")
    yesterday_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%m-%d")

    filepath = "/ql/data/env/jlqc.json"
    with open(filepath, 'r') as f:
        my_list = json.load(f)
    my_length = len(my_list)
    random.shuffle(my_list)
    
    for index, my_dict in enumerate(my_list, start=1):
        print(f"\n{index}/{my_length}{'➠'*10}{my_dict['phone']}：")
        if my_dict['signdate'] != today_date and 'status' not in my_dict:
            jlqc.main()
            with open(filepath, 'w') as f:
                json.dump(my_list, f, indent=2)
            if index < my_length:
                randomSleep(5,30)
        else:
            jlqc.accout_skip += 1
            print("已完成，跳过")
        
    updateGithubFiles(my_list)
    send(title_name, jlqc.sendMsg())
