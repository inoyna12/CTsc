'''
cron: 30 9 * * * ct_jhsh.py
new Env('建行生活签到');
'''

import requests
import os
import json
import time
#print(f"==================脚本执行- 北京时间(UTC+8)：{time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}=====================\n")
from sendNotify import send
from os import environ

def qiandao(Phone, MEB_ID, new_Phone):
    try:
        msg = ""
        headers = {
            'Host': 'yunbusiness.ccb.com',
            'content-type': 'application/json;charset=utf-8',
            'mid': '153',
            'accept': 'application/json,text/javascript,*/*',
            'accept-language': 'zh-cn',
            'channel_num': '0',
            'origin': 'file://',
            'user-agent': 'Mobile/15E148/CloudMercWebView/UnionPay/1.0 CCBLoongPay',
        }
        params = {
            'txcode': 'A3341A040',
        }
        d = get_act_id(MEB_ID, '签到')
        ACT_ID = d.get('AD_URL', '').split('=')[1]
        json_data = {
            'ACT_ID': ACT_ID,
            'MEB_ID': MEB_ID,
            'REGION_CODE': '110000',  # 地区id
            'chnlType': '1',
            'regionCode': '110000',  # 地区id
            "USR_TEL": f"{Phone}",
        }
        response = requests.post('https://yunbusiness.ccb.com/clp_coupon/txCtrl', params=params, headers=headers,json=json_data)
        result = response.json()
        print(result) #打印全部
        if len(result['data']) > 0:
            msg += f"{new_Phone}：签到成功！\n"
            if "result['data']['IS_AWARD']" in locals():
                COUP_TITLE = result['data']['COUP_TITLE']#获得奖励
                COUP_SUB_TITLE = result['data']['COUP_SUB_TITLE']#满多少可用
                msg += f"获得：{COUP_TITLE}，{COUP_SUB_TITLE}\n"  
            NEST_AWARD_DAY = result['data']['NEST_AWARD_DAY']#剩余天数
            SIGN_TIPS = result['data']['SIGN_TIPS']#可获得奖励
            msg += f"再签到{NEST_AWARD_DAY}可获得{SIGN_TIPS}\n\n" 
        elif len(result['data']) == 0: 
            msg += f"{new_Phone}：请勿重复签到！\n\n"
    except:
        msg += f"Cookie失效或脚本待更新\n"
    return msg

def get_act_id(MEB_ID, key_word):
    headers = {
        'Host': 'yunbusiness.ccb.com',
        'clientinfo': '',
        'user-agent': '%E5%BB%BA%E8%A1%8C%E7%94%9F%E6%B4%BB/2023031502 CFNetwork/1220.1 Darwin/20.3.0',
        'devicetype': 'iOS',
        'mbc-user-agent': 'MBCLOUDCCB/iPhone/iOS14.4.2/2.12/2.1.2/0/chinamworld/750*1334/2.1.2.001/1.0//iPad13,1/iOS/iOS14.4.2',
        'appversion': '2.1.2.001',
        'ua': 'IPHONE',
        'clientallver': '2.1.2.001',
        'accept-language': 'zh-cn',
        'c-app-id': '03_64easgdajgdjahgdhajsd6',
        'accept': 'application/json',
        'content-type': 'application/json',
    }
    params = {
        'txcode': 'A3341AB03',
    }
    json_data = {
        'IS_CARE': '0',
        'REGION_CODE': '110000',
        'MEB_ID': MEB_ID,
        'CHANNEL_TYPE': '14',
        'LGT': '116.2445327671808',
        'LTT': '40.05567999910404',
        'DEVICE_NO': '',
        'REAL_REGION_CODE': '110000',
        'SECOND_AD_TYPE_LIST': [
            {
                'SECOND_AD_TYPE': '6',
            },
            {
                'SECOND_AD_TYPE': '7',
            },
            {
                'SECOND_AD_TYPE': '10',
            },
            {
                'SECOND_AD_TYPE': '11',
            },
            {
                'SECOND_AD_TYPE': '12',
            },
            {
                'SECOND_AD_TYPE': '24',
            },
            {
                'SECOND_AD_TYPE': '25',
            },
            {
                'SECOND_AD_TYPE': '37',
            },
            {
                'SECOND_AD_TYPE': '38',
            },
            {
                'SECOND_AD_TYPE': '39',
            },
            {
                'SECOND_AD_TYPE': '40',
            },
            {
                'SECOND_AD_TYPE': '41',
            },
            {
                'SECOND_AD_TYPE': '42',
            },
            {
                'SECOND_AD_TYPE': '75',
            },
            {
                'SECOND_AD_TYPE': '93',
            },
            {
                'SECOND_AD_TYPE': '94',
            },
            {
                'SECOND_AD_TYPE': '95',
            },
            {
                'SECOND_AD_TYPE': '96',
            },
        ],
        'FEED_AD_SHOW_STATUS': 0,
        'chnlType': '1',
        'regionCode': '110000',
    }
    response = requests.post('https://yunbusiness.ccb.com/basic_service/txCtrl', params=params, headers=headers,
                             json=json_data)
    data = response.json().get('data', {})
    info = data.get('GIFT_AD_INFO', [])
    for d in info:
        if key_word in str(d):
            return d    

def ql_env():
    if "jhshcookie" in os.environ:
        token_list = os.environ['jhshcookie'].split('\n')
        if len(token_list) > 0:
            return token_list
        else:
            print("jhshcookie变量未启用")
            sys.exit(1)
    else:
        print("未添加jhshcookie变量")
        sys.exit(0)

if __name__ == '__main__':
    msg = ""
    index = 1
    quantity = ql_env()
    print (f"共找到{len(quantity)}个账号")
    for cookie in quantity:
        print (f"------------正在执行第{index}个账号----------------")
        Phone = cookie.split('&')[0]
        MEB_ID = cookie.split('&')[1]
        new_Phone = Phone[:3] + "****" + Phone[7:]
        msg += qiandao(Phone, MEB_ID, new_Phone)
        print(msg)
        time.sleep(10)
        index += 1
    send('建行生活', msg)
