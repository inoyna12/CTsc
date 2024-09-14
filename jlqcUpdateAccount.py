'''
cron: 2 0 * * *
new Env('吉利汽车更新账号');
'''

import json,os
from github import Github
from notify import send
  
class GithubFile:
    def __init__(self, file_path):
        self.gh = Github(os.getenv('github_token'))
        self.repo = self.gh.get_repo('inoyna12/updateTeam')
        self.file_path = file_path
        self.commit_message = "Updated the file"
        self.file_info = self.repo.get_contents(self.file_path)
        self.content = json.loads(self.file_info.decoded_content.decode('utf-8'))
        print(f"读取gtihub {self.file_path} 文件成功！")
        
    def update(self, new_content):
        encoded_file_content = json.dumps(new_content, indent=2).encode('utf-8')
        self.repo.update_file(self.file_path, self.commit_message, encoded_file_content, self.file_info.sha)
        print(f"更新github {self.file_path} 文件成功！")
   
def updateFile():
    global update_num, add_num
    for gh_dict in gh_list.content:
        for at_dict in all_data:
            if at_dict['phone'] == gh_dict['phone']:
                at_dict['password'] = gh_dict['password']
                at_dict['token'] = gh_dict['token']
                at_dict['refreshToken'] = gh_dict['refreshToken']
                update_num += 1
                print(f"更新次数：{update_num}，号码：{gh_dict['phone']}")
                break
        else:
            gh_dict['availablePoint'] = 0
            gh_dict['signdate'] = ''
            all_data.append(gh_dict)
            add_num += 1
            print(f"增加次数：{add_num}，号码：{gh_dict['phone']}")



filepath = "/ql/data/env/jlqc.json"
with open(filepath, 'r') as f:
    all_data = json.load(f)

update_num = 0
add_num = 0
all_num = len(all_data)
gh_list = GithubFile('吉利汽车/账号密码.json')
if len(gh_list.content) == 0:
    print("空列表，退出运行。")
    exit()
updateFile()
with open(filepath, 'w') as f:
    json.dump(all_data, f, indent=2)
    
gh_list.update([])    

AccountInfo = GithubFile('吉利汽车/AccountInfo.json')
AccountInfo.update(all_data)
print(f"增加账号{add_num}次，更新账号{update_num}次\n原账号数量：{all_num}，现账号数量：{len(all_data)}")
send("吉利汽车更新账号", f"增加账号{add_num}次，更新账号{update_num}次\n原账号数量：{all_num}，现账号数量：{len(all_data)}")
