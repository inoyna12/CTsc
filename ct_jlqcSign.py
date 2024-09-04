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
import string
import csv
import hashlib
from datetime import datetime
from fake_useragent import UserAgent
from github import Github
from notify import send

title_name = '吉利汽车'
version = "3.25.0"

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
         with open('utils/brand_model.csv', newline='', encoding='utf-8-sig') as csvfile:
            self.csvreader = list(csv.DictReader(csvfile))
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
    
    def generate_devicesn(self):
        # 字符集：包括数字和字母a-f
        characters = string.digits + 'abcdef'
        
        # 随机选择字符并组合成字符串
        random_string = ''.join(random.choice(characters) for _ in range(16))

    def random_imei(self):
        # 生成前14位随机数
        imei_base = [random.randint(0, 9) for _ in range(14)]
        # 使用Luhn算法计算校验位
        def luhn_checksum(digits):
            sum_ = 0
            for i in range(len(digits)):
                digit = digits[-(i + 1)]
                if i % 2 == 0:  # 偶数位
                    digit *= 2
                    if digit > 9:
                        digit -= 9
                sum_ += digit
            return (10 - (sum_ % 10)) % 10
        # 计算校验位
        checksum = luhn_checksum(imei_base)
        # 将校验位添加到IMEI码中
        imei_base.append(checksum)
        # 转换为字符串
        imei = ''.join(map(str, imei_base))
        return imei    

    def generate_resolution(self):
        # 定义一些常见的分辨率范围
        width_options = [
            720, 1080, 1440, 2160, 2400, 2560, 3200
        ]
        height_options = [
            1280, 1920, 2560, 3840, 1080, 1200, 1440, 1600, 2400
        ]
    
        # 随机选择一个宽度和高度
        width = random.choice(width_options)
        height = random.choice(height_options)
    
        # 返回格式化的分辨率字符串
        return f"{width}*{height}"

    def md5(self, str_imei):
        md5_hasher = hashlib.md5()
        md5_hasher.update(str_imei.encode('utf-8'))
        md5_hashed_string = md5_hasher.hexdigest()
        return md5_hashed_string

    def create_sweet_security_info(self, imei, osVersion):
        battery = str(random.randint(20, 100))
        phoneInfo = random.choice(self.csvreader)
        random_number = random.randint(100000, 999999)
        osVersion = str(random.randint(8, 14))
        sweet_security_info = {
            "appVersion": version,
            "platform": "android",
            "battery": battery,
            "isCharging": "3",
            "isSetProxy": "false",
            "isUsbDebug": "false",
            "isMockLocation": "false",
            "isRoot": "false",
            "appSignature": "4A25003CFDA7F61BC387C182551D5681",
            "channel": "%E5%90%89%E5%88%A9",
            "screenResolution": self.generate_resolution(),
            "brand": phoneInfo['brand'],
            "model": phoneInfo['model'],
            "imsi": f"35659{random_number}6247",
            "geelyDeviceId": self.md5(imei),
            "os": "android",
            "osVersion": osVersion,
            "androidVersion": "31",
            "networkType": "WIFI",
            "ip": "192.168.0.100",
            "wifiSignalLevel": "-42",
            "isLbsEnabled": "false",
            "lbsLatitude": "",
            "lbsLongitude": ""
        }
        
        sweet_security_info = json.dumps(sweet_security_info, separators=(',', ':'))
        print(sweet_security_info)
        print(type(sweet_security_info))
        return sweet_security_info
      
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
        imei = self.random_imei()
        osVersion = str(random.randint(8, 14))
        sweet_security_info = self.create_sweet_security_info(imei, osVersion)
        body = {
            "signDate": str(signDate),
            "ts": ts,
            "cId":"BLqo2nmmoPgGuJtFDWlUjRI2b1b"
        }
        headers = {
            'Host': 'app.geely.com',
            'x-data-sign': self.js.call("enen", body),
            'x-refresh-token': 'true',
            'devicesn': self.generate_devicesn(),
            'token': my_dict['token'],
            'version': version,
            'platform': 'Android',
            'cache-control': 'no-cache',
            'imei': imei,
            'os': osVersion,
            'sweet_security_info': sweet_security_info,
            'content-type': 'application/json; charset=utf-8'
        }
        result = send_request('POST', url, headers=headers, data=json.dumps(body), proxies=self.proxies)
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
            "pragma": "no-cache",
            "cache-control": "no-cache",
            "accept": "application/json, text/plain, */*",
            "user-agent": self.available_UA(),
            "token": my_dict['token'],
            "x-requested-with": "com.geely.consumer",
            "referer": "https://app.geely.com/app-h5/grow-up/?showTitleBar=0&needLogin=1&tabsIndex=0",
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
            'devicesn': self.generate_devicesn(),
            "token": my_dict['token'],
            "appversion": version,
            "platform": "Android",
            "cache-control": "no-cache"
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
