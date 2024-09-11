'''
cron: 2 0 * * *
new Env('更新账号');
'''

import json,os
from github import Github
from notify import send

ql_jlyh_filepath = "/ql/data/env/jlyh.json"
  
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

class Jlyh:
    def __init__(self, filepath):
        with open(filepath, 'r') as f:
            self.all_data = json.load(f)
        self.update_num = 0
        self.add_num= 0
        self.filepath = filepath
        self.bef_num = len(self.all_data)
        self.gh_jlyh = GithubFile('吉利银河/jlyh.json')
        self.gh_zdjl = GithubFile('吉利银河/zdjl.json')
              
    def update(self):
        if len(self.gh_zdjl.content) == 0:
            print("空列表，跳过")
            return
        for zdjl_dict in self.gh_zdjl.content:
            for my_dict in self.all_data:
                if my_dict['phone'] == zdjl_dict['phone']:
                    my_dict['password'] = zdjl_dict['password']
                    my_dict['refreshToken'] = zdjl_dict['refreshToken']
                    my_dict['imei'] = zdjl_dict['imei']
                    my_dict['deviceSN'] = zdjl_dict['deviceSN']
                    my_dict['sweet_security_info'] = zdjl_dict['sweet_security_info']
                    self.update_num += 1
                    print(f"更新次数：{self.update_num}，号码：{zdjl_dict['phone']}")
                    break
            else:
                zdjl_dict['availablePoints'] = 0
                zdjl_dict['signdate'] = ''
                self.all_data.append(zdjl_dict)
                self.add_num += 1
                print(f"增加次数：{self.add_num}，号码：{zdjl_dict['phone']}")
        
        self.gh_jlyh.update(self.all_data)
        self.gh_zdjl.update([])
        with open(self.filepath, 'w') as f:
            json.dump(self.all_data, f, indent=2)
        send("吉利银河更新账号", f"增加账号{self.add_num}次，更新账号{self.update_num}次\n原账号数量：{self.bef_num}，现账号数量：{len(self.all_data)}")
        
Jlyh(ql_jlyh_filepath).update()
