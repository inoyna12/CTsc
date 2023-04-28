import requests
"""
微信关注 小白技术社 获取更新脚本 
建行生活信用卡办卡链接：https://ssz.ccb.com/hccbtl/m120/2932-17059454.html?dcCpAvyId=YHHD2023030860961#/
"""
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


def sign_day(mem_id, phone):
    """
    签到
    :return:
    """
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
    d = get_act_id(mem_id, '签到')
    ACT_ID = d.get('AD_URL', '').split('=')[1]
    json_data = {
        'ACT_ID': ACT_ID,
        'MEB_ID': mem_id,
        'REGION_CODE': '110000',  # 地区id
        'chnlType': '1',
        'regionCode': '110000',  # 地区id
        "USR_TEL": f"{phone}",
    }

    response = requests.post('https://yunbusiness.ccb.com/clp_coupon/txCtrl', params=params, headers=headers,
                             json=json_data)
    print(response.text)
    return response.text


def get_act_id(mem_id, key_word):
    params = {
        'txcode': 'A3341AB03',
    }

    json_data = {
        'IS_CARE': '0',
        'REGION_CODE': '110000',
        'MEB_ID': mem_id,
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


def tongzhi(ss):
    appToken = "ss"
    url = 'http://wxpusher.zjiecode.com/api/send/message/?appToken={appToken}&content={}&uid=UID_7Cq5WK3Qv30EhVbQyXLq77cMJ'.format(
        appToken, ss)
    r = requests.get(url)
    print(r.text)


mem_id = 'YSM202107150798628'
phone = '15050425338'
res = sign_day(mem_id, phone)
tongzhi(str(res))
