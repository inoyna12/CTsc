'''
cron: 58 9 * * *
new Env('广汽传祺查询');
'''

import requests
import json
import hashlib
import time
import random
from sendNotify import send
from os import environ

def get_md5_signature(input_str):
    # 创建一个 hashlib.md5() 对象
    m = hashlib.md5()
    
    # 将输入字符串编码成 bytes 类型，并进行 MD5 计算
    m.update(input_str.encode('utf-8'))
    
    # 返回计算结果的十六进制表示
    return m.hexdigest()
    
def Gdou(token):
    reqNonc = random.randint(100000, 999999)
    timestamp = str(int(time.time() * 1000)) 
    reqSign = f"signature{reqNonc}{timestamp}17aaf8118ffb270b766c6d6774317a134.1.0"
    md5_reqSign = get_md5_signature(reqSign)
    url = 'https://gsp.gacmotor.com/gateway/app-api/account/getusergdou'
    headers = {
        'token': token,
        'channel': 'unknown',
        'platformNo': 'Android',
        'osVersion': '12',
        'version': '4.1.0',
        'imei': 'fc723391358dedbf',
        'imsi': 'unknown',
        'deviceType': 'Android',
        'registrationID': '100d855908576d8e1ed',
        'deviceCode': 'fc723391358dedbf',
        'verification': 'signature',
        'reqTs': f'{timestamp}',
        'reqNonc': f'{reqNonc}',
        'reqSign': f"{md5_reqSign}",
        'Host': 'gsp.gacmotor.com',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/3.10.0',
    }
    response = requests.get(url=url, headers=headers)
    result = response.json()
    print(result)
    return result['data']
    
def Phone(token):
    reqNonc = random.randint(100000, 999999)
    timestamp = str(int(time.time() * 1000)) 
    reqSign = f"signature{reqNonc}{timestamp}17aaf8118ffb270b766c6d6774317a134.1.0"
    md5_reqSign = get_md5_signature(reqSign)
    url = 'https://gsp.gacmotor.com/gateway/webapi/account/getUserInfoV2'
    headers = {
        'token': token,
        'channel': 'unknown',
        'platformNo': 'Android',
        'osVersion': '12',
        'version': '4.1.0',
        'imei': 'fc723391358dedbf',
        'imsi': 'unknown',
        'deviceType': 'Android',
        'registrationID': '100d855908576d8e1ed',
        'deviceCode': 'fc723391358dedbf',
        'verification': 'signature',
        'reqTs': f'{timestamp}',
        'reqNonc': f'{reqNonc}',
        'reqSign': f"{md5_reqSign}",
        'Host': 'gsp.gacmotor.com',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/3.10.0',
    }
    data = 'userIdStr=NDkzNTE5Mg%3D%3D'
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
    print(result)
    mobile = result['data']['mobile']
    Mobile = mobile[:3] + "****" + mobile[7:]
    gdou = Gdou(token)
    Mobile_data = f"{Mobile}：{gdou}G豆\n"
    print(Mobile_data)
    return Mobile_data

def ql_env():
    if "gqcqCookie" in os.environ:
        token_list = os.environ['gqcqCookie'].split('\n')
        if len(token_list) > 0:
            return token_list
        else:
            print("gqcqCookie变量未启用")
            sys.exit(1)
    else:
        print("未添加gqcqCookie变量")
        sys.exit(0)

if __name__ == '__main__':
    msg = ""
    index = 1
    quantity = ql_env()
    print (f"共找到{len(quantity)}个账号")
    for token in quantity:
        print(f"------------正在执行第{index}个账号----------------")
        msg += Phone(token)
        time.sleep(5)
        index += 1
    send('广汽传祺查询', msg)

