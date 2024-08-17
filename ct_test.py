'''
cron: 2 0 * * *
new Env('吉利汽车更新账号');
'''
import json
import os,random
from github import Github

data_new = []

filepath = "/ql/data/env/jlqc.json"
with open(filepath, 'r') as f:
    all_data = json.load(f)

gh = Github(os.getenv('github_token'))
gh_repo = gh.get_repo("inoyna12/updateTeam")
gh_file_path = "吉利汽车/TokenUnchecked.json"
gh_commit_message = "Updated the file"
gh_file_info = gh_repo.get_contents(gh_file_path)
gh_file_content = json.loads(gh_file_info.decoded_content.decode('utf-8'))

for i in all_data:
    if len(data_new) > 45:
        print("超过45")
        break
    phone = i['phone']
    password = i['password']
    print(phone)
    dict_new = {'phone': phone, 'password': password}
    data_new.append(dict_new)

gh_repo.update_file(gh_file_path, gh_commit_message, json.dumps(data_new, indent=2), gh_file_info.sha)
