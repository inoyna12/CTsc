'''
cron: 2 0 * * *
new Env('dyxw添加');
'''
import re
import json
import os
from utils.github_file_manager import GithubFileManager
from urllib.parse import unquote
from notify import send

def extract_session_and_wdata3(encoded_str):
    decoded_str = unquote(unquote(encoded_str))
    session_id_match = re.search(r'sessionId=([a-f0-9]+)', decoded_str)
    session_id = session_id_match.group(1) if session_id_match else None
    wdata3_match = re.search(r'(wdata3=[^;]+)', decoded_str)
    wdata3 = wdata3_match.group(1) if wdata3_match else None
    return session_id, wdata3

filepath = "/ql/data/env/dyxw.json"
update_account = 0
add_account = 0
access_token = os.getenv('github_token')
file_manager = GithubFileManager(access_token)
repo_name = "inoyna12/CTsc"
branch = "master"
file_path = "token/笛杨新闻/账号密码.txt"
new_content = ''
commit_message = f"Update {file_path}"

current_content = file_manager.get_file_content(repo_name, file_path, branch)

if len(current_content) == 0:
    print(f"{file_path}  内容为空")
    exit(0)
current_content_list = list(filter(None, current_content.split('\n')))

with open(filepath, 'r', encoding='utf-8') as file:
    data_list = json.load(file)

for item in current_content_list:
    phone, password, cookie = item.split('----')
    sessionId, wdata3 = extract_session_and_wdata3(cookie)
    if sessionId is None or wdata3 is None:
        send("笛杨新闻", f"账号{phone}添加失败")
        continue
    found = False
    for data in data_list:
        if data['phone'] == phone:
            data['password'] = password
            data['cookie'] = cookie
            data['sessionId'] = sessionId
            data['wdata3'] = wdata3
            found = True
            update_account += 1
            print(f"更新次数：{update_account}，号码：{phone}")
            break
    if not found:
        account_dict = {
            "phone": phone,
            "password": password,
            "cookie": cookie,
            "sessionId": sessionId,
            "wdata3": wdata3,
            "total_integral": 0
        }
        data_list.append(account_dict)
        add_account += 1
        print(f"增加次数：{add_account}，号码：{phone}")

with open(filepath, 'w', encoding='utf-8') as file:
    json.dump(data_list, file, indent=4)

print('JSON数据更新完成。')
file_manager.update_file_content(repo_name, file_path, new_content, commit_message, branch)
    
send("笛杨新闻", f"更新账号{update_account}次\n增加账号{add_account}次")
