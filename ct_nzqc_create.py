'''
cron: 36 0 * * *
new Env('nzqc创建json');
'''
import os,json
# 假设有两个列表，分别存储了账号和密码
accounts = os.environ['NZphone'].split('\n')
#passwords = os.environ['NZtoken'].split('\n')[:3]
# passwords = os.environ['NZtoken'].split('\n') + os.environ['NZtoken1'].split('\n')

# 初始化空列表
account_list = []

# 遍历账号和密码列表
for i in range(len(accounts)):
    account = accounts[i]
    password = passwords[i]
    
    # 创建包含账号、密码和其他键值对的字典
    account_dict = {
        "mobile": account,
        "refresh_token": password,
        "access_token": None,
        "token_time": None,
        "sign": False,
        "share": 0,
        "comment": 0,
        "creditScore": 0,
        "reserve": None,
        "reserve2": None
    }
    
    # 将每个账号和密码以及其他键值对的字典添加到列表中
    account_list.append(account_dict)
print(len(account_list))
filepath = "/ql/data/env/nzqc.json"
with open(filepath, "w") as f:
    json.dump(account_list, f)
