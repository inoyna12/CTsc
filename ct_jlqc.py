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
from github import Github
from notify import send

title_name = '吉利汽车'
version = "3.24.0"

filepath = "/ql/data/env/jlqc.json"
with open(filepath, 'r') as f:
    jlqc_list = json.load(f)

def randomSleep(min_val, max_val):
    num = random.randint(min_val, max_val)
    print(f"随机等待{num}秒后继续>>>>>>>>>>>")
    time.sleep(num)

class GithubFile:
    def __init__(self, file_path):
        self.gh = Github(os.getenv('github_token'))
        self.repo = self.gh.get_repo('inoyna12/updateTeam')
        self.file_path = file_path
        self.commit_message = f"Updated {file_path}"
        self.file_info = self.repo.get_contents(self.file_path)
        if self.file_info.size > 1048576:  # 1MB 限制
            print(f"文件 {self.file_path} 大小超过限制，无法直接读取。")
            self.lst = None
        else:
            self.lst = json.loads(self.file_info.decoded_content.decode('utf-8'))
            print(f"读取 github {self.file_path} 文件成功！")

    def update(self, new_lst):
        encoded_file_content = json.dumps(new_lst, indent=2).encode('utf-8')
        try:
            self.repo.update_file(self.file_path, self.commit_message, encoded_file_content, self.file_info.sha)
            print(f"更新 github {self.file_path} 文件成功！")
        except Exception as e:
            print(f"更新文件时出错: {e}")

class Jlqc:
    def __init__(self, quantity):
        self.quantity = quantity
        current_time = datetime.now()
        with open('utils/jlqc.js', 'r', encoding='utf-8') as file:
            js_code = file.read()
        self.js = execjs.compile(js_code)
        self.md = current_time.strftime("%m-%d")
        self.day = current_time.day
        self.error_list = []
        self.error = 0
        self.proxy_quantity = 0
        
        # github文件
        self.gh_jlqc = GithubFile('吉利汽车/jlqc.json')
        self.gh_jlqced = GithubFile('吉利汽车/expired.json')
        self.ed_list = self.gh_jlqced.lst
        
        # 签到状态数量
        self.success = 0
        self.prize = 0
        self.id1 = 0
        self.id2 = 0
        self.id3 = 0
        self.tokenInvalid = 0

    def rts(self, method, url, **kwargs):
        time_out = 10
        try:
            method = method.upper()
            if method not in ['GET', 'POST', 'PUT']:
                raise ValueError(f"不支持 {method} 请求方法")
            response = requests.request(method, url, timeout=time_out, **kwargs)
            try:
                return response.json()
            except ValueError:
                return response.text
        except requests.exceptions.Timeout as e:
            print(f"请求超时：{url}")
        except requests.exceptions.RequestException as e:
            print(f"请求错误：{url}")
        except Exception as e:
            print("其他错误:", str(e))
        return False

    def xiequProxy(self):
        url = 'http://api.xiequ.cn/VAD/GetIp.aspx?act=get&uid=148434&vkey=1FB88D53032912792BD945D41B22AD0B&num=1&time=30&plat=0&re=1&type=2&so=1&ow=1&spl=1&addr=&db=1'
        testUrl = "https://www.xiequ.cn/OnlyIp.aspx?yyy=123"
        for i in range(5):
            result = self.rts('get', url)
            if result and result['code'] == 0:
                self.proxy_quantity += 1
                ip = result["data"][0]["IP"]
                port = result["data"][0]["Port"]
                print(f"代理：{ip}")
                proxy = {
                    "http": f"http://{ip}:{port}",
                    "https": f"http://{ip}:{port}"
                }
                result = self.rts('get', testUrl, proxies=proxy)
                if result:
                    return proxy
            else:
                time.sleep(5)
        send(title_name + "---停止运行", "获取代理IP失败！")
        exit()

    def sendMsg(self):
        msg = f'''
            账号总数：{self.quantity}
            成功签到：{self.success}
            获得吉分：{self.prize}
            8吉分：{self.id1}
            16吉分：{self.id2}
            66吉分：{self.id3}
            token失效：{self.tokenInvalid}
            代理ip数量：{self.proxy_quantity}
        ''' + "\n\n" + '\n'.join(self.error_list)
        return msg  

    def gh_update(self, my_dict):
        self.tokenInvalid += 1
        for i in self.ed_list:
            if i['phone'] == my_dict['phone']:
                print("失效号码已在列表中")
                break
        else:
            dct = {
                'phone': my_dict['phone'],
                'password': my_dict['password']
            }
            self.edlst.append(dct)
            self.gh_jlqced.update(self.ed_list)
    
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
            result = self.rts('post', url, headers=headers, json=body, proxies=self.proxies)
            if result:
                return result
            else:
                self.proxies = self.xiequProxy()
        send(title_name + "====停止运行", "多次签到失败")
        exit()
                           
    def signstatus(self, my_dict):
        result = self.sign(my_dict)
        if result['code'] == 'success' and 'msg' not in result['data']:
            if not result['data']:
                print("签到：" + result['code'])
            elif 'id' in result['data']:
                if result['data']['id'] == '1':
                    self.id1 += 1
                    self.prize += 8
                elif result['data']['id'] == '2':
                    self.id2 += 1
                    self.prize += 16
                elif result['data']['id'] == '3':
                    self.id3 += 1
                    self.prize += 66
                print("签到：" + result['data']['prizeName'])
        elif result['code'] == 'fail' and result['message'] == '您已签到,请勿重复操作!':
            print("签到：" + result['message'])
            self.error_list.append(f"{self.index}：重复签到")
        elif result['code'] == 'token.unchecked':
            print("签到：" + result['code'])
            self.gh_update(my_dict)
            return False
        else:
            print(result)
            send(title_name + "====停止运行", str(result))
            exit()
        self.success += 1
        my_dict['signdate'] = self.md
        return True
            
    def available(self, my_dict):
        url = 'https://app.geely.com/api/v1/point/available'
        headers = {
            "Host": "app.geely.com",
            "accept": "application/json, text/plain, */*",
            "user-agent": self.available_UA(),
            "token": my_dict['token'],
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        result = self.rts('get', url, headers=headers, proxies=self.proxies)
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
            result = self.rts('get', url, params=params, headers=headers, proxies=self.proxies)
            if result:
                if result['code'] == "success":
                    my_dict['token'] = result['data']['token']
                    my_dict['refreshToken'] = result['data']['refreshToken']
                    print(f"刷新token：{result['code']}")
                    return
                elif result['data'] == '登录已过期，请重新登录':
                    self.gh_update(my_dict)
                    return
                else:
                    print(result)
                    send(title_name + "====停止运行", str(result))
                    exit()
        self.error += 1
        self.error_list.append(f"{self.index}：刷新token失败")
                
    def main(self, index, my_dict):
        self.index = index
        self.proxies = self.xiequProxy()
        if self.signstatus(my_dict):
            self.available(my_dict)
            if self.day in (1, 15):
                self.refresh_token(my_dict)

            if self.error > 20:
                send(title_name + "====停止运行", '\n'.join(self.error_list))
                exit()
  
if __name__ == '__main__':
    jlqc_quantity = len(jlqc_list)
    jlqc = Jlqc(jlqc_quantity)
    random.shuffle(jlqc_list)
    for index, jlqc_dict in enumerate(jlqc_list, start=1):
        print(f"\n{index}/{jlqc_quantity}{'➠'*10}{jlqc_dict['phone']}：")
        if jlqc_dict['signdate'] != jlqc.md:
            jlqc.main(index, jlqc_dict)
            with open(filepath, 'w') as f:
                json.dump(jlqc_list, f, indent=2)
            if index < jlqc_quantity:
                randomSleep(30,60)
        else:
            print("已签到，跳过")
            
    jlqc.gh_jlqc.update(jlqc.newList(jlqc_list))
    send(title_name, jlqc.sendMsg())
