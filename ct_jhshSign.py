'''
cron: 30 9 * * *
new Env('建行生活签到');

变量格式：手机号#MEB_ID#deviceId#Body
Body在https://yunbusiness.ccb.com/clp_service/txCtrl?txcode=autoLogin请求体body
'''

import json
import requests
import os
from utils.utils import send_request
from notify import send

title_name = '建行生活'
user_cookie = os.getenv("JHck").split('\n')

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
    json_data = {
        "IS_CARE": "0",
        "REGION_CODE": "320500",
        "MEB_ID": "YSM202107150798628",
        "CHANNEL_TYPE": "14",
        "LGT": "120.673529",
        "LTT": "31.139346",
        "DEVICE_NO": "",
        "REAL_REGION_CODE": "320500",
        "SECOND_AD_TYPE_LIST": [
            {
                "SECOND_AD_TYPE": "6"
            },
            {
                "SECOND_AD_TYPE": "7"
            },
            {
                "SECOND_AD_TYPE": "10"
            },
            {
                "SECOND_AD_TYPE": "11"
            },
            {
                "SECOND_AD_TYPE": "12"
            },
            {
                "SECOND_AD_TYPE": "24"
            },
            {
                "SECOND_AD_TYPE": "25"
            },
            {
                "SECOND_AD_TYPE": "37"
            },
            {
                "SECOND_AD_TYPE": "38"
            },
            {
                "SECOND_AD_TYPE": "39"
            },
            {
                "SECOND_AD_TYPE": "40"
            },
            {
                "SECOND_AD_TYPE": "41"
            },
            {
                "SECOND_AD_TYPE": "42"
            },
            {
                "SECOND_AD_TYPE": "75"
            },
            {
                "SECOND_AD_TYPE": "93"
            },
            {
                "SECOND_AD_TYPE": "94"
            },
            {
                "SECOND_AD_TYPE": "95"
            },
            {
                "SECOND_AD_TYPE": "96"
            }
        ],
        "FEED_AD_SHOW_STATUS": 0,
        "chnlType": "1",
        "regionCode": "320500"
    }
    result = send_request(url, 'POST', headers=headers, json=json_data)
    act_id = result['data']['GIFT_AD_INFO'][2]['AD_URL'].split('=')[-1]
    print(act_id)
    return act_id

def get_version():
    url = 'https://itunes.apple.com/cn/lookup?id=1472477795'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    result = send_request(url, 'GET', headers=headers)
    version = result['results'][0]['version']
    print(version)
    return version
   
class Jhsh:
    def __init__(self, cookies):
        cookie = cookies.split("#")
        self.phone, self.meb_id, self.deviceId, self.body = cookie
        self.phone = self.phone[:3] + "****" + self.phone[7:]
        self.session = None

    def auto_login(self):
        url = 'https://yunbusiness.ccb.com/clp_service/txCtrl?txcode=autoLogin'
        headers = {
          'AppVersion': version,
          'Content-Type': 'application/json',
          'DeviceId': self.deviceId,
          'Accept': 'application/json',
          'MBC-User-Agent': f"MBCLOUDCCB/Android/Android 12/2.13/2.00/{self.deviceId}/Decrypt-UTF8/1220*2482/",
          'Cookie': ''
        }
        json_data = self.body
        response = requests.post(url, headers=headers, data=json_data)
        cookies = requests.utils.dict_from_cookiejar(response.cookies)
        if cookies:
            self.session = f'SESSION={cookies.get("SESSION")}'
            return True
        print("session刷新失败")
        msg.append(f"{self.phone}：session刷新失败")
        return False

    def sign(self):
        url = 'https://yunbusiness.ccb.com/clp_coupon/txCtrl?txcode=A3341A115'
        headers = {
            'Host': 'yunbusiness.ccb.com',
            'content-type': 'application/json;charset=utf-8',
            'mid': '160',
            'appversion': version,
            'accept': 'application/json,text/javascript,*/*',
            'cookie': self.session,
        }
        json_data = {
            'ACT_ID': act_id,
            'REGION_CODE': '320500',
            'chnlType': '1',
            'regionCode': '320500',
        }
        result = send_request(url, 'POST', headers=headers, json=json_data)
        print(result)
        if result['errCode'] == '0':
            nodeDay = result['data']['GIFT_BAG'][0]['nodeDay']
            NEST_AWARD_DAY = result['data']['NEST_AWARD_DAY']
            signDay = nodeDay - NEST_AWARD_DAY
            if NEST_AWARD_DAY > nodeDay:
                signDay = nodeDay
            signMsg = f"签到成功，当前已连续签到{signDay}天"
            print(signMsg)
            if result['data']['IS_AWARD'] == 1:
                if signDay == 3:
                    couponId = result['data']['GIFT_BAG'][2]['couponId']
                elif signDay == 7:
                    couponId = result['data']['GIFT_BAG'][0]['couponId']
                self.getGift(signDay,couponId)
                return
        else:
            print(result)
            signMsg = result['errMsg']
        msg.append(f"{self.phone}：{signMsg}")

    def getGift(self,nodeDay,couponId):
        url = 'https://yunbusiness.ccb.com/clp_coupon/txCtrl?txcode=A3341C082'
        headers = {
            'Content-Type': 'application/json;charset=utf-8',
            'Accept': 'application/json,text/javascript,*/*',
            'Host': 'yunbusiness.ccb.com',
            'MID': '160'
        }
        json_data = {
            'mebId': self.meb_id,
            'actId': act_id,
            'nodeDay': nodeDay,
            'couponType': 0,
            'nodeCouponId': couponId,
            'dccpBscInfSn': '',
            'chnlType': '1',
            'regionCode': '320500',
        }
        result = send_request(url, 'POST', headers=headers, json=json_data)
        print(result)
        if result['errCode'] == '0':
            giftMsg = '获得' + result['data']['title']
            print(giftMsg)
            msg.append(f"{self.phone}：{giftMsg}")
    
    def main(self):
        if self.auto_login():
            self.sign()
       
if __name__ == '__main__':
    msg = []
    act_id = get_act_id()
    version = get_version()
    print(f"\n共找到{len(user_cookie)}个账号")
    for index, cookies in enumerate(user_cookie, start = 1):
        print(f"\n{'-' * 13}正在执行第{index}/{len(user_cookie)}个账号{'-' * 13}")
        Jhsh(cookies).main()
    send(title_name, '\n'.join(msg))
