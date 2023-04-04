import requests
import os
import json
from sendNotify import send
from os import environ
cookie = os.environ["txspcookie"]
title = "腾讯视频"
url_qd = "https://vip.video.qq.com/rpc/trpc.new_task_system.task_system.TaskSystem/CheckIn?rpc_data=%7B%7D"
url_gk = "https://vip.video.qq.com/rpc/trpc.new_task_system.task_system.TaskSystem/ProvideAward?rpc_data=%7B%22task_id%22:1%7D"

def ten_video():
    headers = {
        'user-agent':'Mozilla/5.0 (Linux; Android 11; M2104K10AC Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046237 Mobile Safari/537.36 QQLiveBrowser/8.7.85.27058',
        'Content-Type':'application/json',
        'referer':'https://film.video.qq.com/x/vip-center/?entry=common&hidetitlebar=1&aid=V0%24%241%3A0%242%3A8%243%3A8.7.85.27058%244%3A3%245%3A%246%3A%247%3A%248%3A4%249%3A%2410%3A&isDarkMode=0',
        'cookie':cookie
    }
    response_1 = requests.get(url_qd,headers=headers).json()
    print(response_1.text)
    content = "成功"
    send(title,content)

if __name__ == '__main__':
    ten_video()
