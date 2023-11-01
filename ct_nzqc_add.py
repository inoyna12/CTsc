'''
cron: 2 0 * * *
new Env('nzqc添加');
'''

import json,random,os
from utils.ql_api import get_envs, put_envs

env = 'nzqc'
inx_add = 0
accounts = os.environ[env].split('\n')

if accounts[0] == '空':
    print("环境变量为空，不需要添加")
    exit()

filepath = "/ql/data/env/nzqc.json"
with open(filepath, "r") as f:
    data = json.load(f)

print(f"初始：{len(data)}个账号")
print(f"共{len(accounts)}个账号需要处理")

for account in accounts:
    mobile,refresh_token = account.split('----')
    account_dict = {
        "mobile": mobile,
        "refresh_token": refresh_token,
        "access_token": None,
        "token_time": None,
        "sign": False,
        "share": 0,
        "comment": 0,
        "creditScore": 0,
        "reserve": None,
        "reserve2": None
    }
    data.append(account_dict)
    inx_add += 1
    print(f"增加次数：{inx_add}，号码：{mobile}")

with open(filepath, "w") as f:
    json.dump(data, f)    
    
print("增加次数：" + str(inx_add))
print(f"共{len(data)}个账号")

put_envs(get_envs(env)[0].get('id'), env, '空')
