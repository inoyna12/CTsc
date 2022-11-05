'''

cron: 6 10 * * * ct_xbk.py
new Env('线报酷签到');

'''
import requests
import os

from sendNotify import send
from os import environ

cookie = os.environ["xbkcookie"]
url = "https://v1.xianbao.fun/zb_users/plugin/mochu_us/cmd.php"
headers = {
    'Host': 'v1.xianbao.fun',
    'content-length': '0',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'user-agent': 'Mozilla/5.0 (Linux; Android 9; Redmi K20 Pro Build/PKQ1.190616.001;) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/105.0.5195.79 Mobile Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'origin': 'https://v1.xianbao.fun',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://v1.xianbao.fun/Ucenter',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': cookie,
}

params = {
    'act': 'qiandao',
}
response = requests.post(url=url, params=params, headers=headers).json()
print(response.text)
# rep = response['giod']
print("当前积分:", rep)
title = "线报酷"
content = "当前积分:" + rep
send(title,content)

# {"code":0,"msg":"\u7b7e\u5230\u6210\u529f<br\/>\u6ce8\u518c\u4f1a\u5458\u968f\u673a\u5956\u52b1<span style='color:red;font-size:20px;margin: 0 5px;'>23<\/span>\u79ef\u5206\uff01<br\/>\u6e29\u99a8\u63d0\u793a\uff1a\u5347\u7ea7VIP\u4f1a\u5458\u4f1a\u83b7\u53d6\u66f4\u591a\u5956\u52b1\uff01","giod":"982"}