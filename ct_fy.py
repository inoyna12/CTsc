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
appVersion = "1.5.2"

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
                    break
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
                    self.luckDraw(luckyBlessingBagId)
                return
            else:
                self.proxies = self.get_proxy()
        send(f"{title_name}_签到失败", "签到失败")
        exit()

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
                
    # 返回数据太多，暂时不用
    def myInfo(self):
        url = "https://evosapi.fuyu.club/user/myInfo"
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
                result_decrypt = aes_cbc_decrypt(seccode, seccode, result['data'])
                print(result_decrypt)

    def luckDraw(self, activityId):
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
                print(result)
                break
            else:
                self.proxies = self.get_proxy()
        send(f"{title_name}_抽奖失败", "抽奖失败")
        exit()
        
    
    def main(self):
        self.proxies = self.get_proxy()
        self.signIn()
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
