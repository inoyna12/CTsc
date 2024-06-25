'''
cron: 36 9 * * *
new Env('吉利汽车查询');
'''
import requests
import json
from utils.utils import randomSleep,send_request
from fake_useragent import UserAgent
from notify import send

title_name = '吉利汽车查询'
version = "3.20.0"
filepath = "/ql/data/env/jlqc.json"

def random_ua():
    ua = UserAgent()
    base_ua = ua.chrome
    custom_ua = f"{base_ua} MQQBrowser/6.2 TBS/046281 Mobile Safari/537.36/android/geelyApp"
    return custom_ua

def available():
    url = 'https://app.geely.com/api/v1/point/available'
    headers = {
        "Host": "app.geely.com",
        "accept": "application/json, text/plain, */*",
        "user-agent": random_ua(),
        "token": at_dict['token'],
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    result = send_request(url, 'GET', headers=headers)
    print(result)
    if result['code'] == "success":
        at_dict['availablePoint'] = result['data']['availablePoint']
        global success_num
        success_num = success_num + 1
    else:
        global fail_num
        fail_num = fail_num + 1

if __name__ == '__main__':
    success_num = 0
    fail_num = 0
    with open(filepath, 'r') as f:
        accountAll_list = json.load(f)
    print(f"\n共找到{len(accountAll_list)}个账号")
    for index, at_dict in enumerate(accountAll_list, start = 1):
        print(f"\n{'-' * 13}正在执行第{index}/{len(accountAll_list)}个账号{'-' * 13}")
        print(f"{at_dict['phone']}：")
        available()
        if index < len(accountAll_list):
            randomSleep(30,60)
    with open(filepath, 'w') as f:
        json.dump(accountAll_list, f, indent=2)
    send(f"{title_name}：{len(accountAll_list)}", f"成功数量：{success_num}，失败数量：{fail_num}")
