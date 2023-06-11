'''
cron: 55 59 15 * * *
new Env('美团152');
'''

import time,datetime,requests,os,json,execjs
#from sendNotify import send
#from os import environ
#from utils.ql_api import get_envs, disable_env, post_envs, put_envs


#开始抢兑时间
starttime='15:59:59.000'
#结束时间
endtime='16:00:02.000'



couponReferId = 'F6CFF2A35BD94F49BDEE0CC6F7CF9FE4'
url = f'https://promotion.waimai.meituan.com/lottery/limitcouponcomponent/fetchcoupon?couponReferId={couponReferId}&actualLng=120.64517&actualLat=31.13914&geoType=2&gdPageId=306477&pageId=306004&version=1&utmSource=&utmCampaign=&instanceId=16620226080900.11717750606071209&componentId=16620226080900.11717750606071209'


def mtgsig():
    js_code = open('utils/mt.js', 'r', encoding='utf-8').read()
    data = {"cType": "mtandroid", "fpPlatform": 4, "wxOpenId": "", "appVersion": "12.9.404"}
    js = execjs.compile(js_code)
    headers = {
        "dj-token": "",
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; 22081212d Build/SKQ1.220303.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.153 Mobile Safari/537.36",
        "Content-Type": "application/json",
        "X-Requested-With": "com.sankuai.meituan",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://market.waimai.meituan.com/",
        "Cookie": meituanck
    }
    req = {
        "url": url,
        "method": "POST",
        "headers": headers,
        'data': data
    }
    now = int(datetime.datetime.now().timestamp() * 1000)
    r = js.call("signReq", req, now)
#    print(r)
    Cookie = r['headers']['Cookie']
    mtgsig = r['headers']['mtgsig']
    data = r['data']
    return Cookie, mtgsig, data

def Sxin(Cookie):
    url = f'https://promotion.waimai.meituan.com/lottery/limitcouponcomponent/info?couponReferIds={couponReferId}'
    headers = {
        "Host":"promotion.waimai.meituan.com",
        "Connection":"keep-alive",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Linux; Android 12; 22081212d Build/SKQ1.220303.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.153 Mobile Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "dnt":"1",
        "X-Requested-With":"mark.via",
        "Sec-Fetch-Site":"none",
        "Sec-Fetch-Mode":"navigate",
        "Sec-Fetch-User":"?1",
        "Sec-Fetch-Dest":"document",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie":Cookie
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    print(result)

def mt30_15():
    Cookie, mtgsig, data = mtgsig()
    headers = {
        'Connection': 'keep-alive',
        'Content-Length': '2764',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://market.waimai.meituan.com',
        'mtgsig': mtgsig,
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22081212d Build/SKQ1.220303.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.153 Mobile Safari/537.36',
        'Content-Type': 'application/json',
        'Referer': 'https://market.waimai.meituan.com/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': Cookie,
        'X-Requested-With': 'mark.via',
    }
    Jin = Sxin(Cookie)
    print(Cookie, data, "\n刷新参数成功")
    print("正在等待领券时间，请勿终止退出...")
    while True:
        now = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
        if now > starttime:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            print(now, result['msg'])
        if now > endtime:
            print(now, "结束循环")
            u_token = get_envs("meituanck")
            put_envs(u_token[0].get('id'), u_token[0].get('name'), Cookie, '美团 ' + now)
            break
        
if __name__ == '__main__':
    meituanck = os.environ['meituanck']
    mt30_15()
