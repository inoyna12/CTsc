#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import os
import time
import base64
# ======== 配置项（确认SIGN_URL是抓包到的真实接口）========
COOKIE = os.getenv("WJ_KC_COOKIE")
SIGN_URL = "https://wj-kc.com/api/user/sign_use"  # 必须确认正确
REQUEST_METHOD = "POST"  # 抓包的请求方法（GET/POST）
SIGN_DATA = {}  # 抓包的请求参数，无则留空
# ==============================================
if not COOKIE:
    print("❌ 未配置WJ_KC_COOKIE环境变量，请在青龙面板添加")
    exit(1)
# 最终版请求头（适配该网站）
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": COOKIE,
    "Referer": "https://wj-kc.com/",
    "Origin": "https://wj-kc.com/",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
}
def decode_base64(data):
    """Base64解密（处理补位）"""
    try:
        missing_padding = len(data) % 4
        if missing_padding:
            data += "=" * (4 - missing_padding)
        decoded_bytes = base64.b64decode(data)
        return json.loads(decoded_bytes.decode("utf-8"))
    except Exception as e:
        print(f"⚠️ Base64解密失败：{str(e)}")
        return None
def sign_in():
    """最终版签到逻辑（适配所有提示）"""
    try:
        session = requests.Session()
        session.get("https://wj-kc.com", headers=HEADERS, timeout=10)
        # 发送签到请求
        if REQUEST_METHOD.upper() == "POST":
            response = session.post(SIGN_URL, headers=HEADERS, data=SIGN_DATA, timeout=15, allow_redirects=False)
        else:
            response = session.get(SIGN_URL, headers=HEADERS, params=SIGN_DATA, timeout=15, allow_redirects=False)
        # 解析响应
        outer_result = response.json()
        inner_data = decode_base64(outer_result["data"]) if "data" in outer_result else None
        if not inner_data:
            print("❌ 解密失败，原始响应：", response.text)
            return
        # 提取核心字段
        code = inner_data.get("code")
        msg = inner_data.get("msg", "")
        add_traffic = inner_data.get("data", {}).get("addTraffic", 0) / 1024 / 1024  # 转MB
        # 适配所有场景的判断逻辑
        if code == 0 and msg == "SUCCESS":
            print(f"✅ 签到成功！获得流量：{add_traffic:.2f} MB")
        elif msg == "SIGN_USE_MULTY_TIMES" or "MULTY_TIMES" in msg or code == 1028:
            print(f"ℹ️ 今日已签到，无需重复操作（提示：{msg}）")
        elif code in [1, -1, 1000]:
            print(f"❌ 签到失败：{msg}（错误码：{code}）")
        else:
            print(f"ℹ️ 签到结果：{msg}（错误码：{code}）")
    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查网络或网站可用性")
    except json.JSONDecodeError:
        print(f"❌ 响应格式异常：{response.text}")
    except Exception as e:
        print(f"❌ 签到异常：{str(e)}")
if __name__ == "__main__":
    print(f" 开始执行wj-kc.com签到脚本 - {time.strftime('%Y-%m-%d %H:%M:%S')}")
    sign_in()
    print(f" 签到脚本执行完毕 - {time.strftime('%Y-%m-%d %H:%M:%S')}")

