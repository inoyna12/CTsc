'''
cron: 6 9 * * * ct_txsp.py
new Env('腾讯视频签到');
'''

import requests
import os
import json
import time
#print(f"==================脚本执行- 北京时间(UTC+8)：{time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}=====================\n")
from sendNotify import send
from os import environ

def qiandao(cookie):
    try:
        msg = ""
        url = "https://vip.video.qq.com/rpc/trpc.new_task_system.task_system.TaskSystem/CheckIn?rpc_data=%7B%7D"
        headers={
            'user-agent':'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046237 Mobile Safari/537.36 QQLiveBrowser/8.8.05.27133',
            'Content-Type':'application/json',
            'referer':'https://film.video.qq.com/x/vip-center/?entry=common&hidetitlebar=1&aid=V0%24%241%3A0%242%3A8%243%3A8.7.85.27058%244%3A3%245%3A%246%3A%247%3A%248%3A4%249%3A%2410%3A&isDarkMode=0',
            'cookie':cookie
        }
        response = requests.get(url,headers=headers)
        result = response.json()
        if result['ret'] == 0: 
            check_in_score = result['check_in_score']
            msg += f"签到获得成长值: {check_in_score}\n"
            print(msg)
            msg += video_60(cookie)
            msg += chaxun(cookie)
        elif result['ret'] == -110009:
            msg += "出现图形验证，请手动签到后第二天运行此脚本\n\n"
            print(msg)
        elif result['ret'] == -2007:
            msg += "非会员无法签到\n\n"
            print(msg)
        elif result['ret'] == -2002:
            msg += "请勿重复签到\n"
            print(msg)
            msg += video_60(cookie)
            msg += chaxun(cookie)
        else:
            print("未知错误\n")    
    except:
        msg += f"Cookie失效或脚本待更新\n"
        print(msg)
    return msg
    
    
def video_60(cookie):
    msg = ""
    url = "https://vip.video.qq.com/rpc/trpc.new_task_system.task_system.TaskSystem/ProvideAward?rpc_data=%7B%22task_id%22:1%7D"
    headers={
        'user-agent':'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046237 Mobile Safari/537.36 QQLiveBrowser/8.8.05.27133',
        'Content-Type':'application/json',
        'referer':'https://film.video.qq.com/x/vip-center/?entry=common&hidetitlebar=1&aid=V0%24%241%3A0%242%3A8%243%3A8.7.85.27058%244%3A3%245%3A%246%3A%247%3A%248%3A4%249%3A%2410%3A&isDarkMode=0',
        'cookie':cookie
    }
    response = requests.get(url,headers=headers)
    result = response.json()
    if result['ret'] == 0:
        provide_value = result['provide_value'] 
        msg += f"观看视频成长值: {provide_value}\n"
        print(msg)
    elif result['ret'] == -2003:
        msg += f"任务未完成或重复领取\n"
        print(msg)
    return msg

def chaxun(cookie):
    msg = ""
    url = "https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_vscore_user_mashup&cmd=&otype=xjson&type=1"
    headers={
        'user-agent':'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046237 Mobile Safari/537.36 QQLiveBrowser/8.8.05.27133',
        'Content-Type':'application/json',
        'referer':'https://film.video.qq.com/x/vip-center/?entry=common&hidetitlebar=1&aid=V0%24%241%3A0%242%3A8%243%3A8.8.10.27151%244%3A3%245%3A%246%3A%247%3A%248%3A4%249%3A%2410%3A&isDarkMode=0',  
        'cookie':cookie
    }
    response = requests.get(url,headers=headers)
    result = response.json()
    level = result['lscore_info']['level']
    score = result['lscore_info']['score']
    msg += f"当前会员等级: {level}，成长值: {score}\n\n"
    print(msg) 
    return msg

def ql_env():
    if "txspcookie" in os.environ:
        token_list = os.environ['txspcookie'].split('\n')
        if len(token_list) > 0:
            return token_list
        else:
            print("txspcookie变量未启用")
            sys.exit(1)
    else:
        print("未添加txspcookie变量")
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
        time.sleep(10)
        index += 1
  #  print(msg)
    send('腾讯视频', msg)
