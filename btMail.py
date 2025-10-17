# 需要关闭面板ssl

import requests
import hashlib
import time,json

# 面板地址
bt_panel = 'http://43.155.171.19:25794'  # 例如: 'http://yourpanel.com'

# API密钥
bt_api_sk = 'hTiJ1mDxhnxAjXHMKef5tkQolx3etJ5q'

def get_md5(string):
    """MD5加密函数"""
    return hashlib.md5(string.encode('utf-8')).hexdigest()

def add_mailbox(panel,api_sk):
    url = f'{panel}/plugin?action=a&name=mail_sys&s=add_mailbox'
    request_time = int(time.time())
      payload = {
      'request_token': get_md5(str(request_time) + get_md5(api_sk)),
      'request_time': request_time,
      'quota': "2 MB",
      'username': "vefwuhf1111@gkkmail.com",
      'password': "Inoyna11",
      'full_name': "李建杰11",
      'is_admin': "0"
    }
    result = requests.post(url, data=payload).json()
    print(result)

def get_mails(panel, api_sk, mail):
    url = f'{panel}/plugin?action=a&name=mail_sys&s=get_mails'
    request_time = int(time.time())
    payload = {
      'request_token': get_md5(str(request_time) + get_md5(api_sk)),
      'request_time': request_time,
      'username': mail,
      'p': "1"
    }
    result = requests.post(url, data=payload).json()
    print(result)

get_mails(bt_panel, bt_api_sk, "64654fwefw@gkkmail.com")
