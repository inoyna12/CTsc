'''
cron: 36 6 * * *
new Env('吉利汽车签到');
'''
import json
import os
import time
import random
import datetime
import execjs
from utils.utils import randomSleep,send_request
from github import Github
from notify import send

title_name = '吉利汽车签到'
version = "3.23.2"

success_num = 0 #签到成功数量
fail_num = 0 #签到失败数量
repeat_num = 0 #重复签到
availablePoint8 = 0
availablePoint16 = 0
availablePoint88 = 0
token_unchecked = 0

filepath = "/ql/data/env/jlqc.json"
with open(filepath, 'r') as f:
    all_data = json.load(f)

gh = Github(os.getenv('github_token'))
gh_repo = gh.get_repo("inoyna12/updateTeam")
gh_file_path = "吉利汽车/TokenUnchecked.json"
gh_commit_message = "Updated the file"
gh_file_info = gh_repo.get_contents(gh_file_path)
gh_file_content = json.loads(gh_file_info.decoded_content.decode('utf-8'))

js_code = open('utils/jlqc.js', 'r', encoding='utf-8').read()
js = execjs.compile(js_code)
year = datetime.datetime.now().year
month = datetime.datetime.now().month

def get_proxies():
    for i in range(3):
        proxy_json = send_request("http://v2.api.juliangip.com/company/postpay/getips?num=1&pt=1&result_type=json&trade_no=6130652715138961&sign=3b1896626239e61a182b00ac5582d07f", 'GET')
        if proxy_json['code'] == 200:
            proxy_ip = proxy_json['data']['proxy_list'][0]
            print("当前代理IP：" + proxy_ip)
            proxies = {
              "http": proxy_ip,
              "https": proxy_ip,
            }
            return proxies
        else:
            print(proxy_json)
            time.sleep(60)
    send(title_name + "---异常", "获取代理IP失败！")
    exit()

def random_ua():
    android_version = str(random.randint(7, 14))
    device_code = ''.join(random.choices('0123456789ABCDEF', k=8))
    build_number = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))
    return f"Dalvik/2.1.0 (Linux; U; Android {android_version}; {device_code} Build/{build_number})"

#签到
def sign():
    proxies = get_proxies()
    global success_num, fail_num, repeat_num, availablePoint8, availablePoint16, availablePoint88, token_unchecked
    url = 'https://app.geely.com/api/v1/userSign/sign/risk'
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    current_timestamp = int(time.time())
    json_data = {
        "signDate": str(formatted_time),
        "ts": str(current_timestamp),
        "cId":"BLqo2nmmoPgGuJtFDWlUjRI2b1b"
    }
    headers = {
        'Host': 'app.geely.com',
        'accept': 'application/json, text/plain, */*',
        'token': user_dict['token'],
        'version': version,
        'x-data-sign': js.call("enen", json_data),
        'User-Agent': random_ua(),
        'content-type': 'application/json',
        'origin': 'https://app.geely.com',
        'referer': 'https://app.geely.com/app-h5/sign-in?showTitleBar=0',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    result = send_request(url, 'POST', headers=headers, json=json_data, proxies=proxies)
    if result is False:
        fail_num = fail_num + 1
        send(title_name + "---异常", "连接失败")
        return
    print(result)
    if result['code'] == 'success':
        success_num = success_num + 1
        if result['data'] == {}:
            pass
        elif 'id' in result['data']:
            if result['data']['id'] == '1':
                availablePoint8 = availablePoint8 + 1
            elif result['data']['id'] == '2':
                availablePoint16 = availablePoint16 + 1
            elif result['data']['id'] == '3':
                availablePoint88 = availablePoint88 + 1
        else:
            send(title_name + phone, "未知响应体")
            exit()
    elif result['code'] == 'fail':
        if result['message'] == '您已签到,请勿重复操作!':
            repeat_num = repeat_num + 1
        else:
            fail_num = fail_num + 1
            send(title_name + phone, "未知响应体")
            exit()
    elif result['code'] == 'token.unchecked':
        token_unchecked = token_unchecked + 1
        for i in gh_file_content:
            if i['phone'] == phone:
                print("号码已存在，不加入")
                break
        else:
            dict_new = {'phone': phone, 'password': password}
            gh_file_content.append(dict_new)
    else:
        fail_num = fail_num + 1
        send(title_name + phone, "未知响应体")
        exit()

if __name__ == '__main__':
    print(f"共找到{len(all_data)}个账号")
    for index, user_dict in enumerate(all_data, start = 1):
        print(f"\n{'-' * 13}正在执行第{index}/{len(all_data)}个账号{'-' * 13}")
        phone = user_dict['phone']
        password = user_dict['password']
        print(phone + "：")
        sign()
        if fail_num >= 10:
            send(title_name, f"签到失败数量：{fail_num}，脚本停止运行")
            exit()
        if index < len(all_data):
            randomSleep(30,60)
    if token_unchecked > 0:
        gh_repo.update_file(gh_file_path, gh_commit_message, json.dumps(gh_file_content, indent=2), gh_file_info.sha)
    msg = f'''
    账号总数：{len(all_data)}
    成功签到：{success_num}
    失败签到：{fail_num}
    重复签到：{repeat_num}
    token失效：{token_unchecked}
    8吉分：{availablePoint8}
    16吉分：{availablePoint16}
    88吉分：{availablePoint88}
    '''
    send(title_name, msg)
