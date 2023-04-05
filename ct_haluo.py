'''

cron: 6 14 * * * ct_haluo.py
new Env('哈啰签到');

'''
import requests
import os

from sendNotify import send
from os import environ
token = os.environ["haluotoken"]
url = "https://api.hellobike.com/api?common.welfare.signAndRecommend"
url1 = "https://api.hellobike.com/api?user.taurus.pointInfo"
headers = {
    'Host': 'api.hellobike.com',
    'origin': 'https://m.hellobike.com',
    'user-agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36; app=easybike; version=6.36.0',
    'referer': 'https://m.hellobike.com/AppPlatformH5/latest/pr_index_bounty.html',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}

data = f'{{"from":"h5","systemCode":62,"platform":4,"version":"6.36.0","action":"common.welfare.signAndRecommend","token":"{token}"}}'

headers1 = {
    'Host': 'api.hellobike.com',
    'user-agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36; app=easybike; version=6.36.0',
    'origin': 'https://m.hellobike.com',
    'referer': 'https://m.hellobike.com/',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}

data1 = f'{{"from":"h5","systemCode":62,"platform":4,"version":"6.36.0","action":"user.taurus.pointInfo","token":"{token}","pointType":1}}'

def main():
    response = requests.post(url=url, headers = headers, data = data)
    result = response.json()
#调试    print(type(result), result)
    if result['code'] == 0:
        bountyCountToday = result['data']['bountyCountToday']
        rez = f"签到成功，获得{bountyCountToday}奖励金"
        print(rez)
        response1 = requests.post(url=url1, headers = headers1, data = data1)
        result1 = response1.json()
#调试        print(type(result1), result1)
        points = result1['data']['points']
        expiring = result1['data']['expiring']
        rez1 = f"当前奖励金:{points}, 月底将过期{expiring}"
        print(rez1)  
        send("哈啰",rez + '\n' + rez1)
    elif result['code'] == 103:
        print("token失效")
        send("哈啰",result['msg'])
    else:
        print("结束")

if __name__ == '__main__':
    main()
