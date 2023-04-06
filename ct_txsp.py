import requests
import os
import json
from sendNotify import send
from os import environ
cookie = os.environ["txspcookie"]
url = "https://vip.video.qq.com/rpc/trpc.new_task_system.task_system.TaskSystem/CheckIn?rpc_data=%7B%7D"
url1 = "https://vip.video.qq.com/rpc/trpc.new_task_system.task_system.TaskSystem/ProvideAward?rpc_data=%7B%22task_id%22:1%7D"

headers={
    'user-agent':'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046237 Mobile Safari/537.36 QQLiveBrowser/8.8.05.27133',
    'Content-Type':'application/json',
    'referer':'https://film.video.qq.com/x/vip-center/?entry=common&hidetitlebar=1&aid=V0%24%241%3A0%242%3A8%243%3A8.7.85.27058%244%3A3%245%3A%246%3A%247%3A%248%3A4%249%3A%2410%3A&isDarkMode=0',
    'cookie':cookie
}

def main():
    response = requests.get(url,headers=headers)
    result = response.json()
    print(result)
    if result["ret"] == 0: 
        check_in_score = result['check_in_score']
        msg = ""
        msg += f"签到获得成长值: {check_in_score}\n"
        response1 = requests.get(url1,headers=headers)
        result1 = response1.json()
        print(result1)
        provide_value = result1['provide_value']
        msg += f"观看视频成长值: {provide_value}\n"
        print(msg)
        send("腾讯视频", msg)
    elif result["ret"] == -110009:
        res2 = "出现图形验证，请手动签到后第二天运行此脚本"
        send("腾讯视频",res2)
    else:
        print("结束")

if __name__ == '__main__':
    main()
