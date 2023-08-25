'''
cron: 6 13 * * *
new Env('哪吒token提取');
'''
import os

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
        
if __name__ == '__main__':
    quantity1 = ql_env("NZmy_phone")
    quantity2 = ql_env("NZphone")
    quantity3 = ql_env("NZtoken")
    print(len(quantity1))
    print(len(quantity2), len(quantity3))
    if len(quantity2) != len(quantity3):
        print("变量列表数量不相等")
        exit() # 停止运行
    credentials = dict(zip(quantity2, quantity3))
    for phone in quantity1:
        if phone in credentials:
            print(phone)
            print(credentials[phone])
        else:
            print(phone, "未找到此号码")
        print("\n" + "-------------------------------------------" + "\n")
