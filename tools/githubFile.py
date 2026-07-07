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
        github_token: Optional[str] = None,
        as_json: Optional[bool] = None  # 新增：显式指定文件类型。True为JSON，False为纯文本，None为自动识别
    ):
        """
        初始化GitHub文件操作类
        
        :param file_path: 文件在仓库中的路径
        :param repo_name: 仓库名称（格式：用户名/仓库名）
        :param github_token: GitHub Token，优先使用参数传入，其次从环境变量读取
        :param as_json: 是否作为JSON处理。若为None，则根据后缀或内容自动识别
        """
        token = github_token or os.getenv("GITHUB_TOKEN")
        self.gh = Github(token)
        self.repo = self.gh.get_repo(repo_name)
        self.file_path = file_path
        self.file_info: Optional[ContentFile] = None
        
        self.as_json = as_json
        self.cont: Any = None  # JSON模式下为 list/dict，文本模式下为 str
        
        try:
            self._refresh_file_info()
        except Exception as e:
            print(f"初始化失败: {e}")
            raise  # 抛出异常由调用者处理

    def _parse_content(self, content_bytes: bytes) -> Any:
        """
        解析文件内容。根据 self.as_json 的设定或自动识别，解析为 JSON 对象或纯文本字符串。
        """
        raw_str = content_bytes.decode("utf-8") if content_bytes else ""
        
        # 1. 如果显式指定为 JSON，或者未指定但文件以 .json 结尾
        if self.as_json is True or (self.as_json is None and self.file_path.lower().endswith('.json')):
            self.as_json = True
            if not raw_str.strip():
                return []  # 空白文件默认初始化为空列表
            try:
                return json.loads(raw_str)
            except json.JSONDecodeError:
                print(f"警告：文件 {self.file_path} 预期为 JSON，但解析失败，重置为空列表")
                return []

        # 2. 如果未显式指定，尝试自动识别：先尝试解析为 JSON
        if self.as_json is None:
            if raw_str.strip():
                try:
                    parsed_data = json.loads(raw_str)
                    self.as_json = True  # 成功解析，后续也以 JSON 模式处理
                    return parsed_data
                except json.JSONDecodeError:
                    pass
            
            # 解析 JSON 失败或文件为空，且没有 .json 后缀，则视作纯文本处理
            self.as_json = False
            return raw_str

        # 3. 显式指定为纯文本 (self.as_json is False)
        return raw_str

    def _refresh_file_info(self) -> None:
        """刷新文件信息，可能抛出异常"""
        try:
            self.file_info = self.repo.get_contents(self.file_path)
            
            if self.file_info.size > self.MAX_FILE_SIZE:
                raise ValueError(
                    f"文件 {self.file_path} 大小超过 {self.MAX_FILE_SIZE/1024/1024}MB 限制"
                )
            
            # 使用统一的安全解析函数
            self.cont = self._parse_content(self.file_info.decoded_content)
            
        except GithubException as e:
            if e.status == 404:
                raise FileNotFoundError(f"文件 {self.file_path} 不存在") from e
            raise RuntimeError(f"GitHub API错误: {e}") from e

    def update(self, new_data: Any) -> None:
        """
        更新文件内容并确保本地数据同步
        
        :param new_data: 需要写入的新数据。
                         如果是 JSON 模式，可以是 dict/list 等可序列化对象；
                         如果是文本模式，可以是字符串，也可以是列表（列表会被按行写入）。
        """
        # 确保我们在提交前知道最新的类型状态
        self._refresh_file_info()

        if self.as_json:
            try:
                # ensure_ascii=False 可以保证中文（如“四方”）不会被转义为 \u 格式
                encoded_content = json.dumps(new_data, indent=2, ensure_ascii=False).encode("utf-8")
            except TypeError as e:
                raise ValueError("数据无法序列化为JSON格式") from e
        else:
            # 文本模式：如果传入的是列表/元组，自动用换行符拼接成多行文本
            if isinstance(new_data, (list, tuple)):
                txt_content = "\n".join(map(str, new_data))
            else:
                txt_content = str(new_data)
            encoded_content = txt_content.encode("utf-8")

        commit_message = (
            f"Updated {self.file_path}\n"
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        try:
            # 提交更新并获取返回结果
            update_result: Dict = self.repo.update_file(
                path=self.file_path,
                message=commit_message,
                content=encoded_content,
                sha=self.file_info.sha  # type: ignore
            )
            
            # 直接使用 API 返回的新内容更新本地信息
            self.file_info = update_result["content"]
            self.cont = self._parse_content(self.file_info.decoded_content)
            
            print(f"成功更新 {self.file_path}")
            
        except GithubException as e:
            if e.status == 409:
                raise RuntimeError("文件已被其他进程修改，请刷新后重试") from e
            raise RuntimeError(f"更新失败: {e}") from e

    def create(self, initial_data: Any = None) -> None:
        """创建新文件"""
        if initial_data is None:
            # 如果是 JSON 模式默认 []，文本模式默认空字符串
            initial_data = [] if self.as_json is not False else ""
            
        try:
            if self.as_json is not False:
                encoded_content = json.dumps(initial_data, indent=2, ensure_ascii=False).encode("utf-8")
            else:
                if isinstance(initial_data, (list, tuple)):
                    txt_content = "\n".join(map(str, initial_data))
                else:
                    txt_content = str(initial_data)
                encoded_content = txt_content.encode("utf-8")

            self.repo.create_file(
                path=self.file_path,
                message=f"Create {self.file_path}",
                content=encoded_content
            )
            self._refresh_file_info()
        except GithubException as e:
            raise RuntimeError(f"创建文件失败: {e}") from e
