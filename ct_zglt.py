# -*- coding: utf-8 -*-
"""
new Env('中国联通签到');
"""

import requests

url = "https://act.10010.com/SigninApp/signin/daySign"

import requests

headers = {
    'Host': 'act.10010.com',
    'content-length': '0',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'application/json, text/plain, */*',
    'origin': 'https://img.client.10010.com',
    'sec-fetch-dest': 'empty',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; Redmi K20 Pro Build/QKQ1.190825.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.99 Mobile Safari/537.36; unicom{version:android@9.0400,desmobile:13291164580};devicetype{deviceBrand:Xiaomi,deviceModel:Redmi K20 Pro};{yw_code:}',
    'content-type': 'application/x-www-form-urlencoded',
    'x-requested-with': 'com.sinovatech.unicom.ui',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'referer': 'https://img.client.10010.com/SigininApp/index.html?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJleHAiOjE2NjYzNzkxMjgsInRva2VuIjp7ImxvZ2luVXNlciI6IjEzMjkxMTY0NTgwIiwicmFuZG9tU3RyIjoieWh3bks4NWcxNjY1Nzc0MzI4OTI4In0sImlhdCI6MTY2NTc3NDMyOH0.2b5i8II2wnQdi1qdgZYHenRqCMh95QJMPAWxpCghMbJt_vGsk58kWLIu2ckWg2zsBmLFSxh773wLB7vdH_AdiA&signFlag=eyJkYXRhIjoiMTMyYzJlNGFmOTFiOWU0ZTRmMmMyMDQwOWVkNWU5NDJlMTUxYmNkY2UwMWM3YTA0ZTQyMGI3YzQxMjVlMmVjZmQ5NjFjZjUxNGJhMWM3ZDIyYTE3ODMwNDcwMWEwMDczNzg0M2YwZTljOTBmNjkxZTNiMGJmMWYzODVlNjhkNDk1ZjkxZjk4NWFkMzk2NGE2YThmY2YxZWQ0OWJjNzQ5NSIsInZlcnNpb24iOiIwMCJ9',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'SigninApp=fed2e607e1c5f18c2de6996ce452e269;MUT_S=android10;devicedId=a414a29e36e6470ca46539880ebb5f6d;c_version=android@9.0400;login_type=01;u_account=13291164580;city=034|450|90361378|-99;d_deviceCode=e98a3a3580944a2086ad539fa2d743bd;random_login=0;cw_mutual=6ff66a046d4cb9a67af6f2af5f74c321ccd685a4ae3142f31cb1ad4d7bade2f8da9fa97e11fd3e8d5ce8ba426d2cfcc343a250360be773345721349195099e5c;c_mobile=13291164580;wo_family=0;u_areaCode=;clientid=98|0;PvSessionId=202210150304578a041122f3ec433ebfd90c8ef87eba57;SHAREJSESSIONID=10DFB4B109E7CE6297CDED2A31920299;a_token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjYzNzkxMjIsInRva2VuIjp7ImxvZ2luVXNlciI6IjEzMjkxMTY0NTgwIiwicmFuZG9tU3RyIjoieWhhZWY1YzExNjY1Nzc0MzIyIn0sImlhdCI6MTY2NTc3NDMyMn0.QoiiUX5MMAm4chUeSlAyyg0eVW7wS-lUXYTw0IaxxcpguD3dqErlnCdz8bKbWOFq_GOk_-K2JL3ot0ifhMMDbQ;c_id=ec419c401c2a1b94a6842c281f003f4010ec2f04b3b1dba8764fa0cb3e575e15;enc_acc=UtIYZiFYcpgWOZGX+lfQEyITw1l3saM/ky3J+cxjCqJHhOMQd37qfRZdmAdqInbz+1cLMlxCOSIhIZmnwJpbrfTsLr1WBiZhKQMPGAfp93EmDbRBGc1HScc2Q2pdVZb6tb/rW9rCiR9CSL8ZGIbLelj/r6MMLLyDKb21xXYZIgo=;ecs_acc=UtIYZiFYcpgWOZGX+lfQEyITw1l3saM/ky3J+cxjCqJHhOMQd37qfRZdmAdqInbz+1cLMlxCOSIhIZmnwJpbrfTsLr1WBiZhKQMPGAfp93EmDbRBGc1HScc2Q2pdVZb6tb/rW9rCiR9CSL8ZGIbLelj/r6MMLLyDKb21xXYZIgo=;t3_token=26c7d1fb2ce665ed22de70c0c17e81db;invalid_at=bbdc8fe17c44bc5c191d45ef1a0d72538a3165d7dcb15072e3110b9721653afb;third_token=eyJkYXRhIjoiMTMyYzJlNGFmOTFiOWU0ZTRmMmMyMDQwOWVkNWU5NDJlMTUxYmNkY2UwMWM3YTA0ZTQyMGI3YzQxMjVlMmVjZmQ5NjFjZjUxNGJhMWM3ZDIyYTE3ODMwNDcwMWEwMDczNzg0M2YwZTljOTBmNjkxZTNiMGJmMWYzODVlNjhkNDk1ZjkxZjk4NWFkMzk2NGE2YThmY2YxZWQ0OWJjNzQ5NSIsInZlcnNpb24iOiIwMCJ9;ecs_token=eyJkYXRhIjoiNWY5YjYzZTkzODFhZjc3MjVjODUxNTY2NDQ5ZDZiMmNhYmZmN2Y3MDJjODFmYzA2MDAyNjcxYzcxYzBlNTBhMjc5OWFmN2NkMjdiMTI1NGE3MDI4MGRjNWJmNzllM2VlN2E3YzRhMTJhYzNiNDhhNTdhNmFhMWI2MjUzZmQwMDlmZDZjNTIxMTI4NjBkNGNkMzgyYzI5ODVlZGNiOGM4NGFjNjA2Nzk5YTAxNmVmNmJjNTk1OWVhMDRjYTlkMGNkNmFlNTA1ZGIzNzE1NGE0OGJlY2Q1ZWEyOTdkMjAwMTA2Njg0Y2JlNjBkNGNmMWI2OTFmNjFkYjZjMWEwNjQ0ZDllM2IzOTY5ODk0MjVmMmJhYmQ2NjllYjZiMTBjZTczIiwidmVyc2lvbiI6IjAwIn0=;jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtb2JpbGUiOiIxMzI5MTE2NDU4MCIsInBybyI6IjAzNCIsImNpdHkiOiI0NTAiLCJpZCI6IjRlN2UyMGYwMjNjMjgxZmRiNjNlMDZjMDRlZDAyYjdiIn0.hAHFmsQWASJgFcGQvt2kIlYrbpyUjI0BX6SuK9NU5wM;acw_tc=0884324216657743292288962e6e693b7fa96b27948ec21c4a9d7f846e;req_mobile=13291164580;req_serial=;req_wheel=ssss;unicomMallUid=13291164580',
}

response = requests.post(url=url, headers=headers)
print(response.text)