'''
cron: 26 9 * * * ct_FY.py
new Env('福域');
'''

import requests
import os
import json
import time
#print(f"==================脚本执行- 北京时间(UTC+8)：{time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}=====================\n")
from sendNotify import send
from os import environ

def qiandao(cookie):
    msg = ""
    url = 'https://evosapi.changanford.cn/user/signIn'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': 'FC51656005655CF88ECAE541113E4FA9',
        'body': '99914B932BD37A50B983C5E7C90AE93B',
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': 'PlNsG9QMdvbdgLVa1lrrPF4bDbKQOsi7JE2B2vHJ7KNWgF8+ZE5YvdoROgR1+Iz4Z6EwNdxxoJSJz0j2esX/Q96ohXKT7MLkCWhpaRY6oHXTL9E3Bya8veL8Q85kx7KlEtsmbBixEyDQb6+eFNjuz8e+pEC1MnjnYOa8rZfBxVE=',
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': '1683026678109',
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'User-Agent': 'ford-evos',
    }
    data = '{"paramEncr":"XKzFk3KJLGI24Xz+IlKUMA=="}'
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
    if '操作成功' in result['msg']:
        msg += f"签到：{result['msg']}！"
    elif '今天您已签到' in result['msg']:
        msg += f"签到：{result['msg']}！"
    else:
        print("签到失败")
    print(msg)
    return msg
    
def dianzan(cookie):
    msg = ""
    url = 'https://evosapi.changanford.cn/con/posts/actionLike'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': '0166096D9F0E746786A7C6D25F19553A',
        'body': '2DC981D64DFE66D4C898053A13ED51DB',
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': 'olBeWpamXJp3DWe+7ylxT8Al+TaXuLMlPjNr6xU9SqWCB4FDSsbpUsqfESJUsa0aAJuKjElyvQ30Y4ha+UKTT70U9tLzC0Symqeli02QZ1xbs4e1OJLFkei+GXtxine+Q0Q8Mp7JGtqorsyWA4mvz3DS7Ubp5T+Fl9JFV0+LIdk=',
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': '1683197830526',
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'User-Agent': 'ford-evos',
    }
    data = '{"paramEncr":"yEWu+3Rp/EkD9PrAajfCVDxGBJhlOA2abu/08AG0KBI="}'
    success_count = 0 # 记录成功次数
    total_count = 0   # 记录总共尝试次数
    while success_count < 5 and total_count < 12:
        response = requests.post(url=url, headers=headers, data=data)
        result = response.json()
        time.sleep(5)
        if '点赞成功' in result['msg']:
            success_count += 1
            print(f"点赞{success_count}次成功！")     
        total_count += 1
    msg += f"点赞：{success_count}次！"
    print(msg)
    return msg
    
def zixun(cookie):
    msg = ""
    url = 'https://evosapi.changanford.cn/con/share/callback'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': '656A856200D6592CB8CD2798832405F7',
        'body': 'DE2B450C8CEBDBAB9E05AAAA4245660A',
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': 'IM0573c4EoJYBqSs3oXmxlIWSKc/xyrdHvW+0uruvHn8xSXAlIQC7ElIMBG60lZtEyL7e0znG6olxIyULzB13Q8pzDRzobSbLRJCvWeKEmF+/s1bH8y5A+DpfZREVBGmsrOyTIzkwU1Su58otBQsLxC86AozYLI+IVNSvI0+xPw=',
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': '1683197341882',
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'User-Agent': 'ford-evos',
    }
    data = '{"paramEncr":"zYE60FfprFVilaney7P23TfB7u+G6tZjjz+85U5TQsRD/4HQr+5YIeWNrF+CHyM9BXV0d4Atswk3CAwvUldjIiIN5fFdek+QyJqyybpMz+/fFjOWAB0y7AB9oSuQYONiC0AfsEz9+vLrVdINr/rpQwKy3n9XDFgVdICdbfNlOhd8vxNPqpMgcA9JIJ0/aDfzDrcEJgz6aHGmkd7uvE2hCrUV103ly+1dMSkJGuOPXF0BbhBivAejt89dsvBYka4Q281sduSvn+2uVOxo1iEJ4Fgjp5yLpex+VpeKPYE3nvHL7iyikrw36IAuZl+BNQ08xzcCkPCXKo7LigoKL6vpzJOBZhuMztTUuzW6kLjWtK07hndZ5+snSY3fiqEwF/6T4SdymjkaQG1fycIJqm5pW1smDss9vNljKG+Isnb1X+ohs2Hvh0YfipE6KCLouQHX9nXTXGpNUG8ng7YBQP8+ZaNlaoDriaz8bHbcouyiVSi10yoHoZJ7LIlhgEpAHQEpKAQbK8+4mWQLCCWBgNqIH44i5doEtkF0eIXYbS6JBWHJ4xTcLh7pXqAeMAx+hYCMe4QjGvVdzKRtJPOC1bQ9+hPb8AWXFKRn0c1dCeET4qrJtwkZ8kycWrIIuto0L3Ef"}'
    success_count = 0 # 记录成功次数
    total_count = 0   # 记录总共尝试次数
    while success_count < 3 and total_count < 5:
        response = requests.post(url=url, headers=headers, data=data)
        result = response.json()
        time.sleep(5)
        if '操作成功' in result['msg']:
            success_count += 1
            print(f"分享资讯{success_count}次成功！")     
        total_count += 1
    msg += f"分享资讯：{success_count}次！"
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
        time.sleep(5)
        if '操作成功' in result['msg']:
            success_count += 1
            print(f"分享帖子{success_count}次成功！")     
        total_count += 1
    msg += f"分享帖子：{success_count}次！"
    print(msg)
    return msg
    
def huifu(cookie):
    msg = ""
    url = 'https://evosapi.changanford.cn/con/posts/addComment'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': '31E0ACCFD2051985EC1605F586D2C106',
        'body': 'ED2219265CC1224D74AEA17FAA2A1C51',
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': 'cmO7RQLs1MyWabWBz9IVgn2L2N7zxzmWQMOFO8ybqwDkZzt6KLdPhq0JO2SYoVKX2yrLsmSy09/GSz+VFBzBe2WQBTimVLcrri+/vjSba3I+nQKhHwfdqJcl9zIdAqZauVNVI2DzKMh5B9yY0TxXDLv7C1HyyVHDlT67dkdNVHw=',
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': '1683197609895',
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'User-Agent': 'ford-evos',
    }
    data = '{"paramEncr":"oU/jZ3vw6Dq1aE/7DwiJqSlunLUlnsyo/sRNDOByyEhytNfawGzrdUeSwMAM81AcUOHQakDck3+ClXM6EFAb2E1scDgji/Pg8BiGo4eGZcUOIwHk/5wFNyAZOM61iVGR"}'
    success_count = 0 # 记录成功次数
    total_count = 0   # 记录总共尝试次数
    while success_count < 5 and total_count < 6:
        response = requests.post(url=url, headers=headers, data=data)
        result = response.json()
        time.sleep(10)
        if '操作成功' in result['msg']:
            success_count += 1
            print(f"评论|回复{success_count}次成功！")     
        total_count += 1
    msg += f"评论|回复：{success_count}次！"
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
    if '操作成功' in result['msg']:
        msg += f"发帖：{result['msg']}！"
    else:
        print("发帖失败")
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
        print (f"------------正在执行第{index}个账号----------------")
        msg += f"第{str(index)}个账号运行结果: \n"
        msg += qiandao(cookie)
        msg += fatie(cookie)
        msg += dianzan(cookie)
        msg += zixun(cookie)
        msg += tiezi(cookie)
        msg += huifu(cookie)
        time.sleep(5)
        index += 1
    send('福域', msg)