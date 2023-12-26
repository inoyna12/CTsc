'''
cron: 16 0 * * *
new Env('nzqc测试');
'''

import json,random,os
from utils.ql_api import get_envs, put_envs

env = 'TZC_num2'
phone_list = os.environ[env].split('\n')
if phones[0] == '空':
    print("环境变量为空，不需要添加")
    exit()
    

filepath = "/ql/data/env/nzqc.json"
with open(filepath, "r") as f:
    data = json.load(f)
print(len(data))

for info in data:
    info['tzc_num2'] = 0
    if info['mobile'] in phone_list:
        info['tzc_num2'] = 2

with open(filepath, "w") as f:
    json.dump(data, f)
