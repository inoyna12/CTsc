import requests
import time
import string
import random
import json
from requests.exceptions import RequestException

# --- 配置区域 ---
# Mail.tm 的 API 基础地址
BASE_URL = "https://api.mail.tm"
# 请求超时时间（秒）
TIMEOUT = 10 
# 如果你在国内且网络不通，请在此处填写代理，例如:
# PROXY = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
PROXY = None 

# --- 函数定义 ---

def get_domain():
    """获取随机可用域名"""
    res = requests.get(f"{BASE_URL}/domains", timeout=TIMEOUT, proxies=PROXY)
    try:
        data = res.json()
        domains = data.get('hydra:member', [])
        
        if not domains:
            raise Exception("API 返回的域名列表为空")
            
        # --- 修改点开始：随机选择一个域名 ---
        # 也可以在这里加判断，比如只选 isActive=True 的域名
        # active_domains = [d for d in domains if d.get('isActive')]
        selected_domain_data = random.choice(domains)
        print(f"已从 {len(domains)} 个可用域名中随机选择: {selected_domain_data['domain']}")
        return selected_domain_data['domain']
        # --- 修改点结束 ---
        
    except (KeyError, IndexError) as e:
        raise Exception(f"解析域名列表失败: {e}")

def create_account(email, password):
    """注册临时账户"""
    payload = {"address": email, "password": password}
    res = requests.post(f"{BASE_URL}/accounts", json=payload, timeout=TIMEOUT, proxies=PROXY)
    if res.status_code == 201:
        return res.json()
    else:
        # 如果域名有问题，可能会注册失败，抛出详细信息
        raise Exception(f"注册失败 ({res.status_code}): {res.text}")

def get_token(email, password):
    """获取访问 Token"""
    payload = {"address": email, "password": password}
    res = requests.post(f"{BASE_URL}/token", json=payload, timeout=TIMEOUT, proxies=PROXY)
    if res.status_code == 200:
        return res.json()['token']
    else:
        raise Exception(f"获取Token失败: {res.text}")

def get_messages(token):
    """获取邮件列表"""
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/messages", headers=headers, timeout=TIMEOUT, proxies=PROXY)
    # 接口偶尔可能返回空或错误，做简单容错
    if res.status_code == 200:
        return res.json().get('hydra:member', [])
    return []

def get_message_detail(token, msg_id):
    """获取邮件详情（含正文）"""
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/messages/{msg_id}", headers=headers, timeout=TIMEOUT, proxies=PROXY)
    return res.json()

# --- 主逻辑 ---
if __name__ == "__main__":
    try:
        # 1. 准备账号信息
        print("正在连接服务器获取域名...")
        domain = get_domain()
        
        # 生成随机用户名和密码
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        password = "Pwd" + ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        email = f"{username}@{domain}"
        
        print(f"------------------------------------------------")
        print(f"正在注册临时邮箱: {email}")
        print(f"密码: {password}")
        print(f"------------------------------------------------")
        
        # 2. 创建账号并获取 Token
        create_account(email, password)
        token = get_token(email, password)
        print("账号注册成功，正在等待邮件（按 Ctrl+C 停止）...")
        
        # 3. 轮询邮件（带容错机制）
        max_retries = 60 # 尝试60次（约5分钟）
        
        for i in range(max_retries):
            try:
                # 尝试获取邮件列表
                msgs = get_messages(token)
                
                if msgs:
                    print(f"\n[成功] 收到 {len(msgs)} 封邮件!")
                    
                    for msg in msgs:
                        print("="*60)
                        print(f"发件人: {msg['from']['address']} ({msg['from']['name']})")
                        print(f"标题:   {msg['subject']}")
                        print(f"时间:   {msg['createdAt']}")
                        print("-" * 60)
                        
                        # 获取详情
                        print("正在下载邮件详情...")
                        try:
                            detail = get_message_detail(token, msg['id'])
                            
                            # --- 内容显示逻辑 ---
                            text_body = detail.get('text')
                            html_body = detail.get('html')
                            intro = detail.get('intro') # 邮件摘要，通常是验证码所在位置

                            if text_body:
                                print("【邮件类型：纯文本】")
                                print(text_body)
                            elif html_body:
                                print("【邮件类型：HTML】(无纯文本版本)")
                                print("\n--- 内容摘要 (Intro) ---")
                                print(intro if intro else "无摘要")
                                
                                # 这里可以加正则提取验证码，例如 re.search(r'\d{6}', html_body)
                            else:
                                print("【异常】未找到任何邮件内容。")
                                
                        except Exception as e:
                            print(f"读取内容失败: {e}")
                        
                        print("="*60)
                    
                    # 收到邮件后退出循环
                    break 
                
                print(f"[{i+1}/{max_retries}] 暂无邮件...", end="\r")
                
            except RequestException as e:
                print(f"\n[{i+1}] 网络连接波动，正在重试...")
            except Exception as e:
                print(f"\n[{i+1}] 发生未知错误: {e}")

            # 等待 5 秒
            time.sleep(5)
            
        else:
            print("\n超时未收到邮件。")
            
    except KeyboardInterrupt:
        print("\n用户手动停止。")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
