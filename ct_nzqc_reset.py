'''
cron: 36 0 * * *
new Env('nzqc重置');
'''

import json,random,os
from utils.ql_api import get_envs, put_envs

env = 'nzqc'
accounts = os.environ[env].split('\n')
filepath = "/ql/data/env/nzqc.json"
with open(filepath, "r") as f:
    data = json.load(f)

if accounts != '空':
    print(f"共需要添加{len(accounts)}个账号")
    for account in accounts:
        info = account.split('----')
        account_dict = {
            "mobile": info[0],
            "refresh_token": info[1],
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
    
for i in data:
    i["sign"] = False
    i['share'] = 0
    i['comment'] = 0
    
random.shuffle(data)  
with open(filepath, "w") as f:
    json.dump(data, f)    
    
print(len(data))
put_envs(get_envs(env)[0].get('id'), env, '空')
