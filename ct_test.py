from notify import send

success_num = 0 #签到成功数量
fail_num = 0 #签到失败数量
repeat_num = 0 #重复签到
availablePoint8 = 0
availablePoint16 = 0
availablePoint88 = 0
token_unchecked = 0
all_data = [0,1]

if __name__ == '__main__':
    msg = f'''
        账号总数：{len(all_data)}
        成功签到：{success_num}
        失败签到：{fail_num}
        重复签到：{repeat_num}
        token失效：{token_unchecked}
        8吉分：{availablePoint8}
        16吉分：{availablePoint16}
        88吉分：{availablePoint88}
        '''
    print(msg,len(msg))
    send('吉利汽车签到', msg)
