'''
cron: 36 9 * * *
new Env('吉利汽车签到');
'''
import requests
import json
import time
import random
import datetime
import execjs
from utils.utils import randomSleep,send_request
from notify import send

title_name = '吉利汽车签到'
version = "3.23.2"

msg = [] #推送内容
signSuccess_num = 0 #签到成功数量
signFail_num = 0 #签到失败数量
scriptStop_num = 10 #签到失败数量大于当前值停止运行

filepath = "/ql/data/env/jlqc.json"
js_code = open('utils/jlqc.js', 'r', encoding='utf-8').read()
js = execjs.compile(js_code)
year = datetime.datetime.now().year
month = datetime.datetime.now().month

api_url = "http://v2.api.juliangip.com/company/postpay/getips?num=1&pt=1&result_type=json&trade_no=6130652715138961&sign=3b1896626239e61a182b00ac5582d07f"

def get_proxies():
    proxy_json = send_request(api_url, 'GET')
    if proxy_json['code'] == 200:
        proxy_ip = proxy_json['data']['proxy_list'][0]
        print("当前代理IP：" + proxy_ip)
        proxies = {
          "http": proxy_ip,
          "https": proxy_ip,
        }
        return proxies
    else:
        print("获取代理IP失败！")
        send(title_name + "\n\n异常", "获取代理IP失败！")
        exit()

def random_ua():
    android_version = str(random.randint(7, 14))
    device_code = ''.join(random.choices('0123456789ABCDEF', k=8))
    build_number = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=16))
    return f"Dalvik/2.1.0 (Linux; U; Android {android_version}; {device_code} Build/{build_number})"

#签到
def sign():
    proxies = get_proxies()
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
        'token': user_data['token'],
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
        send(title_name + "\n\n异常", "连接失败")
        return
    print(result)
    print(f"签到：{result['code']}")
    # 遍历字典中的所有值，而不是键
    if "异常" in result.values():
        send(title_name + "\n\n异常", "签到异常")
        exit()
    if result['code'] == 'success' or result['message'] == '您已签到,请勿重复操作!':
        global signSuccess_num
        signSuccess_num = signSuccess_num + 1
    else:
        global signFail_num
        signFail_num = signFail_num + 1
        print(result)

if __name__ == '__main__':
    with open(filepath, 'r') as f:
        all_data = json.load(f)
    print(f"\n共找到{len(all_data)}个账号")
    for index, user_data in enumerate(all_data, start = 1):
        print(f"\n{'-' * 13}正在执行第{index}/{len(all_data)}个账号{'-' * 13}")
        print(f"{user_data['phone']}：")
        sign()
        if signFail_num >= scriptStop_num:
            send(title_name, f"签到失败数量：{signFail_num}，脚本停止运行")
            exit()
        if index < len(all_data):
            randomSleep(30,60)
    send(f"{title_name}：{len(all_data)}", f"成功数量：{signSuccess_num}，失败数量：{signFail_num}")
