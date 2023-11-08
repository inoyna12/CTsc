'''
cron: 2 0 * * *
new Env('jlqc添加');
'''

import json,random,os
from utils.ql_api import get_envs, put_envs

env = 'jlqc'
accounts = os.environ[env].split('\n')
inx_add = 0
inx_update = 0

if accounts[0] == '空':
    print("环境变量为空，不需要添加")
    exit()

filepath = "/ql/data/env/jlqc.json"
with open(filepath, "r") as f:
    data = json.load(f)

print(f"初始：{len(data)}个账号")
print(f"共{len(accounts)}个账号需要处理")

for item in accounts:
    mobile,password,token,token_time = item.split("----")
    exists = False
    for info in data:
        if info["mobile"] == mobile:
            info["password"] = password
            info["token"] = token
            info["token_time"] = token_time
            exists = True
            inx_update += 1
            print(f"更新次数：{inx_update}，号码：{mobile}")
            break
    if not exists:
        account_dict = {
            "mobile": mobile,
            "password": password,
            "token": token,
            "token_status": True,
            "token_time": token_time,
            "sign": False,
            "availablePoint": 0,
            "signDay": None
        }
        data.append(account_dict)
        inx_add += 1
        print(f"增加次数：{inx_add}，号码：{mobile}")
 
with open(filepath, "w") as f:
    json.dump(data, f)    
print(f"更新次数：{inx_update}，增加次数：{inx_add}")
print(f"共{len(data)}个账号")
put_envs(get_envs(env)[0].get('id'), env, '空')
