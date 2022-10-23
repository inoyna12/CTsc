# -*- coding: utf-8 -*-
"""
new Env('联通话费购');
"""



import json
import os
import time
import requests
import random
import utils.hfgCookie

#time.sleep(random.randint(0,3600))
requests.packages.urllib3.disable_warnings()

try:
    from utils.hfgCookie import get_cookies
    from sendNotify import send
except:
    send = None


def env(key):
    return os.environ.get(key)

# cook = env('hfg')

hfgCookieArr = get_cookies()
# https://atp.bol.wo.cn/atpapi/act/lottery/start/v1/actPath/ACT202009101956022770009xRb2UQ/0?jQEeL4DkuBXpw0chttps=KR5.uhpDfh4vrfpNb3CMUl10PmRozyWC7ReMyF3N9_v7lJEtzJWeO2nnOiPz0kehaOqCu.WuVNEEWC3XRFghMnOTJEMtCpy5I05hYrkV9b5bM
url_cj = 'https://atp.bol.wo.cn/atpapi/act/lottery/start/v1/actPath/ACT202009101956022770009xRb2UQ/0'
url_qd = 'https://atp.bol.wo.cn/atpapi/act/actUserSign/everydaySign?actId=1516'


def head(cook) :
    head = { "Host"            : "atp.bol.wo.cn" ,
             "Accept"          : "application/json, text/plain, */*" ,
             "Connection"      : "keep-alive" ,
             "Cookie"          : cook ,
             "User-Agent"      : "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.16(0x18001042) NetType/4G Language/zh_CN" ,
             "Accept-Language" : "zh-CN,zh-Hans;q=0.9" ,
             "Referer"         : "https://atp.bol.wo.cn/atplottery/ACT202012221038331042965g65tNa?product=hfgo" ,
             "Accept-Encoding" : "gzip, deflate, br"
             }
    return head

def qiandao(cook,num):
    result = ""
    resp_qd = requests.get( url = url_qd , headers = head( cook ) )
    resp_qd = json.loads( resp_qd.text )
    result =  resp_qd[ 'message' ] + '\n'
    for i in range(0,10):
        #    time.sleep(random.randint(0,10))
        time.sleep(5)

        resp = requests.get( url = url_cj , headers = head( cook ) )
        resp = json.loads(resp.text)
        print(resp)
        try:
            resu = resp['data']['prizeName']
        except:
            resu = resp[ 'message' ]
        result += resu + '\n'
        if resu == '您的抽奖次数已用完!':
            break
#    sendMessage(str(num) + result)
    print(str(num) + result)
    send('话费购',str(num) + result)


i = 0
while(i < len(hfgCookieArr)):
    hfg_cookie = hfgCookieArr[i]
    qiandao(hfg_cookie,i)
    i += 1