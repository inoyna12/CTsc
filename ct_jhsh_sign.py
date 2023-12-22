'''
cron: 30 9 * * *
new Env('建行生活签到');
'''

import json
import requests
import sys
import os
from sendNotify import send

giftType = 1 #  1：外卖券，2：打车券

def sign(session):
    url = 'https://yunbusiness.ccb.com/clp_coupon/txCtrl?txcode=A3341A115'
    headers = {
        'Host': 'yunbusiness.ccb.com',
        'content-type': 'application/json;charset=utf-8',
        'mid': '160',
        'appversion': AppVersion,
        'accept': 'application/json,text/javascript,*/*',
        'cookie': session,
    }
    json_data = {
        'ACT_ID': ACT_ID,
        'REGION_CODE': '320500',
        'chnlType': '1',
        'regionCode': '320500',
    }
    response = requests.post(url=url, headers = headers, json = json_data)
    result = response.json()
    if 'SIGN_REQ' in result['data'] and result['data']['SIGN_REQ'] == 1:
        nodeDay = result['data']['GIFT_BAG'][0]['nodeDay']
        NEST_AWARD_DAY = result['data']['NEST_AWARD_DAY']
        signDay = nodeDay - NEST_AWARD_DAY
        if NEST_AWARD_DAY > nodeDay:
            signDay = nodeDay
        signMsg = f"签到成功，当前已连续签到{signDay}天"
        print(signMsg)
        if result['data']['IS_AWARD'] == 1:
            getGift(result['data']['GIFT_BAG'])
            return
    else:
        signMsg = result['errMsg']
        print(signMsg)
        print(result)
    msg.append(phone + '：' + signMsg)
        
def autoLogin():
    url = 'https://yunbusiness.ccb.com/clp_service/txCtrl?txcode=autoLogin'
    headers = {
      'AppVersion': AppVersion,
      'Content-Type': 'application/json',
      'DeviceId': DeviceId,
      'Accept': 'application/json',
      'MBC-User-Agent': f"MBCLOUDCCB/Android/Android 12/2.13/2.00/{DeviceId}/Decrypt-UTF8/1220*2482/",
      'Cookie': ''
    }
    data = Body
    response = requests.post(url, headers=headers, data=data)
    cookie = requests.utils.dict_from_cookiejar(response.cookies)
    session = f'SESSION={cookie.get("SESSION")}'
    print(session)
    return session

def get_act_id():
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
    global ACT_ID
    ACT_ID = result['data']['GIFT_AD_INFO'][2]['AD_URL'].split('=')[-1]
    print(ACT_ID)

def getGift(data):
    giftMap = { "1": "外卖", "2": "打车" }
    filtered_list = [d for d in data if d['couponScene'] == giftMap[str(giftType)]]
    sorted_list = sorted(filtered_list, key=lambda x: x['couponPrice'], reverse=True)
    url = 'https://yunbusiness.ccb.com/clp_coupon/txCtrl?txcode=A3341C082'
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Accept': 'application/json,text/javascript,*/*',
        'Host': 'yunbusiness.ccb.com',
        'MID': '160'
    }
    for item in sorted_list:
        json_data = {
            'mebId': MEB_ID,
            'actId': ACT_ID,
            'nodeDay': item['nodeDay'],
            'couponType': 0,
            'nodeCouponId': item['couponId'],
            'dccpBscInfSn': '',
            'chnlType': '1',
            'regionCode': '320500',
        }
        response = requests.post(url=url, headers = headers, json = json_data)
        result = response.json()
        if result['errCode'] == '0':
            giftMsg = '获得' + result['data']['title']
            print(giftMsg)
            msg.append(phone + '：' + giftMsg)
            return

def getLatestVersion():
    url = 'https://itunes.apple.com/cn/lookup?id=1472477795'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.get(url=url, headers = headers)
    result = response.json()
    global AppVersion
    AppVersion = result['results'][0]['version']
    print(AppVersion)

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
            print("变量未启用" + name)
            sys.exit(1)
    else:
        print("未添加变量" + name)
        sys.exit(0)
    
def main():
    if 'ACT_ID' not in globals():
        get_act_id()
    if 'AppVersion' not in globals():
        getLatestVersion()
    session = autoLogin()
    sign(session)
             
if __name__ == '__main__':
    title_name = '建行生活签到'
    env_list = ql_env("JHck")
    msg = []
    index = 1
    print(f"共找到{len(env_list)}个账号")
    for env in env_list:
        print(f"\n{'-' * 13}正在执行第{index}个账号{'-' * 13}")
        phone = env.split('#')[0]
        phone = phone[:3] + "****" + phone[7:]
        MEB_ID = env.split('#')[1]
        DeviceId = env.split('#')[2]
        Body = env.split('#')[3]
        main()
        if index < len(env_list):
            index + 1
            random_sleep(10, 20)
    send(title_name, '\n'.join(msg))
