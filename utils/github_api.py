#10/8
import requests
import base64
from datetime import datetime

def update_github_file(
    file_path,
    new_content,
    username="inoyna12",
    repository_name="CTsc",
    branch_name="master",
    access_token="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",
    committer_name="inoyna12",
    committer_email="inoyna12@163.com"
    ):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    new_file_content = str(new_content)  # 将变量转换为字符串
    
    # 将新的内容编码为 Base64，并发送 PUT 请求更新内容
    new_file_content_bytes = str.encode(new_file_content)
    new_file_content_b64 = base64.b64encode(new_file_content_bytes).decode()
    
    # 设置 API 访问 URL 和请求头部信息
    url = f"https://api.github.com/repos/{username}/{repository_name}/contents/{file_path}?ref={branch_name}"
    headers = {"Authorization": f"token {access_token}"}
    
    # 发送 GET 请求到 GitHub API 获取文件内容
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        create_url = f"https://api.github.com/repos/{username}/{repository_name}/contents/{file_path}"
        payload = {
            "message": f"Create {file_path}\n{current_time}",
            "committer": {
                "name": committer_name,
                "email": committer_email
            },
            "content": new_file_content_b64,
            "branch": branch_name
        }
        response = requests.put(create_url, headers=headers, json=payload)
        if response.status_code == 201:
            msg = f"{file_path} 文件创建成功\n"
        else:
            print(response.text)
            msg = f"{file_path} 文件创建失败\n"

        return msg
        
    data = response.json()
    payload = {
        "message": f"Update {file_path}\n{current_time}",
        "committer": {
            "name": committer_name,
            "email": committer_email
        },
        "content": new_file_content_b64,
        "sha": data['sha']
    }
    response = requests.put(url, headers=headers, json=payload)

    # 打印结果
    if response.status_code == 200:
        msg = f"{file_path} 文件更新成功\n"
    else:
        print(response.text)
        msg = f"{file_path} 文件更新失败\n"

    return msg
