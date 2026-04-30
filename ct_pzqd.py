# -*- coding: utf-8 -*-
"""
IPZAN 多账户自动领取工具 v1.0.0

功能：IPZAN自动登录 + 每周领取IP，支持多账户
环境变量：Pzandaili (支持多账号: acc1#pwd1&acc2#pwd2)
IPZAN注册链接：https://www.ipzan.com?pid=b1sf3o4ao

更新说明:
### 2026.03.01
v1.0.0:
- 🚀 初始化版本，自动登录 + 每周领取IP
- 📢 支持青龙面板推送通知

配置说明:
1. 账号变量 (Pzandaili):
    格式: 账号#密码
    多账号用 @ 或 & 分隔: acc1#pwd1@acc2#pwd2

2. 推送设置 (青龙面板):
    - 自动调用青龙面板自带的 notify.py 文件
    - 脚本运行结束后，将所有账号的运行结果汇总，发送一次统一通知

依赖安装:
- requests

定时规则建议 (Cron):
15 8 * * *

From: YaoHuo8648
Email: zheyizzf@188.com
Update: 2026.03.01
"""

import warnings
import os
import random
import base64
import requests
import time

# -------------------------- 青龙通知模块 --------------------------
# 自动检测是否存在 notify.py，用于发送汇总通知
try:
    from notify import send as ql_send
    print("✅ 已加载青龙通知模块：notify.py")
except ImportError:
    print("⚠️ 未发现 notify.py，仅在控制台输出日志（不影响运行）")
    ql_send = None

# 关闭SSL警告
warnings.filterwarnings("ignore")

# -------------------------- 基础配置 --------------------------
HOME_PAGE = "https://www.ipzan.com?pid=b1sf3o4ao"
LOGIN_API = "https://service.ipzan.com/users-login"  # 登录接口
RECEIVE_API = "https://service.ipzan.com/home/userWallet-receive"  # 每周领取接口
ENV_VAR_NAME = "Pzandaili"  # 环境变量名
FIXED_KEY = "QWERIPZAN1290QWER"  # 加密固定密钥

# 全局请求头
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://ipzan.com",
    "Referer": "https://ipzan.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
}


# -------------------------- 核心工具函数 --------------------------
def encrypt_account(phone: str, password: str) -> str:
    """IPZAN专属加密逻辑（官网JS还原）"""
    plain_text = f"{phone}{FIXED_KEY}{password}"
    encoded_str = base64.b64encode(plain_text.encode("utf-8")).decode("utf-8")
    
    # 生成400位混淆字符串
    random_hex = "".join([hex(int(random.random() * 10**16))[2:] for _ in range(80)])
    random_hex = random_hex.ljust(400, "0")[:400]
    
    # 拼接
    return "".join([
        random_hex[:100], encoded_str[:8],
        random_hex[100:200], encoded_str[8:20],
        random_hex[200:300], encoded_str[20:],
        random_hex[300:400]
    ])

def load_accounts_from_env():
    """加载环境变量中的账户信息"""
    env_value = os.getenv(ENV_VAR_NAME)
    if not env_value:
        raise ValueError(
            f"环境变量 {ENV_VAR_NAME} 未设置！\n"
            f"请按照格式配置：账号#密码 (多账号用 @ 或 & 分隔)"
        )
    
    # 兼容 @ 和 & 分隔符
    if "@" in env_value:
        accounts_str_list = env_value.split("@")
    elif "&" in env_value:
        accounts_str_list = env_value.split("&")
    else:
        accounts_str_list = [env_value]
    
    accounts = []
    for idx, account_str in enumerate(accounts_str_list, 1):
        account_str = account_str.strip()
        if not account_str: continue
        
        parts = account_str.split("#", 1)
        if len(parts) < 2:
            print(f"跳过格式错误账户{idx}：需为 账号#密码")
            continue
            
        acc = parts[0].strip()
        pwd = parts[1].strip()
        
        if acc and pwd:
            accounts.append({
                "index": idx, "account": acc, "password": pwd
            })
            
    if not accounts:
        raise ValueError("未加载到有效账户！请检查环境变量配置。")
    return accounts


def mask_account(account):
    """账号脱敏显示"""
    if len(account) > 7:
        return account[:3] + "****" + account[-4:]
    return account

def process_single_account(session, account_info):
    """
    处理单个账户逻辑
    返回：该账户的执行简报（用于青龙汇总），如果发生致命错误返回None
    """
    account = account_info["account"]
    password = account_info["password"]
    
    summary_msg = ""  # 用于汇总
    
    print(f"\n[{account_info['index']}] 开始处理账号：{mask_account(account)}")
    
    try:
        # 1. 执行登录
        login_headers = HEADERS.copy()
        login_headers["Authorization"] = "Bearer null"
        
        encrypted_account = encrypt_account(account, password)
        login_data = {"account": encrypted_account, "source": "ipzan-home-one"}
        
        login_resp = session.post(
            url=LOGIN_API, headers=login_headers, json=login_data, timeout=15
        )
        login_result = login_resp.json()
        
        if login_result.get("code") != 0:
            err_msg = login_result.get("message", "未知错误")
            print(f"  ❌ 登录失败：{err_msg}")
            
            summary_msg = f"账号：{mask_account(account)}\n状态：❌ 登录失败\n原因：{err_msg}"
            return summary_msg

        token = login_result.get("data", {}).get("token")
        if not token: raise ValueError("登录成功但未返回Token")
        print("  ✅ 登录成功")
        
        # 2. 执行领取
        receive_headers = HEADERS.copy()
        receive_headers["Authorization"] = f"Bearer {token}"
        
        receive_resp = session.get(url=RECEIVE_API, headers=receive_headers, timeout=15)
        receive_result = receive_resp.json()
        
        code = receive_result.get("code")
        msg = receive_result.get("message", "")
        data = receive_result.get("data", "")
        
        if code == 0:
            # 成功
            print(f"  🎉 领取成功：{data}")
            summary_msg = f"账号：{mask_account(account)}\n状态：✅ 领取成功\n结果：{data}"
            
        elif code == -1 and "领取过" in str(msg):
            # 重复领取（不算失败）
            print(f"  ⚠️ 本周已领：{msg}")
            summary_msg = f"账号：{mask_account(account)}\n状态：⚠️ 本周已领\n提示：{msg}"
            
        else:
            # 其他失败
            print(f"  ❌ 领取失败：{msg}")
            summary_msg = f"账号：{mask_account(account)}\n状态：❌ 领取失败\n原因：{msg}"
            
    except Exception as e:
        err_msg = str(e)
        print(f"  ❌ 运行异常：{err_msg}")
        summary_msg = f"账号：{mask_account(account)}\n状态：❌ 运行异常\n原因：{err_msg}"
        
    return summary_msg

# -------------------------- 主程序入口 --------------------------
def main():
    print("="*50)
    print("IPZAN 多账户自动领取工具（每周领IP）")
    print(f"注册链接：{HOME_PAGE}")
    print("="*50)
    
    all_summaries = [] # 存储所有账户的结果，用于青龙汇总
    
    try:
        # 加载账户
        accounts = load_accounts_from_env()
        print(f"共加载 {len(accounts)} 个账户，开始执行任务...\n")
        
        # 循环处理
        for acc in accounts:
            session = requests.Session()
            session.headers.update(HEADERS)
            
            # 处理单个账户
            result = process_single_account(session, acc)
            if result:
                all_summaries.append(result)
            
            # 多账户防并发延迟
            if len(accounts) > 1:
                sleep_time = random.uniform(2, 5)
                time.sleep(sleep_time)
                
    except Exception as e:
        print(f"\n❌ 程序全局错误：{e}")
        all_summaries.append(f"❌ 全局错误导致中断：{e}")
        
    finally:
        print("\n" + "="*50)
        # 触发青龙统一推送（仅当有结果且模块可用时）
        if ql_send and all_summaries:
            print("正在发送青龙面板汇总推送...")
            content = "\n\n".join(all_summaries)
            content += f"\n\n执行时间：{time.strftime('%Y-%m-%d %H:%M:%S')}"
            try:
                ql_send("IPZAN每周领取汇总", content)
                print("✅ 汇总推送发送成功")
            except Exception as e:
                print(f"❌ 汇总推送发送失败：{e}")
        
        print("📝 脚本执行完成")
        print("="*50)

if __name__ == "__main__":
    main()
