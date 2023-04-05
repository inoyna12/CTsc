'''

cron: 6 14 * * * ct_haluo.py
new Env('线报酷签到');

'''

import requests
import os
import json
from sendNotify import send
from os import environ
cookie = os.environ["xbkcookie"]
url = "http://new.xianbao.fun/zb_users/plugin/mochu_us/cmd.php?act=qiandao"

headers = {
    'Host': 'new.xianbao.fun',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36',
    'Origin': 'http://new.xianbao.fun',
    'Referer': 'http://new.xianbao.fun/Ucenter',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie':cookie
}

def main():
    response = requests.post(url=url, headers = headers)
    result = response.json()
#    print(result)
    if result['code'] == 0:
        giod = result['giod']
        rez = f"签到成功，当前积分: {giod}"
        print(rez)
        send("线报酷",rez)
    elif result['code'] == 1:
        print(result['msg'])
        send("线报酷",result['msg'])
    else:
        print("结束")  

if __name__ == '__main__':
    main()
