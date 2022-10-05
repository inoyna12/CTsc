# -*- coding: utf-8 -*-
"""
new Env('中国联通签到');
"""

import requests

url = "https://act.10010.com/SigninApp/signin/daySign"

headers = {
    'Host': 'act.10010.com',
    'content-length': '0',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Linux; Android 9; Redmi K20 Pro Build/PKQ1.190223.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.136 Mobile Safari/537.36; unicom{version:android@9.0400,desmobile:13291164580};devicetype{deviceBrand:Xiaomi,deviceModel:Redmi K20 Pro};{yw_code:}',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://img.client.10010.com',
    'x-requested-with': 'com.sinovatech.unicom.ui',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://img.client.10010.com/',
    # 'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'SigninApp=a3a410cb7831bf07a496534f608a064b;MUT_S=android9;devicedId=fa40f255c8144dbebae91465708a5526;c_version=android@9.0400;PvSessionId=20221003225343d37b3dbd559143eaaad3e683b9f79d57;login_type=06;u_account=13291164580;city=034|450|90361378|-99;d_deviceCode=e959bb3b39554988846ef735a6accbf1;cw_mutual=6ff66a046d4cb9a67af6f2af5f74c321ccd685a4ae3142f31cb1ad4d7bade2f8da9fa97e11fd3e8d5ce8ba426d2cfcc343a250360be773345721349195099e5c;c_mobile=13291164580;wo_family=0;u_areaCode=;clientid=98|0;unicomMallUid=13291164580;random_login=0;a_token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjU0MTM3MDcsInRva2VuIjp7ImxvZ2luVXNlciI6IjEzMjkxMTY0NTgwIiwicmFuZG9tU3RyIjoieWhhZWY1YzExNjY0ODA4OTA3In0sImlhdCI6MTY2NDgwODkwN30.irBFxcMr6SMrwcfX4oc0ozzcDSlMkLHhlNitpFmuCwxuv_8M8rAb_veLy6wAGnfZBzXhoOrres0Qu4CAMMi2Sw;c_id=ec419c401c2a1b94a6842c281f003f40735ee8568b7dd8c8031ace87b12e754d;enc_acc=a327KoPFxQxUeV2D7DSs1r3baK1m5mjyyeRh+r43D/ESMnFUNSp1s0ck0PjrFUytvU4Ll1SANzYRIW1ySgCGDBJP4MH4Z6lgQPqAoXF2kVvIMH99QiiARsCSPAJDMyRE/uw00Qvb4p93W3xxnbGHbwqUckUR6bCmxu/mshJnmuw=;ecs_acc=a327KoPFxQxUeV2D7DSs1r3baK1m5mjyyeRh+r43D/ESMnFUNSp1s0ck0PjrFUytvU4Ll1SANzYRIW1ySgCGDBJP4MH4Z6lgQPqAoXF2kVvIMH99QiiARsCSPAJDMyRE/uw00Qvb4p93W3xxnbGHbwqUckUR6bCmxu/mshJnmuw=;t3_token=88b59fe968cdcd38bd0086b79f34f4d1;invalid_at=548cef35054de0ddc5efa0203a136ed9192ae30f4e8fd5707f4ff3de500f5be1;third_token=eyJkYXRhIjoiMTMyYzJlNGFmOTFiOWU0ZTRmMmMyMDQwOWVkNWU5NDJjMjEyOGMyZTlmZmZlMWQ1MDM4YWE4M2I4ZGY1ODcwMzQwNzQyMGM2MGUzYmJlYTMwYWMxOWQwNmZiM2JlZWUzNzM2ZTYxODY3MGM3NTdjYjZlMTJmNWRjNjdiMmZkMmQxMDYxZGEzYjZhYjkyOWMxYjEzMzY1NjliYTUxMDMwNSIsInZlcnNpb24iOiIwMCJ9;ecs_token=eyJkYXRhIjoiNWY5YjYzZTkzODFhZjc3MjVjODUxNTY2NDQ5ZDZiMmNiYmYyMjY2YWMzN2MzZTJmODYxZjJlMGY3NWRmZmVhMmMxYzcxYjI4Nzg0NzYwNDYxODZlNWZjNjE0MTUxODNkNDkzNGFkZWJhODljYzkyNjhhYjI0OGNmYzM2NzNjOGNhMDJkY2I5MThjNThmOGQxNzFkZjIxOWQxZjRjMzdhMTNlNDM3YzI3MjA3ZmUxNjBlNmE0YmQ0YjgwYzc1ODRiNzVjMGQxYzVlY2JmNWQ5ZTY0YTExZDljZjg4N2M1MTMzMzdhZDBhYjY0NTg4ODk5ZWU1ZDg4NmMyNmEyOGQ1ZGNmMDcxY2ZiNTQ4ODY3YzVlMGE4YzJhZjgxMDliZDQ3IiwidmVyc2lvbiI6IjAwIn0=;jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtb2JpbGUiOiIxMzI5MTE2NDU4MCIsInBybyI6IjAzNCIsImNpdHkiOiI0NTAiLCJpZCI6IjdjOTE4ODZhNjNkNjFlZDg4Yjg2YWIzMTU4MzQzMWE4In0.iDODqk0ctDTYtMefcTbuc7g1nf3V3-TPmdfdcp6lwG0;acw_tc=0884320d16648089171944466ef9fa48cad9568680651e6fbc67478415;req_mobile=13291164580;req_serial=;req_wheel=ssss',
}

response = requests.post(url=url, headers=headers)
print(response.text)