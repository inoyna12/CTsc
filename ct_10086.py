'''
cron: 1 0 * * *
new Env('中国移动');
'''

import requests,json,base64,re
import random
import time
import hashlib
import ssl
import urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

class SSLAdapter(HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)

context = create_urllib3_context()
context.set_ciphers("DEFAULT:@SECLEVEL=1")
# python3.12可用
# context.options |= ssl.OP_LEGACY_SERVER_CONNECT
# 3.11可用
context.options |= 0x4
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
adapter = SSLAdapter(ssl_context=context)

encrypted_data = 'O3fIBA5/7El612+bC8WeNDX+YRsQhOwny+bi8flFyGBTirVy0llPXAYvZ9T4f+vOge5d3PZWX6Uk0YibrmzqTAEfteqsRl2LjsILVnPl7dAWcGQB2ys02bEny/JYTglngHeGWMn6QNOIUidtvQ/vvTPa0OZyFPVoWDfUm/ZYxx23nazyl7YFg4UVp3KmbEh/X3Oood50hBeaiGI2MPZPqUDe590IwSs4voteWTXybMXiT/bxCekKKO3mh4fWtDLLvJh8bQ/gwoT4tAyciKpZCTdz61fpKYZ4sXZZCW/c2XvFCxD80JNBLIYd7owqiCS01sbJlFIS52Hxqs+3HXtg1iCR7ZTY7pbgmJnb4+XRIGTiCkEaiy10hMaEEYRA2CFxlEw+fOMpZj+DAeNTg53MnA8xW/CE+rIorv3lzX4N6IfcBpeVBG9uebtVwHC9OT+N9czC8uaDpn/T/sbBBg/BRMrK2r2/UmPQDzrfRm5ezYwDxT8IYWDfXwjYjh+po1MPFi373tNUl4kfSLb1ZBxXEEQNZ8wM30cAJE/nIczHjDkWXQG7ls/yh7llFjcKqFHD1eBdFffLVvaNxH9BSN0GyTIdXGj6w3OiJxeEyeDlvDd5LK3ukN9w6lcVx5QEULalGfq7hiFit9xs5aP70cotYvRD2N305BhTYoBa2rJzsWC/5H//bYpjKl3SO3s/x7ir/O0fdKaiBdCq6NKM7PXitgzNWaZeW5jQfyyclkn+mBmZD4Ytna6bXyWDf2Bh5wEYsK63VhdUp7SI+6d8SkZNfXQ0vzLJuY+RDhvr1Niwy8ZJ64Xw0RcCGUNdpsayNp5xNgpTA2ngYjzp6KWlU83cqgHD8i8QOF9BejURFAQfAWTfm2Ozim2SX3VeKByi68Gb1m6w6s5aEPO/hRPXJa9SDMIXZBCP7Cmr+rrF9hO+Kg2atuTk/QlJQFy2iA4QsNlqAKjSpqz7/lk90XSOHMXbI5duwlSa3ExnOHEqgh8i9515iK/GTKhSaQCtgGNxe0skZ6Tap9GFO0l3Lsy6qYjuuwbTMSK91JFP0bIXUrlVWKjIkMCSjLImIR+5bpaGlbLFbBpIKeTx6J+msG7LhZgZH8TOkufB4T7TvPo9xSlwKtfEXVpnllq3WGaEPPNP+fcznRp7CqG7Pw8JecczWerN5ZJXQVdH9RT8I2O6zdJGFS/eXSQ450z72rTc3MbtX9VBSerxdulaChClGcUWl0xHV8qJG2ABe5+wXTxZh+7giSTZVfKNem1z1UY3wZtVYU6WSIV80KB0Q4MpnfCaMYqf+DyE1pbzskFEZuyz31iK5LaJMfrbKgz6kZeytdmj97dc2V5Kr41YIqDzYOphZJl/f+sYYG2I6r9K2lAl8QcmTZZpnwAOR70FPbuZT7bUiHaYQgyROQvmrk53HUH/jKLPJlnNlKAu0IUvIol74QlxAKCYQYl2rKgS0yJTkVe3I1cJC87P+jVC0dkkv3dQkIPSkv7OWXuL7QDeaRzvH6ByDr8sL0Sl+0dpyV4GOhqrb2mWdni3dh2Xued+rXFUDwawbw=='

class Yd:
    def __init__(self, encrypted_data):
        self.key = 'bAIgvwAuA4tbDr9d'
        self.key2 = 'GS7VelkJl5IT1uwQ'# 响应体秘钥
        self.iv = '9791027341711819'
        self.my_data = self.aes_cbc_decrypt(self.key, self.iv, encrypted_data)
        self.my_dict = json.loads(self.my_data)
        self.session = requests.Session()
        self.session.mount('https://', adapter)
        self.jsUrl = 'https://wap.js.10086.cn/nact/action.do'
        self.jsHeaders = self.jsHeaders()
    
    def aes_cbc_encrypt(self, key_str, iv_str, data_str):
        key = key_str.encode('utf-8')
        iv = iv_str.encode('utf-8')
        data = data_str.encode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = pad(data, AES.block_size, style='pkcs7')
        encrypted_bytes = cipher.encrypt(padded_data)
        encrypted_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')
        return encrypted_base64
        
    def aes_cbc_decrypt(self, key, iv, encrypted_data):
        key_bytes = key.encode('utf-8')
        iv_bytes = iv.encode('utf-8')
        encrypted_bytes = base64.b64decode(encrypted_data)
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        decrypted_bytes = cipher.decrypt(encrypted_bytes)
        try:
            unpadded_bytes = unpad(decrypted_bytes, AES.block_size, style='pkcs7')
        except ValueError as e:
            print("解密失败，可能是密钥、IV 或加密数据不正确。")
            return None
        decrypted_data = unpadded_bytes.decode('utf-8')
        return decrypted_data

    def md5_encrypt(self, data):
        md5_hash = hashlib.md5()
        md5_hash.update(data.encode('utf-8'))
        return md5_hash.hexdigest()

    def create_body(self):
        my_dict = {
            "ak": self.my_dict['ak'],
            "cid":self.my_dict['cid'],
            "city": self.my_dict['city'],
            "ctid": self.my_dict['ctid'],
            "cv": self.my_dict['cv'],
            "en": self.my_dict['en'],
            "imei": self.my_dict['imei'],
            "nt": self.my_dict['nt'],
            "prov": self.my_dict['prov'],
            "reqBody": {
                "cellNum": self.phone,
                "sourceId": "039014",
                "url": "https://wap.js.10086.cn/nact/resource/2510/html/index.html"
            },
            "sb": self.my_dict['sb'],
            "sn": self.my_dict['sn'],
            "sp": self.my_dict['sp'],
            "st": self.my_dict['st'],
            "sv": self.my_dict['sv'],
            "t": "e268633f681c99175175851d4cf964e0",
            "tel": self.phone,
            "xc": self.my_dict['xc'],
            "xk": self.my_dict['xk']
        }
        my_data = json.dumps(my_dict, separators=(',', ':'))
        return my_data

    def jsHeaders(self):
        headers = {
            'Host': 'wap.js.10086.cn',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.146 Mobile Safari/537.36 leadeon/9.4.1/CMCCIT',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://wap.js.10086.cn',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://wap.js.10086.cn/nact/resource/2510/html/index.html',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        return headers

#响应体headers中的cookie会携带JSESSIONID
    def autoLogin(self):
        url = 'https://client.app.coc.10086.cn/biz-orange/LN/uamrandcodelogin/autoLogin'
        x_nonce = '{:08d}'.format(random.randint(0, 99999999))
        timestamp = str(int(time.time() * 1000))
        url_path = urlparse(url).path
        self.my_dict['reqBody']['sysTime'] = timestamp
        data_new = json.dumps(self.my_dict, separators=(',', ':'))
        xs = f"{url}_{data_new}_Leadeon/SecurityOrganization"
        xs_md5 = self.md5_encrypt(xs)
        x_token = f"{self.my_dict['xk']}_{url_path}_{timestamp}_{x_nonce}"
        x_token_encrypt = self.aes_cbc_encrypt(self.key, self.iv, x_token)
        x_sign = f"{x_token_encrypt}_{timestamp}_{x_nonce}_null"
        x_sign_md5 = self.md5_encrypt(x_sign)
        headers = {
            'x-sign': x_sign_md5,
            'x-time': timestamp,
            'xs': xs_md5,
            'x-qen': '2',
            'x-nonce': x_nonce,
            'x-token': x_token_encrypt,
            'Content-Type': 'application/json; charset=utf-8',
            'Host': 'client.app.coc.10086.cn',
            'Connection': 'Keep-Alive',
            'User-Agent': 'okhttp/3.14.9'
        }
        body = self.aes_cbc_encrypt(self.key, self.iv, data_new)
        response = self.session.post(url, headers=headers, data=body, verify=False)
        if response.status_code == 200:
            resphead = response.headers
            result = self.aes_cbc_decrypt(self.key2, self.iv, response.text)
            result_dict = json.loads(result)
            if result_dict['retCode'] == '000000':
                self.phone = result_dict['rspBody']['userName']
                print(self.phone + "登录成功")
                self.cookie = resphead.get('Set-Cookie')
                match = re.search(r'JSESSIONID=([a-f0-9\-]+)', self.cookie)
                self.jsessionid = match.group(1)
                return True
            else:
                print(result)
        else:
            print(f"登录失败，响应状态码：{response.status_code}")
        return False
 
    def getBigNetToken(self):
        my_data = self.create_body()
        url = 'https://client.app.coc.10086.cn/leadeon-abilityopen-biz/BN/obtainToken/getBigNetToken'
        x_nonce = '{:08d}'.format(random.randint(0, 99999999))
        timestamp = str(int(time.time() * 1000))
        url_path = urlparse(url).path
        xs = f"{url}_{my_data}_Leadeon/SecurityOrganization"
        xs_md5 = self.md5_encrypt(xs)
        x_token = f"{self.my_dict['xk']}_{url_path}_{timestamp}_{x_nonce}"
        x_token_encrypt = self.aes_cbc_encrypt(self.key, self.iv, x_token)
        x_sign = f"{x_token_encrypt}_{timestamp}_{x_nonce}_{self.jsessionid}"
        x_sign_md5 = self.md5_encrypt(x_sign)
        headers = {
            'x-sign': x_sign_md5,
            'x-time': timestamp,
            'xs': xs_md5,
            'x-qen': '2',
            'x-nonce': x_nonce,
            'x-token': x_token_encrypt,
            'Cookie': self.cookie,
            'Content-Type': 'application/json; charset=utf-8',
            'Host': 'client.app.coc.10086.cn',
            'Connection': 'Keep-Alive',
            'User-Agent': 'okhttp/3.14.9'
        }
        body = self.aes_cbc_encrypt(self.key, self.iv, my_data)
        response = self.session.post(url, headers=headers, data=body, verify=False).text
        result = self.aes_cbc_decrypt(self.key2, self.iv, response)
        result_dict = json.loads(result)
        if result_dict['retCode'] == '000000':
            token = result_dict['rspBody']['token']
            return token
        else:
            print(result_dict)

#响应体headers中的cookie会携带cmtokenid
    def getCmtokenid(self):
        jtToken = self.getBigNetToken()
        body = {
            'reqUrl': 'wapLogin',
            'method': 'jtTokenLogin',
            'busiNum': 'JTTokenLOGIN',
            'jtToken': jtToken,
            'actCode': '2510',
            'env': 'jt_app',
            'extendParams': '',
            'ywcheckcode': '',
            'mywaytoopen': ''
        }
        response = self.session.post(self.jsUrl, headers=self.jsHeaders, data=body, verify=False).text
        result = json.loads(response)
        sc = result['resultObj']['sc']

    def doSign(self):
        body = {
            'reqUrl': 'act2510',
            'method': 'doSign',
            'operType': '1',
            'actCode': '2510',
            'isJtAPP': 'true',
            'env': 'jt_app',
            'extendParams': '',
            'ywcheckcode': '',
            'mywaytoopen': ''
        }
        response = self.session.post(self.jsUrl, headers=self.jsHeaders, data=body, verify=False).text
        result = json.loads(response)
        if result['success']:
            if 'prize' in result['resultObj']:
                awardName = result['resultObj']['prize']['awardName']
                print(awardName)
                if '抽奖' in awardName:
                    self.doSignMulti()
            else:
                print(result['resultObj']['errorMsg'])
        else:
            print(result)
    
    # 开启签到宝箱
    def doSignMulti(self):
        body = {
            'reqUrl': 'act2510',
            'method': 'doSignMulti',
            'operType': '1',
            'actCode': '2510',
            'isJtAPP': 'true',
            'env': 'jt_app',
            'extendParams': '',
            'ywcheckcode': '',
            'mywaytoopen': ''
        }
        response = self.session.post(self.jsUrl, headers=self.jsHeaders, data=body, verify=False).text
        result = json.loads(response)
        if result['success']:
            if 'prize' in result['resultObj']:
                awardName = result['resultObj']['prize']['awardName']
                print(awardName)
            else:
                print(result['resultObj']['errorMsg'])
        else:
            print(result)

    def Ebean(self):
        body = {
            'reqUrl': 'act2510',
            'method': 'initIndexTasks',
            'operType': '1',
            'actCode': '2510',
            'isJtAPP': 'true',
            'env': 'jt_app',
            'extendParams': '',
            'ywcheckcode': '',
            'mywaytoopen': ''
        }
        response = self.session.post(self.jsUrl, headers=self.jsHeaders, data=body, verify=False).text
        result = json.loads(response)
#        print(result)
        # 任务列表
        tasksCfg = result['resultObj']['tasksCfg']
        # 已完成任务列表
        userTasksOpr = result['resultObj']['userTasksOpr']
        for cfg in tasksCfg:
            taskId = cfg['taskId']
            taskName = cfg['taskName']
            for opr in userTasksOpr:
                if taskId == opr['taskId']:
                    # 1已领取奖励，0未领取
                    if opr['status'] == '0':
                        self.EbeanTaskAward(taskId)
                    elif opr['status'] == '1':
                        print(f"{taskName} 已完成")
                    break
            else:
                print(f"执行任务：{taskName}({taskId})")
                if taskId == 'act_task_09':
                    self.EbeanTask_09(taskId)
                elif taskId == 'act_task_89':
                    self.EbeanTask_89(taskId)
                elif taskId == 'act_task_17':
                    self.EbeanTask_17(taskId)
                elif taskId in 'act_task_34':
                    self.EbeanTask_34(taskId)
                elif 'ch=7x' in cfg['url']:
                    self.EbeanTask_7x(cfg)
                elif 'thass=1' in cfg['url']:
                    self.action_task(taskId, 'completeTask')
                else:
                    print("未知任务")
                    continue
                print(f"领取奖励：{taskName}({taskId})")
                self.EbeanTaskAward(taskId)

    def action_task(self, taskId, method):
        body = {
            'reqUrl': 'act2510',
            'method': method,
            'actCode': '2510',
            'taskId': taskId
        }
        response = self.session.post(self.jsUrl, headers=self.jsHeaders, data=body, verify=False).text
        result = json.loads(response)
        print(result)
    
    # 领e豆奖励              
    def EbeanTaskAward(self, taskId):
        body = {
            'reqUrl': 'act2510',
            'method': 'receiveTaskAward',
            'operType': '1',
            'actCode': '2510',
            'taskId': taskId,
            'isJtAPP': 'true',
            'env': 'jt_app',
            'extendParams': '',
            'ywcheckcode': '',
            'mywaytoopen': ''
        }
        response = self.session.post(self.jsUrl, headers=self.jsHeaders, data=body, verify=False).text
        result = json.loads(response)
        print(result)

    def EbeanTask_09(self, taskId):
        url = "http://wap.js.10086.cn/ex/mall/api/v1/user/act618/signIn618"
        body = json.dumps({
          "taskId": taskId,
          "userAppVer": "1",
          "userNetwork": "1",
          "userOs": "ios",
          "userCityNum": "1"
        })
        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.146 Mobile Safari/537.36 leadeon/9.4.1/CMCCIT",
            'Accept': "application/json, text/plain, */*",
            'Accept-Encoding': "gzip, deflate",
            'Content-Type': "application/json",
            'Cache-Control': "no-cache",
            'Origin': "http://wap.js.10086.cn",
            'X-Requested-With': "com.greenpoint.android.mc10086.activity",
            'Referer': "http://wap.js.10086.cn/",
            'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        response = self.session.post(url, data=body, headers=headers, verify=False)
        print(response.text)

    def EbeanTask_17(self, taskId):
        body = {
            'reqUrl': 'act2381',
            'method': 'newCompleteEBeanTask',
            'task2510Id': taskId,
            'actCode': '2381',
            'env': 'jt_app',
            'extendParams': f"thass=1&task2510Id={taskId}&task2510Status=0",
            'ywcheckcode': '',
            'mywaytoopen': ''
        }
        response = self.session.post(self.jsUrl, headers=self.jsHeaders, data=body, verify=False).text
        result = json.loads(response)
        print(result)
        
    def EbeanTask_89(self, taskId):
        body = {
            'reqUrl': 'act2510',
            'method': 'completeTargetTask',
            'operType': '1',
            'actCode': '2510',
            'taskId': taskId,
            'isJtAPP': 'true',
            'env': 'jt_app',
            'extendParams': '',
            'ywcheckcode': '',
            'mywaytoopen': ''
        }
        response = self.session.post(self.jsUrl, headers=self.jsHeaders, data=body, verify=False).text
        result = json.loads(response)
        print(result)

    def EbeanTask_34(self, taskId):
        body = {
            'reqUrl': 'mscx',
            'method': 'mengluTask',
            'taskId': taskId
        }
        response = self.session.post(self.jsUrl, headers=self.jsHeaders, data=body, verify=False).text
        result = json.loads(response)
        print(result)
        
    def EbeanTask_7x(self, cfg):
        parsed_url = urlparse(cfg['url'])
        path_parts = parsed_url.path.split('/')
        field = path_parts[-1].split('.')[0]
        url = 'https://wap.js.10086.cn/vw/gateway/biz/eSignIn/qd'
        headers = {
            "Host": "wap.js.10086.cn",
            "Connection": "keep-alive",
            "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Android WebView";v="128"',
            "Accept": "application/json, text/plain, */*",
            "sec-ch-ua-platform": "Android",
            "sec-ch-ua-mobile": "?1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.146 Mobile Safari/537.36 leadeon/9.4.1/CMCCIT",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://wap.js.10086.cn",
            "X-Requested-With": "com.greenpoint.android.mc10086.activity",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://wap.js.10086.cn/",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        body = {
          "taskId": cfg['taskId'],
          "wapContext": {
            "optType": "1",
            "bizCode": field
          }
        }
        # 发送 POST 请求
        result = self.session.post(cfg['url'], headers=headers, data=json.dumps(body), verify=False).text
        print(result)

    def main(self):
        if self.autoLogin():
            self.getCmtokenid()
            self.doSign()
            self.Ebean()
        self.session.close()



yd = Yd(encrypted_data)
yd.main()
