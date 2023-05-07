'''
cron: */30 * * * *
new Env('福域');
'''

import requests
import os
import json
import time
#print(f"==================脚本执行- 北京时间(UTC+8)：{time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}=====================\n")
#from sendNotify import send
#from os import environ

def qiandao(cookie):
    msg = ""
    url = 'https://evosapi.changanford.cn/user/signIn'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': '97AA8AF9FE6129B6F0C424771E8B3FFF',
        'body': '99914B932BD37A50B983C5E7C90AE93B',
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': 'PlNsG9QMdvbdgLVa1lrrPF4bDbKQOsi7JE2B2vHJ7KNWgF8+ZE5YvdoROgR1+Iz4Z6EwNdxxoJSJz0j2esX/Q96ohXKT7MLkCWhpaRY6oHXTL9E3Bya8veL8Q85kx7KlEtsmbBixEyDQb6+eFNjuz8e+pEC1MnjnYOa8rZfBxVE=',
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': '1683391102473',
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'User-Agent': 'ford-evos',
    }
    data = '{"paramEncr":"lUd2+hUCDyae7SN4fD5NEw=="}'
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
    print(result)
    if '操作成功' in result['msg']:
        msg += f"签到：{result['msg']}！\n"
    elif '今天您已签到' in result['msg']:
        msg += f"签到：{result['msg']}！\n"
    else:
        msg += f"签到：{result['msg']}！\n"
    print(msg)
    return msg
    
def dianzan(cookie):
  #  msg = ""
    url = 'https://evosapi.changanford.cn/con/posts/actionLike'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': 'F0518F5F2EDDC058863C4D41ADD878DD',
        'body': '703352112693E705E8BB4F75ABC40751',
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': 'ioExDJcBRKX805Z18Zeo/3U7Qx1v+EnD/DThp6w9Iz5rweDZBTED1yoim+fyxef9Uluzx5dXLPASZ2a3qe+QgSzTYMzj1bQVGLwHKeAdvureKG2nAJd1Jbcfko9GNYg5cnsrOQPK92JaiXU7pBlHpOva2M2Ztlt4c9Nx8x9bW4Q=',
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': '1683361884265',
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Content-Length': '60',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'ford-evos',
    }
    data = '{"paramEncr":"pbS+spFyjlW04+Ad6jbTI5H/TjfEkVn2mEDR58hc0SY="}'
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
    print(result)
    
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
    if '操作成功' in result['msg']:
        msg += f"发帖：{result['msg']}！\n"
    else:
        msg += f"发帖：{result['msg']}！\n"
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
 #   msg = ""
    index = 1
    quantity = ql_env()
    print (f"共找到{len(quantity)}个账号")
    for cookie in quantity:
        print(f"------------正在执行第{index}个账号----------------")
      #  msg += f"第{str(index)}个账号运行结果: \n"
      #  msg += qiandao(cookie)
     #   msg += fatie(cookie)
        dianzan(cookie)
    #    msg += zixun(cookie)
   #     msg += tiezi(cookie)
     #   msg += huifu(cookie)
     #   time.sleep(5)
        index += 1
  #  print(msg)
#    send('福域', msg)

#dianzan(cookie)