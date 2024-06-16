'''
cron: 2 0 * * *
new Env('吉利汽车更新账号');
'''
import json
import os,random
from utils.github_file_manager import GithubFileManager
from notify import send

ql_filepath = "/ql/data/env/jlqc.json"

access_token = os.getenv('github_token')
repo_name = "inoyna12/updateTeam"
branch = "master"
gh_filepath = "吉利汽车/账号密码.txt"
new_content = '' #修改github文件内容
commit_message = f"Update {gh_filepath}"

def get_gh_fileContent():
    file_content = fileManager.get_file_content(repo_name, gh_filepath, branch)
    if len(file_content) == 0:
        print(f"{gh_filepath}  内容为空")
        exit(0)
    file_content_list = list(filter(None, file_content.split('\n')))
    return file_content_list

def updateFile():
    global update_num, add_num
    gh_fileContent_list = get_gh_fileContent()
    for item in gh_fileContent_list:
        phone, password, token, refreshToken = item.split('----')
        for at_dict in accountAll_list:
            if at_dict['phone'] == phone:
                at_dict['password'] = password
                at_dict['token'] = token
                at_dict['refreshToken'] = refreshToken
                update_num += 1
                print(f"更新次数：{update_num}，号码：{phone}")
                break
        else:
            account_dict = {
                "phone": phone,
                "password": password,
                "token": token,
                "refreshToken": refreshToken,
                "availablePoint": 0
            }
            accountAll_list.append(account_dict)
            add_num += 1
            print(f"增加次数：{add_num}，号码：{phone}")

if __name__ == '__main__':
    update_num = 0
    add_num = 0
    fileManager = GithubFileManager(access_token)
    with open(ql_filepath, 'r') as f:
        accountAll_list = json.load(f)
    updateFile()
    random.shuffle(accountAll_list)
    with open(ql_filepath, 'w') as f:
        json.dump(accountAll_list, f, indent=2)
    print('JSON数据更新完成。')
    fileManager.update_file_content(repo_name, gh_filepath, new_content, commit_message, branch)
    
    send("吉利汽车", f"增加账号{add_num}次，更新账号{update_num}次")
