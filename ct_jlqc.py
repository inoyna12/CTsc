'''
cron: 36 6 * * *
new Env('吉利汽车签到');
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

title_name = '吉利汽车签到'
version = "3.24.0"

filepath = "/ql/data/env/jlqc.json"
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
        self.content = json.loads(self.file_info.decoded_content.decode('utf-8'))
        print(f"读取gtihub {self.file_path} 文件成功！")
        
    def update(self, new_content):
        encoded_file_content = json.dumps(new_content, indent=2).encode('utf-8')
        self.repo.update_file(self.file_path, self.commit_message, encoded_file_content, self.file_info.sha)
        print(f"更新github {self.file_path} 文件成功！")

class Jlqc:
    def __init__(self, gh_list):
        js_code = open('utils/jlqc.js', 'r', encoding='utf-8').read()
        current_time = datetime.now()
        self.js = execjs.compile(js_code)
        self.md = current_time.strftime("%m-%d")
        self.day = current_time.day
        self.error_list = []
        self.gh_list = gh_list
        # 签到状态数量
        self.success = 0
        self.fail = 0
        self.availablePoint = 0
        self.availablePoint8 = 0
        self.availablePoint16 = 0
        self.availablePoint66 = 0
        self.token_unchecked = 0
        # 推送内容

    def sendMsg(self):
        msg = f'''
            账号总数：{len(all_data)}
            成功签到：{self.success}
            获得吉分：{self.availablePoint}
            8吉分：{self.availablePoint8}
            16吉分：{self.availablePoint16}
            66吉分：{self.availablePoint66}
            token失效：{self.token_unchecked}
        ''' + "\n\n" + '\n'.join(self.error_list)
        return msg  
    
    def newList(self, lst):
        new_lst = sorted(lst, key=lambda x: float(x['availablePoint']), reverse=True)
        return new_lst
                  
    def get_proxies(self):
        url = 'http://v2.api.juliangip.com/company/postpay/getips?num=1&pt=1&result_type=json&trade_no=6130652715138961&sign=3b1896626239e61a182b00ac5582d07f'
        for i in range(3):
            result = send_request('GET', url)
            if not result:
                break
            if result['code'] == 200:
                proxy_ip = result['data']['proxy_list'][0]
                print("代理：" + proxy_ip)
                self.proxies = {
                  "http": proxy_ip,
                  "https": proxy_ip,
                }
                if self.pin_network(self.proxies):
                    return
            else:
                print(result)
                time.sleep(60)
        send(title_name + "---异常", "获取代理IP失败！")
        exit()   
         
    def pin_network(self, proxies):
        url = "https://www.juliangip.com/api/general/Test"
        result = send_request('GET', url, proxies=proxies)
        if result:
            return True
        print(f"{proxies['http']}：连接失败！！！")
        return False 
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
        current_time = datetime.now()
        signDate = current_time.strftime("%Y-%m-%d %H:%M:%S")
        ts = int(time.time())
        body = {
            "signDate": str(signDate),
            "ts": str(ts),
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
        result = send_request('POST', url, headers=headers, json=body, proxies=self.proxies)
        if result:
            if result['code'] == 'success' and 'msg' not in result['data']:
                self.success += 1
                my_dict['signdate'] = self.md
                if 'id' in result['data']:
                    if result['data']['id'] == '1':
                        self.availablePoint8 += 1
                        self.availablePoint += 8
                    elif result['data']['id'] == '2':
                        self.availablePoint16 += 1
                        self.availablePoint += 16
                    elif result['data']['id'] == '3':
                        self.availablePoint66 += 1
                        self.availablePoint += 66
                    print(f"签到：{result['code']}，{result['data']['prizeName']}")
                else:
                    print(f"签到：{result['code']}")
                return True
            elif result['code'] == 'fail' and result['message'] == '您已签到,请勿重复操作!':
                pass
            elif result['code'] == 'token.unchecked':
                self.token_unchecked += 1
                for i in self.gh_list:
                    if i['phone'] == self.phone:
                        print("号码已存在，不加入")
                        break
                else:
                    dict_new = {
                        'phone': my_dict['phone'],
                        'password': my_dict['password']
                    }
                    self.gh_list.append(dict_new)
            else:
                print(result)
                send(title_name + "====停止运行", str(result))
                exit()
            print(result)
        self.fail += 1
        self.error_list.append(f"{self.index}：签到失败")
            
    def available(self, my_dict):
        url = 'https://app.geely.com/api/v1/point/available'
        headers = {
            "Host": "app.geely.com",
            "accept": "application/json, text/plain, */*",
            "user-agent": self.available_UA(),
            "token": my_dict['token'],
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        result = send_request('GET', url, headers=headers, proxies=self.proxies)
        if result:
            if result['code'] == "success":
                my_dict['availablePoint'] = result['data']['availablePoint']
                print(f"吉分：{result['data']['availablePoint']}")
                return
            print(result)
        self.fail += 1
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
        result = send_request('GET', url, params=params, headers=headers, proxies=self.proxies)
        if result:
            if result['code'] == "success":
                my_dict['token'] = result['data']['token']
                my_dict['refreshToken'] = result['data']['refreshToken']
                print(f"刷新token：{result['code']}")
                return
            print(result)
        self.fail += 1
        self.error_list.append(f"{self.index}：刷新token失败")
                
    def main(self, index, my_dict):
        self.index = index
        self.get_proxies()
        if self.fail >= 20:
            send(title_name + "---停止运行", self.msg)
            exit()
        if self.sign(my_dict):
            self.available(my_dict)
            if self.day in (1, 15):
                self.refresh_token(my_dict)
            with open(filepath, 'w') as f:
                json.dump(all_data, f, indent=2)

if __name__ == '__main__':
    accountInfo = GithubFile('吉利汽车/AccountInfo.json')
    tokenUnchecked = GithubFile('吉利汽车/TokenUnchecked.json')
    jlqc = Jlqc(tokenUnchecked.content)
    random.shuffle(all_data)
    for index, my_dict in enumerate(all_data, start = 1):
        print(f"\n{index}/{len(all_data)}{'➠'*10}{my_dict['phone']}：")
        if my_dict['signdate'] != jlqc.md:
            jlqc.main(index, my_dict)
            if index < len(all_data):
                randomSleep(30,60)
        else:
            print("已签到，跳过")
            
    accountInfo.update(jlqc.newList(all_data))
    if len(jlqc.gh_list) > 0:
        tokenUnchecked.update(jlqc.gh_list)
    send(title_name, jlqc.sendMsg())
