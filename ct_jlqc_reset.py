'''
cron: 16 0 * * *
new Env('jlqc重置');
'''

import json,random,os
from utils.ql_api import get_envs, put_envs

env = 'jlqc'

accounts = os.environ[env].split('\n')


filepath = "/ql/data/env/jlqc.json"
with open(filepath, "r") as f:
    data = json.load(f)

for i in data:
    i["sign"] = False
    i['create'] = False


if len(accounts) > 1:
    print(f"共需要添加{len(accounts)}个账号")
    for account in accounts:
        info = account.split('----')
        for datas in data:
            if info[0] == datas["mobile"]:
                datas["password"] = info[1]
                datas["token"] = info[2]
                datas["token_time"] = info[3]
                break
        else:
            account_dict = {
                "mobile": info[0],
                "password": info[1],
                "token": info[2],
                "token_status": True,
                "token_time": info[3],
                "sign": False,
                "create": False,
                "availablePoint": 0,
                "reserve": None,
                "reserve2": None
            }
            data.append(account_dict)
            
random.shuffle(data)  
with open(filepath, "w") as f:
    json.dump(data, f)    
    
print(len(data))

put_envs(get_envs(env)[0].get('id'), env, '空')
