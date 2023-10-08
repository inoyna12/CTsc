'''
cron: 36 9 * * *
new Env('吉利汽车生成账号密码');
'''

import os, sys
from utils.github_api import update_github_file

def ql_env(name):
    if name in os.environ:
        token_list = os.environ[name].split('\n')
        if len(token_list) > 0:
            return token_list
        else:
            print("变量未启用" + name)
            sys.exit(1)
    else:
        print("未添加变量" + name)
        sys.exit(0)
        
        
if __name__ == '__main__':
    title_name = "吉利汽车"    
    env_phone = "JLphone"#变量名
    quantity = ql_env(env_phone)
    new_list = [phone + '----j' + phone for phone in quantity]
    phone_list = '\n'.join(new_list)
    update_github_file(f"token/{title_name}/账号密码.txt", phone_list)
