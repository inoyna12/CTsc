'''
cron: 0 9 * * *
new Env('IKuuu机场');
'''
import requests
import json
import random
import time
import datetime
import os
from sendNotify import send

def random_sleep(min_val, max_val):
    num = random.randint(min_val, max_val)
    print(f"等待{num}秒后继续>>>>>>>>>>>")
    time.sleep(num)

def ql_env(name):
    if name in os.environ:
        token_list = os.environ[name].split('\n')
        if len(token_list) > 0:
            return token_list
        else:
            print(name + "变量未启用")
            sys.exit(1)
    else:
        print("未添加变量：" + name)
        sys.exit(0)    

def email_ent():
    username = email.split('@')[0]
    domain = email.split('@')[1]
    if len(username) > 2:
        hidden_username = username[0] + '*'*(len(username)-2) + username[-1]
    else:
        hidden_username = username
    hidden_email = hidden_username + '@' + domain
    return hidden_email

def main():
    session = requests.session()
    url_login = 'https://ikuuu.art/auth/login'
    url_sign = 'https://ikuuu.art/user/checkin'
    headers = {
        'Host': 'ikuuu.art',
        'user-agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.153 Mobile Safari/537.36'
    }
    data = {
        'email': email,
        'passwd': passwd,
        'code': ''
    }
    resplogin = session.post(url_login, headers=headers, data=data).json()
    if resplogin['ret'] == 1:
        respsign = session.post(url_sign, headers=headers).json()
        print(respsign)
        status = respsign['msg']
    else:
        print(resplogin)
        status = resplogin['msg']
    msg.append(f"{msg_email}：{status}")
    session.close()

if __name__ == '__main__':
    title_name = 'IKuuu机场'
    env = ql_env('ikuuu')
    msg = []
    index = 0
    print(f"共找到{len(env)}个账号")
    for info in env:
        print(f"\n{'-' * 13}正在执行第{index + 1}个账号{'-' * 13}")
        email = info.split('#')[0]
        passwd = info.split('#')[1]
        msg_email = email_ent()
        main()
        index += 1
        if index < len(env):
            random_sleep(60, 80)
    send(title_name, '\n'.join(msg))
