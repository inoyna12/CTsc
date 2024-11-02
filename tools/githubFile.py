import os
from github import Github

class GithubFile:
    def __init__(self, file_path):
        self.gh = Github(os.getenv('github_token'))
        self.repo = self.gh.get_repo('inoyna12/updateTeam')
        self.file_path = file_path
        self.commit_message = f"Updated {file_path}"
        self.file_info = self.repo.get_contents(self.file_path)
        if self.file_info.size > 1048576:  # 1MB 限制
            print(f"文件 {self.file_path} 大小超过限制，无法直接读取。")
            self.lst = None
        else:
            self.lst = json.loads(self.file_info.decoded_content.decode('utf-8'))
            print(f"读取 github {self.file_path} 文件成功！")

    def update(self, new_lst):
        encoded_file_content = json.dumps(new_lst, indent=2).encode('utf-8')
        try:
            self.repo.update_file(self.file_path, self.commit_message, encoded_file_content, self.file_info.sha)
            print(f"更新 github {self.file_path} 文件成功！")
        except Exception as e:
            print(f"更新文件时出错: {e}")
