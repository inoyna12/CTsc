'''
cron: 36 9 * * *
new Env('吉利汽车刷新token');
'''
import requests
import json,os,time
from utils.utils import randomSleep,send_request
from github import Github
from notify import send

title_name = '吉利汽车刷新token'
version = "3.23.2"

success_num = 0
fail_num = 0
    
filepath = "/ql/data/env/jlqc.json"
with open(filepath, 'r') as f:
    all_data = json.load(f)

gh = Github(os.getenv('github_token'))
gh_repo = gh.get_repo("inoyna12/updateTeam")
gh_file_path = "吉利汽车/AccountInfo.json"
gh_commit_message = "Updated the file"
gh_file_info = gh_repo.get_contents(gh_file_path)
gh_file_content = json.loads(gh_file_info.decoded_content.decode('utf-8'))

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

def refresh():
    proxies = get_proxies()
    global success_num, fail_num
    url = "https://app.geely.com/api/v1/user/refresh"
    params = {
        'refreshToken': at_dict['refreshToken']
    }
    headers = {
        "Host": "app.geely.com",
        "x-refresh-token": "true",
        "token": at_dict['token'],
        "appversion": version,
        "platform": "Android"
    }
    result = send_request(url, 'GET', params=params, headers=headers, proxies=proxies)
    if result is False:
        fail_num = fail_num + 1
        send(title_name + "---异常", "连接失败")
        return
    print(result)
    if result['code'] == "success":
        at_dict['token'] = result['data']['token']
        at_dict['refreshToken'] = result['data']['refreshToken']
        success_num = success_num + 1
    else:
        fail_num = fail_num + 1

if __name__ == '__main__':
    print(f"\n共找到{len(all_data)}个账号")
    for index, at_dict in enumerate(all_data, start = 1):
        print(f"\n{'-' * 13}正在执行第{index}/{len(all_data)}个账号{'-' * 13}")
        print(f"{at_dict['phone']}：")
        refresh()
        with open(filepath, 'w') as f:
            json.dump(all_data, f, indent=2)
        if index < len(all_data):
            randomSleep(30,60)
    gh_repo.update_file(gh_file_path, gh_commit_message, json.dumps(all_data, indent=2), gh_file_info.sha)
    send(f"{title_name}：{len(all_data)}", f"成功数量：{success_num}，失败数量：{fail_num}")
