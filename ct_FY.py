'''
cron: 26 9 * * *
new Env('福域');
'''

import requests
import os
import json
import time
#print(f"==================脚本执行- 北京时间(UTC+8)：{time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}=====================\n")
from sendNotify import send
from os import environ

def jihuo(cookie):
    msg = ""
    url = 'https://evosapi.changanford.cn/con/recommend/list'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': 'D8760241979CB9493573C04BB2D2441E',
        'body': '8E28A89F8ACD6349CA3F9C63E0DC59DB',
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': 'IKcwDfeLpBKkbG1aSOyzpu3ri62/3lD7phdTiByAH8Lwu6+HrjQ6mE1m4Tu+VK4byat+JhqPJJrXaDqeFpK/kLJextzezlrcYtftQX+kTIq4txX4780ARcCefUxsWXS3hPRDtwbP5tAG8n0tDrOWfjeXVGpU6OCT6MetpsJIFMw=',
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': '1683465989209',
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'User-Agent': 'ford-evos',
    }
    data = '{"paramEncr":"9V8SFXMO9IIxyIVJc4SOitFdPjJ+46sg/50wFTCVkqk="}'
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
    print(result)

def choujiang(cookie):
    msg = ""
    url = 'https://evosapi.changanford.cn/luckyBlessingBag/luckDraw/3'
    headers = {
        'Host': 'evosapi.changanford.cn',
        'Connection': 'keep-alive',
        'seccode': 'jt9CGoJjZItsKnsSp8aiHDWfahVHX9qX2rU6uKf8+QhiJQFLFWo7nZeVvZYvUd64R6izEAQOLXuF7OrCB7DK16mWQEjvJcdy1sLv6JcLxzh/DGS+11uyJi+TqL1VzCZJqUmZxvF7yZpM7BL55YbE1YyyejnaVrVecviW2rUuy6s=',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36 AgentWeb/5.0.0  UCBrowser/11.6.4.950  ford-evos',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'timestamp': '1683475740080',
        'token': cookie,
        'sign': '41B4B1B29D1B9EDBB66478E026B9BE7C',
        'appVersion': '1.2.7',
        'Origin': 'https://evosh5.changanford.cn',
        'X-Requested-With': 'com.changanford.evos',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://evosh5.changanford.cn/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    data = '{"paramEncr":"gI2ZYcEHqfQEE34VLe83kmp8fj/aoueChw7Vd+L3ma8="}'

    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
    print(result)
    msg += f"签到7天抽奖：{result['msg']}！\n"
    print(msg)
    return msg

def qiandao(cookie):
    msg = ""
    url = 'https://evosapi.changanford.cn/user/signIn'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': '674AC2BD9462FE668EB8352B7C10FB2A',
        'body': '99914B932BD37A50B983C5E7C90AE93B',
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': 'Sx+uLlRALOz6+IuB0T8xLFZH8LwvIx/TSlk2rt8IBfuC3m2twTPJW4dw+SaLheI4UDLN7N3TosqHzDKQ+1VSjg9uSGM9oct5URXXDIGtY3z5wlD8C4e1jsYmTfWb2bBSBG8s/WI9qgwG4LNbYwrL8waiyrogj6jMsyQOujIMuT0=',
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': '1683475660211',
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'User-Agent': 'ford-evos',
    }
    data = '{"paramEncr":"QAjyx5a5MN/LyUN1cScmJg=="}'
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
    print(result)
    msg += f"签到：{result['msg']}！\n"
    print(msg)
    return msg
    
def dianzan(cookie):
    msg = ""
    url = 'https://evosapi.changanford.cn/con/posts/actionLike'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': '13FA4C978F99CA22C4AB90F0910C66D4',
        'body': '703352112693E705E8BB4F75ABC40751',
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': 'xqC2BKU7WQ6r+y35o+gdlbBzskHn0X4Gz/ssrrxsm4ikwWNiaMguDA+Z+E4SCyUnbZB/H7br5yjpbLw/05pyE07oK7kSmkmGtfVd2omzI8hMTIx8jLq7Xb4yrqXbeKMDz9Rs6Ibi9hCabQqwDPVYwCsD9Bp54F8N0BMTaWvBp0k=',
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': '1683350785305',
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'ford-evos',
    }
    data = '{"paramEncr":"NouQ+nFhP3HCZf9V+uYuSVNPDGkZnC2WZLj5BmIzuG4="}'
    success_count = 0 # 记录成功次数
    total_count = 0   # 记录总共尝试次数
    while success_count < 5 and total_count < 12:
        response = requests.post(url=url, headers=headers, data=data)
        result = response.json()
        print(result)
        time.sleep(5)
        if '点赞成功' in result['msg']:
            success_count += 1
            print(f"点赞{success_count}次成功！")     
        total_count += 1
    msg += f"点赞：{success_count}次！\n"
    print(msg)
    return msg
    
def zixun(cookie):
    msg = ""
    url = 'https://evosapi.changanford.cn/con/share/callback'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': '97BBDDE42A93291E40E682BC421BCBD5',
        'body': '979D5F5D7A75F9E63EAA08829C9E7604',
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': 'SJ3ylHvmdAuA1SG8xPdOiAXWY1S+ekvVvL4TFlTXbphb0PrQVapeYvz6WVHJfzIAOwnkmhbZrVpVIBSyVeFeTaZjwOsKnzgilM3pyvgEt4pMkxblUzEZkD3cQqeJsQVlJTMOVu7tVz/plD7PUrBNlgXO4pTDi3yEelk0/uDUEUo=',
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': '1683580430621',
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'User-Agent': 'ford-evos',
    }
    data = '{"paramEncr":"RRCvQsl8njB88hv33Eh7OgfqvhK597tDqO3XHEtc/mzPVaD7sjcNKCPJifsRxcga2LJqny+2rSP+nHXT1GdkcpnyFoELNVBcQQpr8dyGXgR1+lLmcfYMWSZqscnvC57/VCGSchN0HSL3uctbY+tzIXoqNR70enTS97E7iqnijy5vRgpyR3rvMiaJlQW3Bm4vyCi7XyjLfLOuMjQbhSmPSUQtjn4g5DTHIBtp8fHznRms1dsx/sXBFmOzhncq3nl728D+aixpqSGQG1uoMyk8cr7RUvdpvsswNiAZUyYkjTBgmYmZ6gMv3W3zt71jbPW7mKYGm3RXwm77IPJwRx7KjqM7HeY7VcJaNTJpFt4yICnfeB2SaPda2yHheSeUYndDliEHIxWcfPxeSo+WYmBm6vT1vE/gp18GnB9haMdLjIR2pMb5BnWw2CWferYg8h/McEIE9j4UhMwlKTorED4O6yIbwh5o92z3h+qQIWhQDvEy3ySIBOF7ZzXJghGj4EX0DlHiQq/p6LGJCc5Sb8mimTNVtNvMxZ6ycgz8pXQBkTgnzfWa6WDpHjApvo41GX/BGyVW124PKyuac1/N9MO1RFn5os8SD/Z5dmUfjbmLxiIfXDqBQNhb4FtCUy0dzkAy"}'
    success_count = 0 # 记录成功次数
    total_count = 0   # 记录总共尝试次数
    while success_count < 3 and total_count < 5:
        response = requests.post(url=url, headers=headers, data=data)
        result = response.json()
        print(result)
        time.sleep(5)
        if '操作成功' in result['msg']:
            success_count += 1
            print(f"分享资讯{success_count}次成功！")     
        total_count += 1
    msg += f"分享资讯：{success_count}次！\n"
    print(msg)
    return msg
    
def tiezi(cookie):
    msg = ""
    url = 'https://evosapi.changanford.cn/con/share/callback'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': 'F0518F5F2EDDC058863C4D41ADD878DD',
        'body': '864C4826CC07F9C510221BCA84B3CB8A',
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': 'Q5dIblTrBfhDcW6n2o+KlZkQBSHv3fRNcYOFIc4hXNqwgOW5mNL8mLmGoWa0wzK2IjA6kJGa1uCc8wdkPQKa1X10GMgS6D32Hv5PZj40qKLBy2Ju/lRJWkQe2rBWbeR/SuchfqNzlYdirMjDRCd7qM4nC9KleAE8HRTbHclJNbk=',
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': '1683273138658',
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'User-Agent': 'ford-evos',
    }
    data = '{"paramEncr":"C+zs9gblLdh2WFin9D5AUX70UKNKu/LJkfOiPIIdbbxIdeWlDJotPdygHYQ9odN3Jw4XnnFRDGRAjpZr2H7pVPjqU8M1JZk8v/nAcEzV+zE66egwiF7RWk2v2nuHM8IKXAHfj+K98Rz5YgwdDTHR+cokqD5MMxJgy7OzxqJ3krMgZJZqjj2DjfWF7Cz6q3OQcddogOMWbfUyuvYAAOI5cs+XWa7FWtow/9IF80BhAbayet/80OkN9tr3jL7YtSvuUIVKKJ8SkqVjNX5Mbv6azHeC7gs77MnJ9ekqybk337qNiuMMJDmiRdAyo+vIZp0fTF6+98lNLyzUDAWkAWxlhyWjKfI1VJD6U77cFUrPJtxIPAK8yf9uaOFVuaeybHhuJOfQ1TDXad6NoamrcgARuf+pHiB99/LfdCkBofKaw+Es4r9oXO3D1/PPwJc/Lye6ZFKbjiL1b5XAZd8oRdM/zqh7d5UuMcRNKQW+ZUiHR7dZxetSzrqmwMu0L394jV2lSQEAB1e3BuGVvtmj3JoSI4rTUwrCN3a6GKOTUSAwzWXwlCyVrBFRdUykSwqTWPeE"}'
    success_count = 0 # 记录成功次数
    total_count = 0   # 记录总共尝试次数
    while success_count < 3 and total_count < 5:
        response = requests.post(url=url, headers=headers, data=data)
        result = response.json()
        print(result)
        time.sleep(5)
        if '操作成功' in result['msg']:
            success_count += 1
            print(f"分享帖子{success_count}次成功！")     
        total_count += 1
    msg += f"分享帖子：{success_count}次！\n"
    print(msg)
    return msg
    
def huifu(cookie):
    msg = ""
    url = 'https://evosapi.changanford.cn/con/posts/addComment'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': '1AA7F33D57D04FF104CA0BA2F5025E44',
        'body': 'C80F14C55439E1A30B5CE5154742DC79',
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': 'bS9C/fuujAPGrwi95OajynaupDF9jdNaGWKIvfwplV/nxB1lsEVG0+bSB0GNpxYpABob3Q+6VcLgvU6qNDWEXD4CT0QBaC+KSa5QfD5BNFUyXtuF3ENd3UtGovragwtqBbhXhZpLA2tdsYWg5HWAADn5ySlRUY7fNt59fPyKIsg=',
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': '1683351139151',
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'User-Agent': 'ford-evos',
    }
    data = '{"paramEncr":"hoKLnEODAPIOEIhUCVXEiQ8TTizCpv08G5mR4MceBuHuIYdxNYwA6oP7gCbRY/U19mBzd7nm3ObwEF22RmYyc3GAuK55svGDGsQTc6UkC4kb4+htaJh/r8Oi7PrItH4/"}'
    success_count = 0 # 记录成功次数
    total_count = 0   # 记录总共尝试次数
    while success_count < 5 and total_count < 6:
        response = requests.post(url=url, headers=headers, data=data)
        result = response.json()
        print(result)
        time.sleep(10)
        if '操作成功' in result['msg']:
            success_count += 1
            print(f"评论|回复{success_count}次成功！")     
        total_count += 1
    msg += f"评论|回复：{success_count}次！\n"
    print(msg)
    return msg
    
def fatie(cookie):
    msg = ""
    url = 'https://evosapi.changanford.cn/con/posts/addPosts'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': 'E29D1E3810CF641D9C9466D6FD6C57E4',
        'body': '1AE0E9A39466462C781EB59537876AFE',
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': 'qWWZBdg+EYpjvrI7uFzYiWaEJwXsLrUo2po7ptOrrPJNNkdn8n3uurc0QZCyD+1pzsUhRNUgFUMLb+yvXfCgGDRmUTNsHg7QMue9UF8S2RO20bNdRdrj8W5NKWiLD8V9RjG3F/L2MPRrUPq3e7wzkMlZ81XQXKzqlzpku8k/Gt8=',
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': '1683273579328',
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'User-Agent': 'ford-evos',
    }
    data = '{"paramEncr":"tHzd+87rdhFvZczxNmCk/GCFoSVcwffJubotmuRx9W9xREUWOL5DobOmbQVEe/DT4tUB92RWV5mGSbsHq3E1iWyPxYB4cpvXbFt2/WLmxgkiTTPpMpjMEFlxcP1xETcMrU1i38ZmRIsBgLBkpszSNKH3nJFqYnXf9Typ8CObpSUPyFZvXeVvYCwqsWBAD2BusJOG/wHNU6/hHCJBFrEBgH/kZeyAIyBo6gWZGiBFf2JMxUvcpJRkYzDDOCsw7jYX3XAv11Fng9jJ6E3nZx63WpQxOiRD9SgCg5JN7VMeEFWtQVAe1COzN6S4kWTz7XxC"}'
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
    print(result)
    msg += f"发帖：{result['msg']}！\n"
    print(msg)
    return msg

def chaxun():
    msg = ""
    url = 'https://cafwkf.changanford.cn/cafwkf-app-wxminiapp/v1/cmcApi/getCustomerInfo'
    headers = {
        'Host': 'cafwkf.changanford.cn',
        'Connection': 'keep-alive',
        'charset': 'utf-8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/107.0.5304.141 Mobile Safari/537.36 XWEB/5049 MMWEBSDK/20230405 MMWEBID/6162 MicroMessenger/8.0.35.2360(0x28002339) WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv/android',
        'content-type': 'application/json',
        'access-token': 'eyJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50SWQiOjEzMzc1OTQyMjIyMTM0ODIyMDksImluc3RhbmNlSWQiOi0xLCJhY2NvdW50TmFtZSI6IkZEMTY0NDY5MDQxMjM1NjYzNjY3MiIsImxvZ2luTmFtZSI6IkZEMTY0NDY5MDQxMjM1NjYzNjY3MiIsInRlbmFudElkIjotMSwiaWQiOjEzMzc1OTQyMjIyMTM0ODIyMDksImFwcGxpY2F0aW9uQ29kZSI6IkNBRldLRi1BUFAtV1hNSU5JQVBQIiwidW5pcXVlSWQiOiJjMWM4MzA5Ny05NDk3LTRmMDQtYjQzNC0yMmNiZmJiZjVhNzMiLCJqdGkiOiIyZGVhNDgzMi04YWZiLTQxMjEtOWQ0MC01ZTFmOGMyZmZiMjYiLCJuYmYiOjE2ODM1MDQzNDksImV4cCI6MjY4MzUwNDM0OH0.tZwnL5pLR7UBwHSJ_laIxronxt15F7EHjd-lXn7zOmg',
        'Referer': 'https://servicewechat.com/wxdedb3aece36a5f8a/112/page-frame.html',
    }
    json = {
        'userId': 'U488973090246210082',
        'sourceType': 'FT_CUSTOMER_APPLET',
    }
    response = requests.post(url=url, headers=headers, json=json)
    result = response.json()
    print(result)
    score = result['data']['score']
    msg += f"当前福币：{score}"
    print(msg)
    return msg

def ql_env():
    if "FYtoken" in os.environ:
        token_list = os.environ['FYtoken'].split('\n')
        if len(token_list) > 0:
            return token_list
        else:
            print("FYtoken变量未启用")
            sys.exit(1)
    else:
        print("未添加FYtoken变量")
        sys.exit(0)

if __name__ == '__main__':
    msg = ""
    index = 1
    quantity = ql_env()
    print (f"共找到{len(quantity)}个账号")
    for cookie in quantity:
        print(f"------------正在执行第{index}个账号----------------")
        jihuo(cookie)
        msg += f"第{str(index)}个账号运行结果: \n"
        msg += qiandao(cookie)
        msg += fatie(cookie)
        msg += dianzan(cookie)
        msg += zixun(cookie)
        msg += tiezi(cookie)
        msg += huifu(cookie)
        msg += choujiang(cookie)
        msg += chaxun()
        time.sleep(5)
        index += 1
    send('福域', msg)