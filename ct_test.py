import json,os
from github import Github

filepath = "/ql/data/env/jlqc.json"
with open(filepath, 'r') as f:
    all_data = json.load(f)
    
    
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
        
        
gh_jlInfo_list = GithubFile('吉利汽车/AccountInfo.json')
gh_jlInfo_list.update(all_data)
    
    
