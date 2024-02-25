'''
cron: 6 13 * * *
new Env('哪吒token提取');
'''
import json,os,sys
from utils.github_file_manager import GithubFileManager

git_token = []

def ql_env(name):
    if name in os.environ:
        token_list = os.environ[name].split('\n')
        if len(token_list) > 0:
            return token_list
        else:
            print("变量未启用")
            sys.exit(1)
    else:
        print("未添加变量")
        sys.exit(0)

def git_github():
    access_token = os.getenv('github_token')
    file_manager = GithubFileManager(access_token)
    repo_name = "inoyna12/updateTeam"
    branch = "master"
    file_path = "哪吒汽车/refresh_token.txt"
    new_content = '\n'.join(git_token)
    commit_message = f"Update {file_path}"
    file_manager.update_file_content(repo_name, file_path, new_content, commit_message, branch)
        
phone_list = ql_env("NZmy_phone")
print(f"共找到{len(phone_list)}个账号\n\n")
filepath = "/ql/data/env/nzqc.json"

with open(filepath, "r") as f:
    info_new = json.load(f)

for phone in phone_list:
    for info in info_new:
        if info['mobile'] == phone:
            print(phone + '\n')
            print(info['refresh_token'])
            print("\n" + "-------------------------------------------" + "\n")
            token = phone + '----' + info['refresh_token']
            git_token.append(token)
            break
            
git_github()
