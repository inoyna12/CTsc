'''
cron: 55 13 * * * ct_meituan20.py
new Env('美团奶茶券');
'''

#青龙多账号换行并发:task 5.py conc ceshi 1 2


import time,datetime,requests,os,json
from sendNotify import send
from os import environ

today = datetime.datetime.now().strftime('%Y-%m-%d')
#开始抢兑时间
starttime='14:05:58.00000000'
#结束时间
endtime='14:06:04.00000000'

couponReferId='4D823738DC09463DAA54156094768F02'

qgtime = '{} {}'.format (today, starttime)
qgendtime = '{} {}'.format (today, endtime)



def exchange(cookie):
    try:
        msg = ""
        url = f"https://promotion.waimai.meituan.com/lottery/limitcouponcomponent/fetchcoupon?couponReferId={couponReferId}&actualLng=120.58319&actualLat=31.29834&geoType=2&gdPageId=481021&pageId=482299&version=1&utmSource=&utmCampaign=&instanceId=16825614060250.5872321938318412&componentId=16825614060250.5872321938318412"
        data = '{"cType":"mti","fpPlatform":3,"wxOpenId":"","appVersion":"","mtFingerprint":"H5dfp_1.8.2_tttt_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"}'
        headers = {
            'Connection': 'keep-alive',
            'Content-Length': '2464',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://market.waimai.meituan.com',
            'mtgsig': '{"a1":"1.0","a2":1682999934302,"a3":"37047387vv0x5vuxy9yu01x986326x588126369x6xx97958u1228498","a4":"293e827758246cce77823e29ce6c2458297fa2f3e71386ab","a5":"WJzT+ccIaeLk4NOpMWKiTwq9GJy4DopfbS4Ral/wzTObQB8tAaT/zMjLxMOWf1XK0gAgJd2VCgbd83sWAwf8tPq3tJI=","a6":"h1.2IKNuDyebwrKwczTgSVAPu4dVUTo4/CRxeOgcV8K6MmadyyTmgJ4FCC5e/yHKJfr5Ye1GCKPTLi7s9EDEY3C5ydlX6ifqgB/PL9yOgCd/8D9H2cKdvooNrL+UvWM2RDDWZ3i/irlS+Yc8qS/htLj0NgkOUDPiFNs85+vI1LCHc1Ht1LhlglDb1EXXl2ViYHeXUfw/sd/o0HKXY500CRX0KoG5WYqoZj4JjrBO0D2rpR5DNvpNmbakvBzv0grVbMDLG5r63kQT7y6pnw3DvF29x2BtQ/c0+vFsatZdooYZTas9T/lfgzRfdpjFhTb6HZRZFi0d/alN/c+6e07sL2IM9Furog5LtSRZ4xOsi8Xg5IR/44vUrP0/+BPvaU/sFTaHuEX6ex8xvWnVHlkCWUX1x0h9VqwD0EFhNW3IKdFRZoGnD+H3VleW0SF8fE23a23b","a7":"","x0":4,"d1":"3bafcd7449e64994ee79a6642576db12"}',
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
            nowtime1 = datetime.datetime.now ().strftime ('%Y-%m-%d %H:%M:%S.%f8')#循环刷新当前系统时间
            if nowtime1 > qgtime:
                response = requests.post(url=url,headers=headers,data=data)
                result = response.json()
                print(result)
                if result['subcode'] == 0:
                    msg += "抢券成功！"
                 #   print(f"当前时间：{nowtime1}")
                    print(msg)
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
