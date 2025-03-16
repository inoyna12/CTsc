import os
import json
from datetime import datetime
from typing import Any, Optional, Dict
from github import Github, GithubException
from github.ContentFile import ContentFile

class GithubFile:
    MAX_FILE_SIZE: int = 1048576  # 1MB，类常量提高可维护性

    def __init__(
        self, 
        file_path: str,
        repo_name: str = "inoyna12/updateTeam",  # 参数化仓库名称
        github_token: Optional[str] = None
    ):
        """
        初始化GitHub文件操作类
        
        :param file_path: 文件在仓库中的路径
        :param repo_name: 仓库名称（格式：用户名/仓库名）
        :param github_token: GitHub Token，优先使用参数传入，其次从环境变量读取
        """
        self.gh = Github(os.getenv("GITHUB_TOKEN"))  # 更通用的环境变量名
        self.repo = self.gh.get_repo(repo_name)
        self.file_path = file_path
        self.file_info: Optional[ContentFile] = None
        self.cont: Optional[list] = None
        
        try:
            self._refresh_file_info()
        except Exception as e:
            print(f"初始化失败: {e}")
            raise  # 抛出异常由调用者处理

    def _refresh_file_info(self) -> None:
        """刷新文件信息，可能抛出异常"""
        try:
            self.file_info = self.repo.get_contents(self.file_path)
            
            if self.file_info.size > self.MAX_FILE_SIZE:
                raise ValueError(
                    f"文件 {self.file_path} 大小超过 {self.MAX_FILE_SIZE/1024/1024}MB 限制"
                )
                
            self.cont = json.loads(self.file_info.decoded_content.decode("utf-8"))
            
        except GithubException as e:
            if e.status == 404:
                raise FileNotFoundError(f"文件 {self.file_path} 不存在") from e
            raise RuntimeError(f"GitHub API错误: {e}") from e

    def update(self, new_lst: Any) -> None:
        """
        更新文件内容并确保本地数据同步
        
        :param new_lst: 需要写入的新数据（必须可JSON序列化）
        """
        try:
            encoded_content = json.dumps(new_lst, indent=2).encode("utf-8")
        except TypeError as e:
            raise ValueError("数据无法序列化为JSON格式") from e

        commit_message = (
            f"Updated {self.file_path}\n"
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        try:
            # 提交前必须刷新SHA，避免冲突
            self._refresh_file_info()
            
            # 提交更新并获取返回结果
            update_result: Dict = self.repo.update_file(
                path=self.file_path,
                message=commit_message,
                content=encoded_content,
                sha=self.file_info.sha  # type: ignore
            )
            
            # 直接使用API返回的新内容更新本地信息
            self.file_info = update_result["content"]
            self.cont = json.loads(self.file_info.decoded_content.decode("utf-8"))
            
            print(f"成功更新 {self.file_path}")
            
        except GithubException as e:
            if e.status == 409:
                raise RuntimeError("文件已被其他进程修改，请刷新后重试") from e
            raise RuntimeError(f"更新失败: {e}") from e

    def create(self, initial_data: Any = None) -> None:
        """创建新文件（补充功能）"""
        if initial_data is None:
            initial_data = []
            
        try:
            encoded_content = json.dumps(initial_data, indent=2).encode("utf-8")
            self.repo.create_file(
                path=self.file_path,
                message=f"Create {self.file_path}",
                content=encoded_content
            )
            self._refresh_file_info()
        except GithubException as e:
            raise RuntimeError(f"创建文件失败: {e}") from e
