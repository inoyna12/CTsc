'''
cron: 6 13 * * *
new Env('哪吒token提取');
'''
import json,os,sys

def ql_env(name):
    if name in os.environ:
        token_list = os.environ[name].split('\n')
        if len(token_list) > 0:
            return token_list
        else:
            print("变量未启用")
            sys.exit(1)
    else:
        print("未添加变量")
        sys.exit(0)
        
phone_list = ql_env("nzphone")
print(f"共找到{len(phone_list)}个账号\n\n")
filepath = "/ql/data/env/nzqc.json"

with open(filepath, "r") as f:
    info_new = json.load(f)

for phone in phone_list:
    for info in info_new:
        if info['mobile'] == phone:
            print(phone + '\n')
            print(info['refresh_token'])
            print("\n" + "-------------------------------------------" + "\n")
            token = phone + '----' + info['refresh_token']
            break
