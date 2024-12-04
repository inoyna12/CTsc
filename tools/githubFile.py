import os
import json
from datetime import datetime
from github import Github, GithubException

class GithubFile:
    def __init__(self, file_path):
        self.gh = Github(os.getenv('github_token'))
        self.repo = self.gh.get_repo('inoyna12/updateTeam')
        self.file_path = file_path
        self._refresh_file_info()

    def _refresh_file_info(self):
        """刷新文件信息"""
        try:
            self.file_info = self.repo.get_contents(self.file_path)
            if self.file_info.size > 1048576:  # 1MB 限制
                print(f"文件 {self.file_path} 大小超过限制，无法直接读取。")
                self.lst = None
            else:
                self.lst = json.loads(self.file_info.decoded_content.decode('utf-8'))
        except GithubException as e:
            if e.status == 404:
                print(f"文件 {self.file_path} 不存在。")
            else:
                print(f"读取文件时出错: {e}")
            exit()

    def update(self, new_lst):
        """更新文件"""
        encoded_file_content = json.dumps(new_lst, indent=2).encode('utf-8')
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        commit_message = f"Updated {self.file_path}\n{current_time}"
        try:
            # 在更新前先刷新文件信息
            self._refresh_file_info()
            self.repo.update_file(
                self.file_path, 
                commit_message, 
                encoded_file_content, 
                self.file_info.sha
            )
            print(f"更新 github {self.file_path} 文件成功！")
        except Exception as e:
            print(f"更新文件时出错: {e}")
