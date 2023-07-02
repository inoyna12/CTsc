'''
cron: 30 9 * * * ct_jhsh.py
new Env('建行生活签到');
'''

import requests
import os
import json
import time
from sendNotify import send
from os import environ

def sign():
    msgs = ''
    url = 'https://yunbusiness.ccb.com/clp_coupon/txCtrl?txcode=A3341A040'
    headers = {
        'Host': 'yunbusiness.ccb.com',
        'channel_num': '1',
        'mid': '160',
        'content-type': 'application/json;charset=UTF-8',
        'accept': 'application/json,text/javascript,*/*',
        'user-agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36/CloudMercWebView',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    json = {
        'ACT_ID': '20230628070000000001',
        'MEB_ID': MEB_ID,
        'USR_TEL': Phone,
        'REGION_CODE': '320500',
        'chnlType': '1',
        'regionCode': '320500',
    } 
    response = requests.post(url=url, headers = headers, json = json)
    result = response.json()
    print(result)
    if result['errMsg'] == None:
        msgs += f"{Phones}：签到成功！\n"
        if result['data']['IS_AWARD'] == 1:
            COUP_TITLE = result['data']['COUP_TITLE']#获得奖励
            COUP_SUB_TITLE = result['data']['COUP_SUB_TITLE']#满多少可用
            msgs += f"获得：{COUP_TITLE}，{COUP_SUB_TITLE}\n"  
        NEST_AWARD_DAY = result['data']['NEST_AWARD_DAY']#剩余天数
        SIGN_TIPS = result['data']['SIGN_TIPS']#可获得奖励
        msgs += f"再签到{NEST_AWARD_DAY}天获得{SIGN_TIPS}\n\n" 
    else:
        msgs += f"{Phones}：{result['errMsg']}\n\n"
    return msgs

def get_act_id(MEB_ID):
    url = 'https://yunbusiness.ccb.com/basic_service/txCtrl?txcode=A3341AB03'
    headers = {
    'Host': 'yunbusiness.ccb.com',
    'cache-control': 'no-cache',
    'accept': 'application/json,text/javascript,*/*',
    'content-type': 'application/json;charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36/CloudMercWebView',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    json_data = '{"IS_CARE":"0","REGION_CODE":"320500","MEB_ID":"MEB_ID_A","CHANNEL_TYPE":"14","LGT":"120.673529","LTT":"31.139346","DEVICE_NO":"","REAL_REGION_CODE":"320500","SECOND_AD_TYPE_LIST":[{"SECOND_AD_TYPE":"6"},{"SECOND_AD_TYPE":"7"},{"SECOND_AD_TYPE":"10"},{"SECOND_AD_TYPE":"11"},{"SECOND_AD_TYPE":"12"},{"SECOND_AD_TYPE":"24"},{"SECOND_AD_TYPE":"25"},{"SECOND_AD_TYPE":"37"},{"SECOND_AD_TYPE":"38"},{"SECOND_AD_TYPE":"39"},{"SECOND_AD_TYPE":"40"},{"SECOND_AD_TYPE":"41"},{"SECOND_AD_TYPE":"42"},{"SECOND_AD_TYPE":"75"},{"SECOND_AD_TYPE":"93"},{"SECOND_AD_TYPE":"94"},{"SECOND_AD_TYPE":"95"},{"SECOND_AD_TYPE":"96"}],"FEED_AD_SHOW_STATUS":0,"chnlType":"1","regionCode":"320500"}'
    data = json_data.replace('MEB_ID_A', MEB_ID)
    response = requests.post(url=url, headers = headers, data = data)
    result = response.json()
    #print(result)
    id = result['data']['GIFT_AD_INFO'][2]['AD_URL'].split('=')[-1]
    print(id)
    return id

def random_sleep(min_val, max_val):
    num = random.randint(min_val, max_val)
    print(f"等待{num}秒后继续>>>>>>>>>>>")
    time.sleep(num)

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
    env_name = "jhshID"#变量名
    title_name = '建行生活'
    msg = ""
    index = 0
    quantity = ql_env(env_name)
    print (f"共找到{len(quantity)}个账号")
    for cookie in quantity:
        print (f"------------正在执行第{index + 1}个账号----------------")
        Phone = cookie.split('#')[0]
        MEB_ID = cookie.split('#')[1]
        Phones = Phone[:3] + "****" + Phone[7:]
        msg += sign()
        print(f"第{index + 1}个账号运行完成\n")
        index += 1
        if index < len(quantity):
            random_sleep(10, 20)
    send(title_name, msg)
