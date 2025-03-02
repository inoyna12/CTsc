'''
cron: 36 6 * * *
new Env('福域');
'''

import json,base64,string,hashlib,datetime,random,time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from tools.tool import rts, randomSleep
from tools.githubFile import GithubFile
from tools.proxy import xiequ
from notify import send

title_name = "福域"
appVersion = "1.5.4"

def aes_cbc_encrypt(key_str, iv_str, data_str):
    key = key_str.encode('utf-8')
    iv = iv_str.encode('utf-8')
    data = data_str.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(data, AES.block_size, style='pkcs7')
    encrypted_bytes = cipher.encrypt(padded_data)
    encrypted_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')
    return encrypted_base64

def aes_cbc_decrypt(key, iv, encrypted_data):
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
    
def rsa_encrypt(text, public_key):
    # 将Base64编码的公钥转换成RSA对象
    rsa_key = RSA.importKey(base64.b64decode(public_key))
    cipher = PKCS1_v1_5.new(rsa_key)
    # 对文本进行加密
    ciphertext = cipher.encrypt(text.encode('utf-8'))
    # 返回Base64编码的加密结果
    return base64.b64encode(ciphertext).decode()
    
def md5_encrypt(text, uppercase=True):
    md5_hash = hashlib.md5()
    md5_hash.update(text.encode('utf-8'))
    if uppercase:
        return md5_hash.hexdigest().upper()
    else:
        return md5_hash.hexdigest()
    
class FY:
    def __init__(self):
        self.seccode_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDUUKw74ULuOMsQT9EO64Ij8y/DAgmW2JvbPIa7XTLibr0lfG7nnbXhnIWFwx1tfgG04P1jYZBHBVcvP7sVIWVvVDg8N43RErIu+kNCEMMfq22iUahKK1vi+y2bsXfVCa4SWS5eDegQOsuBfsP30HlcA4uvH3+/elFepv+6ep9ZmwIDAQAB'
        self.gh_fy = GithubFile("福域/fy.json")
        
        # 签到成功数量
        self.sign_true = 0
        
        # 账号跳过数量
        self.accout_skip = 0
        
        # 抽奖失败数量
        self.luckDraw_fail = 0
    
    def newList(self, lst):
        new_lst = sorted(lst, key=lambda x: x['totalIntegral'], reverse=True)
        return new_lst
    
    def sendMsg(self):
        msg = f'''
            账号总数：{my_length}
            签到：{self.sign_true}
            跳过：{self.accout_skip}
        '''
        return msg
         
    def get_proxy(self):
        proxies = xiequ()
        if proxies:
            return proxies
        send(f"{title_name}_获取代理ip失败", "获取代理ip失败")
        exit()
    
    # app启动
    def app_launch(self):
        url = "https://evosapi.fuyu.club/con/ads/list"
        for i in range(5):
            timestamp = str(int(time.time() * 1000))
            randomStr = ''.join(random.sample(string.ascii_uppercase, 3))
            seccode = timestamp + randomStr
            paramEncr = json.dumps({
                "posCode": "app_launch"
            }, separators=(',', ':'))
            body = json.dumps({
              "paramEncr": aes_cbc_encrypt(seccode, seccode, paramEncr)
            }, separators=(',', ':'))
            sign = body + timestamp + 'hyzh-unistar-8KWAKH291IpaFB'
            headers = {
              'User-Agent': "ford-evos",
              'Connection': "Keep-Alive",
              'Content-Type': "application/json",
              'Host': 'evosapi.fuyu.club',
              'appVersion': appVersion,
              'os': "Android",
              'loginChannel': "baidu",
              'sign': md5_encrypt(sign),
              'body': md5_encrypt(paramEncr),
              'operatorName': "yd",
              'networkState': "WIFI",
              'token': my_dict['token'],
              'osVersion': my_dict['osVersion'],
              'seccode': rsa_encrypt(seccode, self.seccode_key),
              'model': my_dict['model'],
              'brand': my_dict['brand'],
              'timestamp': timestamp,
              'codelab': "codelabs"
            }
            result = rts('post', url, headers=headers, data=body, proxies=self.proxies)
            if result:
                print(f"app_launch：{result['msg']}")
                if result['msg'] == '操作成功':
                    return
                else:
                    print(result)
                    send(f"{title_name}_app_launch", "未知响应体")
                    exit()
            else:
                self.proxies = self.get_proxy()
        
    def signIn(self):
        url = "https://evosapi.fuyu.club/user/signIn"
        for i in range(5):
            timestamp = str(int(time.time() * 1000))
            randomStr = ''.join(random.sample(string.ascii_uppercase, 3))
            seccode = timestamp + randomStr
            paramEncr = json.dumps({})
            body = json.dumps({
              "paramEncr": aes_cbc_encrypt(seccode, seccode, paramEncr)
            }, separators=(',', ':'))
            sign = body + timestamp + 'hyzh-unistar-8KWAKH291IpaFB'
            headers = {
              'User-Agent': "ford-evos",
              'Connection': "Keep-Alive",
              'Content-Type': "application/json",
              'Host': 'evosapi.fuyu.club',
              'appVersion': appVersion,
              'os': "Android",
              'loginChannel': "baidu",
              'sign': md5_encrypt(sign),
              'body': md5_encrypt(paramEncr),
              'operatorName': "dx",
              'networkState': "WIFI",
              'token': my_dict['token'],
              'osVersion': my_dict['osVersion'],
              'seccode': rsa_encrypt(seccode, self.seccode_key),
              'model': my_dict['model'],
              'brand': my_dict['brand'],
              'timestamp': timestamp,
              'codelab': "codelabs"
            }
            result = rts('post', url, headers=headers, data=body, proxies=self.proxies)
            if result:
                if result['data'] is None:
                    print(result)
                    return False
                d_data = json.loads(aes_cbc_decrypt(seccode, seccode, result['data']))
                luckyBlessingBagId = None
                if result['msg'] == '操作成功':
                    luckyBlessingBagId = d_data['luckyBlessingBagId']
                    msg = f"已连续签到 {d_data['ontinuous']} 天"
                elif result['msg'] == '今天您已签到':
                    msg = result['msg']
                else:
                    print(result)
                    break
                print(f"签到：{msg}")
                my_dict['signdate'] = today_date
                self.sign_true += 1
                if luckyBlessingBagId:
                    self._luckDraw(luckyBlessingBagId)
                return True
            else:
                self.proxies = self.get_proxy()
        send(f"{title_name}_签到失败", "签到失败")
        exit()

    # 查询福币
    def getAllTasks(self):
        url = "https://evosapi.fuyu.club/userTask/getAllTasks"
        timestamp = str(int(time.time() * 1000))
        randomStr = ''.join(random.sample(string.ascii_uppercase, 3))
        seccode = timestamp + randomStr
        paramEncr = json.dumps({})
        body = json.dumps({
          "paramEncr": aes_cbc_encrypt(seccode, seccode, paramEncr)
        }, separators=(',', ':'))
        sign = body + timestamp + 'hyzh-unistar-8KWAKH291IpaFB'
        headers = {
          'User-Agent': "ford-evos",
          'Connection': "Keep-Alive",
          'Content-Type': "application/json",
          'Host': 'evosapi.fuyu.club',
          'appVersion': appVersion,
          'os': "Android",
          'loginChannel': "baidu",
          'sign': md5_encrypt(sign),
          'body': md5_encrypt(paramEncr),
          'operatorName': "dx",
          'networkState': "WIFI",
          'token': my_dict['token'],
          'osVersion': my_dict['osVersion'],
          'seccode': rsa_encrypt(seccode, self.seccode_key),
          'model': my_dict['model'],
          'brand': my_dict['brand'],
          'timestamp': timestamp,
          'codelab': "codelabs"
        }
        result = rts('post', url, headers=headers, data=body, proxies=self.proxies)
        if result:
            if result['msg'] == '操作成功':
                d_data = json.loads(aes_cbc_decrypt(seccode, seccode, result['data']))
                totalIntegral = d_data[0]['userTatalScore']
                print(f"福币：{totalIntegral}")
                my_dict['totalIntegral'] = totalIntegral

    # 签到抽奖
    def _luckDraw(self, activityId):
        url = f"https://evosapi.fuyu.club/luckyBlessingBag/luckDraw/{activityId}"
        for i in range(5):
            timestamp = str(int(time.time() * 1000))
            randomStr = ''.join(random.sample(string.ascii_uppercase, 3))
            seccode = timestamp + randomStr
            paramEncr = json.dumps({
                "activityId": str(activityId)
            }, separators=(',', ':'))
            body = json.dumps({
              "paramEncr": aes_cbc_encrypt(seccode, seccode, paramEncr)
            }, separators=(',', ':'))
            sign = body + timestamp + 'hyzh-unistar-8KWAKH291IpaFB'
            headers = {
              'User-Agent': f"Mozilla/5.0 (Linux; Android 12; {my_dict['model']} Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046291 Mobile Safari/537.36 ford-evos",
              'Accept': "application/json, text/plain, */*",
              'Content-Type': "application/json",
              'Pragma': "no-cache",
              'Cache-Control': "no-cache",
              'seccode': rsa_encrypt(seccode, self.seccode_key),
              'timestamp': timestamp,
              'token': my_dict['token'],
              'sign': md5_encrypt(sign),
              'appVersion': appVersion,
              'Origin': "https://evosh5.fuyu.club",
              'X-Requested-With': "com.changanford.evos",
              'Sec-Fetch-Site': "same-site",
              'Sec-Fetch-Mode': "cors",
              'Sec-Fetch-Dest': "empty",
              'Referer': "https://evosh5.fuyu.club/",
              'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
            }
            result = rts('post', url, headers=headers, data=body, proxies=self.proxies)
            if result:
                if result['msg'] == '操作成功':
                    d_data = json.loads(aes_cbc_decrypt(seccode, seccode, result['data']))
                    print(f"抽奖：{d_data['prizeName']}")
                    return
                elif result['msg'] == '已无抽奖机会':
                    print(result)
                    self.luckDraw_fail += 1
                    if self.luckDraw_fail > 5:
                        print('抽奖失败次数过多')
                        break
                    return
                else:
                    print(result)
                    break
            else:
                self.proxies = self.get_proxy()
        send(f"{title_name}_抽奖失败", "抽奖失败")
        exit() 

    # 登录获取ssdmnToken
    def login(self):
        url = "https://h5fya.fuyu.club/ford-cyjl/user/login"
        for i in range(5):
            timestamp = str(int(time.time() * 1000))
            body = json.dumps({
                "data": self._getTempCode(),
                "code": "https://h5fyaxo.fuyu.club/prod/h5-2025/ford-cyjl/dist/index.html",
                "type": "APP"
            }, separators=(',', ':'))
            sign = 'ford-ssdmn-api-4531sadfs' + body + timestamp + 'ford-ssdmn-api-4531sadfs'
            headers = {
              'User-Agent': f"Mozilla/5.0 (Linux; Android 12; {my_dict['model']} Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.146 Mobile Safari/537.36 ford-evos",
              'Accept': "application/json, text/plain, */*",
              'Accept-Encoding': "gzip, deflate, br, zstd",
              'Content-Type': "application/json",
              'pragma': "no-cache",
              'cache-control': "no-cache",
              'sec-ch-ua': "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Android WebView\";v=\"128\"",
              'channel-type': "APP",
              'sec-ch-ua-mobile': "?1",
              'channel_type': "APP",
              'content-type': "application/json;charset=UTF-8",
              'timestamp': timestamp,
              'sign': md5_encrypt(sign, uppercase=False),
              'sec-ch-ua-platform': "\"Android\"",
              'origin': "https://h5fyaxo.fuyu.club",
              'x-requested-with': "com.changanford.evos",
              'sec-fetch-site': "same-site",
              'sec-fetch-mode': "cors",
              'sec-fetch-dest': "empty",
              'referer': "https://h5fyaxo.fuyu.club/",
              'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
              'priority': "u=1, i"
            }
            result = rts('post', url, headers=headers, data=body, proxies=self.proxies)
            if result:
                if result['msg'] == 'ok':
                    self.ssdmnToken = result['data']['ssdmnToken']
                else:
                    print(result)
                    break
            else:
                self.proxies = self.get_proxy()
        send(f"{title_name}_login", "未知响应体")
        exit()

    # 获取code值
    def _getTempCode(self, body_dict):
        url = "https://evosapi.fuyu.club/idp/getTempCode"
        for i in range(5):
            timestamp = str(int(time.time() * 1000))
            randomStr = ''.join(random.sample(string.ascii_uppercase, 3))
            seccode = timestamp + randomStr
            paramEncr = json.dumps(body_dict, separators=(',', ':'))
            body = json.dumps({
              "paramEncr": aes_cbc_encrypt(seccode, seccode, paramEncr)
            }, separators=(',', ':'))
            sign = body + timestamp + 'hyzh-unistar-8KWAKH291IpaFB'
            headers = {
              'User-Agent': "ford-evos",
              'Connection': "Keep-Alive",
              'Content-Type': "application/json",
              'Host': 'evosapi.fuyu.club',
              'appVersion': appVersion,
              'os': "Android",
              'loginChannel': "baidu",
              'sign': md5_encrypt(sign),
              'body': md5_encrypt(paramEncr),
              'operatorName': "yd",
              'networkState': "WIFI",
              'token': my_dict['token'],
              'osVersion': my_dict['osVersion'],
              'seccode': rsa_encrypt(seccode, self.seccode_key),
              'model': my_dict['model'],
              'brand': my_dict['brand'],
              'timestamp': timestamp,
              'codelab': "codelabs"
            }
            result = rts('post', url, headers=headers, data=body, proxies=self.proxies)
            if result:
                if result['msg'] == '操作成功':
                    d_data = json.loads(aes_cbc_decrypt(seccode, seccode, result['data']))
                    return d_data['code']
                else:
                    print(result)
                    break
            else:
                self.proxies = self.get_proxy()
        send(f"{title_name}_getTempCode", "未知响应体")
        exit()

    # 会员周领取奖励
    def send_prize(self, token):
        url = "https://h5fyax.fuyu.club/member-week-api/api/v1/activity/send_prize"
        for i in range(5):
            timestamp = str(int(time.time() * 1000))
            body = {}
            headers = {
              'User-Agent': f"Mozilla/5.0 (Linux; Android 12; {my_dict['model']} Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.146 Mobile Safari/537.36 ford-evos",
              'Accept-Encoding': "gzip, deflate, br, zstd",
              'Content-Type': "application/json",
              'pragma': "no-cache",
              'cache-control': "no-cache",
              'sec-ch-ua': "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Android WebView\";v=\"128\"",
              'sec-ch-ua-mobile': "?1",
              'o': token,
              'c': "DJ8732FD21AW23ED",
              't': timestamp,
              'sec-ch-ua-platform': "\"Android\"",
              'origin': "https://h5fyax.fuyu.club",
              'x-requested-with': "com.changanford.evos",
              'sec-fetch-site': "same-origin",
              'sec-fetch-mode': "cors",
              'sec-fetch-dest': "empty",
              'referer': "https://h5fyax.fuyu.club/member-week/",
              'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
              'priority': "u=1, i"
            }
            result = rts('post', url, headers=headers, data=json.dumps(body), proxies=self.proxies)
            if result:
                print(f"会员周奖励：{result['msg']}")
                if result['msg'] in ('发放成功', '今日已获取浏览奖励'):
                    return
                else:
                    print(result)
                    break
            else:
                self.proxies = self.get_proxy()
        send(f"{title_name}_send_prize", "未知响应体")
        exit()

    # 会员周登录获取token
    def app_info(self):
        url = "https://h5fyax.fuyu.club/member-week-api/api/v1/activity/app_info"
        body_dict = {
            "clientId": "678960629228142593",
            "redirectUrl":"https://evossys.changanford.cn/ssdmn/test/h5"
        }
        for i in range(5):
            timestamp = str(int(time.time() * 1000))
            body = {
              "c": self._getTempCode(body_dict),
              "u": "https://evossys.changanford.cn/ssdmn/test/h5"
            }
            headers = {
              'User-Agent': f"Mozilla/5.0 (Linux; Android 12; {my_dict['model']} Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.146 Mobile Safari/537.36 ford-evos",
              'Accept-Encoding': "gzip, deflate, br, zstd",
              'Content-Type': "application/json",
              'pragma': "no-cache",
              'cache-control': "no-cache",
              'sec-ch-ua': "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Android WebView\";v=\"128\"",
              'sec-ch-ua-platform': "\"Android\"",
              'c': "DJ8732FD21AW23ED",
              't': timestamp,
              'sec-ch-ua-mobile': "?1",
              'origin': "https://h5fyax.fuyu.club",
              'x-requested-with': "com.changanford.evos",
              'sec-fetch-site': "same-origin",
              'sec-fetch-mode': "cors",
              'sec-fetch-dest': "empty",
              'referer': "https://h5fyax.fuyu.club/member-week/",
              'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
              'priority': "u=1, i"
            }
            result = rts('post', url, headers=headers, data=json.dumps(body), proxies=self.proxies)
            if result:
                if result['msg'] == '登录成功':
                    return result['data']['token']
                else:
                    print(result)
                    break
            else:
                self.proxies = self.get_proxy()
        send(f"{title_name}_app_info", "未知响应体")
        exit()

    # 会员周行为动作
    def option(self, token, p):
        url = "https://h5fyax.fuyu.club/member-week-api/api/v1/activity/option"
        for i in range(5):
            timestamp = str(int(time.time() * 1000))
            body = {
              "p": p
            }
            headers = {
              'User-Agent': f"Mozilla/5.0 (Linux; Android 12; {my_dict['model']} Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.146 Mobile Safari/537.36 ford-evos",
              'Accept-Encoding': "gzip, deflate, br, zstd",
              'Content-Type': "application/json",
              'pragma': "no-cache",
              'cache-control': "no-cache",
              'sec-ch-ua': "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Android WebView\";v=\"128\"",
              'sec-ch-ua-mobile': "?1",
              'o': token,
              'c': "DJ8732FD21AW23ED",
              't': timestamp,
              'sec-ch-ua-platform': "\"Android\"",
              'origin': "https://h5fyax.fuyu.club",
              'x-requested-with': "com.changanford.evos",
              'sec-fetch-site': "same-origin",
              'sec-fetch-mode': "cors",
              'sec-fetch-dest': "empty",
              'referer': "https://h5fyax.fuyu.club/member-week/",
              'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
              'priority': "u=1, i"
            }
            result = rts('post', url, headers=headers, data=json.dumps(body), proxies=self.proxies)
            if result:
                print(f"{p}：{result['msg']}")
                if result['msg'] == 'success':
                    return 
                else:
                    print(result)
                    break
            else:
                self.proxies = self.get_proxy()
        send(f"{title_name}_option", "未知响应体")
        exit()
    
    # 会员周任务状态，1：已完成，2：未完成
    def status(self, token):
        url = "https://h5fyax.fuyu.club/member-week-api/api/v1/activity/status"
        for i in range(5):
            timestamp = str(int(time.time() * 1000))
            body = {}
            headers = {
              'User-Agent': f"Mozilla/5.0 (Linux; Android 12; {my_dict['model']} Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.146 Mobile Safari/537.36 ford-evos",
              'Accept-Encoding': "gzip, deflate, br, zstd",
              'Content-Type': "application/json",
              'pragma': "no-cache",
              'cache-control': "no-cache",
              'sec-ch-ua': "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Android WebView\";v=\"128\"",
              'sec-ch-ua-mobile': "?1",
              'o': token,
              'c': "DJ8732FD21AW23ED",
              't': timestamp,
              'sec-ch-ua-platform': "\"Android\"",
              'origin': "https://h5fyax.fuyu.club",
              'x-requested-with': "com.changanford.evos",
              'sec-fetch-site': "same-origin",
              'sec-fetch-mode': "cors",
              'sec-fetch-dest': "empty",
              'referer': "https://h5fyax.fuyu.club/member-week/",
              'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
              'priority': "u=1, i"
            }
            result = rts('post', url, headers=headers, data=json.dumps(body), proxies=self.proxies)
            if result:
                if result['msg'] == 'success':
                    return result['data']['status']
                else:
                    print(result)
                    break
            else:
                self.proxies = self.get_proxy()
        send(f"{title_name}_status", "未知响应体")
        exit()

    # 畅享会员周
    def HuiYuanZhou(self):
        token = self.app_info()
        status = self.status(token)
        if status == 2:
            self.option(token, '进入活动')
            time.sleep(random.randint(15, 20))
            self.option(token, '浏览完成发放福币')
            self.send_prize(token)
        elif status == 1:
            print("会员周任务已完成")
        else:
            print("未知任务状态")
    
    def main(self):
        self.proxies = self.get_proxy()
        self.app_launch()
        if self.signIn():
           # self.HuiYuanZhou()
            self.getAllTasks()
            
            
if __name__ == '__main__':
    today_date = datetime.datetime.now().strftime("%m-%d")
    filepath = "/ql/data/env/fy.json"
    with open(filepath, 'r') as f:
        my_list = json.load(f)
    my_length = len(my_list)
    random.shuffle(my_list)
    
    fy = FY()
    for index, my_dict in enumerate(my_list, start = 1):
        print(f"\n{index}/{my_length}{'➠'*10}{my_dict['phone']}：")
        if my_dict['signdate'] != today_date:
            fy.main()
            with open(filepath, 'w') as f:
                json.dump(my_list, f, indent=2)
            if index < my_length:
                randomSleep(30,60)
        else:
            fy.accout_skip += 1
            print("已完成，跳过")
    
    fy.gh_fy.update(fy.newList(my_list))
    send(title_name, fy.sendMsg())
