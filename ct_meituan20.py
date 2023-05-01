'''
cron: 55 13 * * * ct_meituan20.py
new Env('美团奶茶券');
'''

#青龙多账号换行并发:task 5.py conc ceshi 1 2


import time,datetime,requests,os,json
from sendNotify import send
from os import environ

today = datetime.datetime.now().strftime('%Y-%m-%d')
nowtime1 = datetime.datetime.now ().strftime ('%Y-%m-%d %H:%M:%S.%f8')#当前时间
#开始抢兑时间
starttime='13:59:57.00000000'
#结束时间
endtime='14:00:05.00000000'

couponReferId='5865AE2DF47846FC8C2B85078C075051'

qgtime = '{} {}'.format (today, starttime)
qgendtime = '{} {}'.format (today, endtime)

def exchange(cookie):
    try:
        url = f"https://promotion.waimai.meituan.com/lottery/limitcouponcomponent/fetchcoupon?couponReferId={couponReferId}&actualLng=120.58319&actualLat=31.29834&geoType=2&gdPageId=481021&pageId=482299&version=1&utmSource=&utmCampaign=&instanceId=16825614060250.5872321938318412&componentId=16825614060250.5872321938318412"
        json = '{"cType":"mti","fpPlatform":3,"wxOpenId":"","appVersion":"","mtFingerprint":"H5dfp_1.8.2_tttt_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"}'
        headers = {
            'Connection': 'keep-alive',
            'Content-Length': '2444',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://market.waimai.meituan.com',
            'mtgsig': '{"a1":"1.0","a2":1682917519266,"a3":"37047387vv0x5vuxy9yu01x986326x588126369x6xx97958u1228498","a4":"fe1db7c3c4394221c3b71dfe214239c461d8ae2b409a97ef","a5":"xpLqJ+YTi8pBpU+bFkJ5sK8QRXV/Q9NX3co7O57/5OZHk8m8Npso07noiRLFIcNgjLU02yQBVLB0uSW6l9mObu6T9BD=","a6":"h1.20BIYnw6Mr487xIhmYPIa3cOpjkseHWEnC9s0DASEFrtc/8Irtku7EleuufPS8L7LA/PK4GlMGAzi+U4MFuWXvNFsDKrOdfLNAi+v954rtYdKg84vkgP2TovIl1vRVoUlZtBnLlHUuN3n8PsojFULqPgyNiT2UOgZffc0yeL19EuCdxZNKWPkSedhukFv4ATE0xGQNEiwT7lnqOV89HxhXpiXPBryZrGcPT/8ms/takXkgyQ2cuZ31WPrSAN5URHg05ysRdEP9PpevJUkgH8RQg+mo/NG+Ok/L1NlOdYYCXICRIJWtcjNGFtkZN0x4gt7vwiNzg7Z9rTOMeXvMUxHnWzydPVAjs+ExzE4xxhdD13ok8bE2hiZLaBZsgSq9ELo/w2ocLzi5+ipxG+X2tF1rQu7BsSeEuE2XJtgcPfn3Lk=","a7":"","x0":4,"d1":"2f2dd3b5b1da0b9aa3bdcd754d78660d"}',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.153 Mobile Safari/537.36',
            'Content-Type': 'application/json',
            'Referer': 'https://market.waimai.meituan.com/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie': cookie,
            'X-Requested-With': 'mark.via',
        }
        print(f"抢购时间为：{qgtime}")
        print("正在等待兑换时间，请勿终止退出...")
        while True:
            if nowtime1 > qgtime:
                response = requests.post(url=url,headers=headers,json=json)
                result = response.json()
                if result['msg'] == '抢券成功！':
                    msg += f"美团奶茶券：{result['msg']}\n"
                    break
                time.sleep(0.002)
                if nowtime1 > qgendtime:
                    print("超过兑换时间，退出执行")
                    break
    except:
        print("报错")
    return msg

if __name__ == '__main__':
    msg = ""
    cookie = os.environ['meituan20']
    msg += exchange(cookie)
    send('美团奶茶20券', msg)