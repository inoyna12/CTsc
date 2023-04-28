'''
cron: 6 9 * * * ct_txsp8.py
new Env('腾讯视频礼遇日抽奖');
'''

import requests
import os
import json
import time
#print(f"==================脚本执行- 北京时间(UTC+8)：{time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}=====================\n")
from sendNotify import send
from os import environ

def choujiang(cookie):
    try:
        msg = ""
        url = "https://activity.video.qq.com/fcgi-bin/asyn_activity?platform=8&type=100143&option=100&act_id=sj85gxwpc28azgd6wa6fydyqu5&module_id=0wd9irj6c9jxkfxd6069at07j5&ptag=ad.djtx.tc&is_prepublish=&aid=V0%2524%25242%253A8%25244%253A3%25248%253A4%25243%253A8.8.10.27151%25241%253A0%252444%253Aae092621&otype=xjson&_ts=1681081812372"
        headers={
            'user-agent':'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/89.0.4389.72 MQQBrowser/6.2 TBS/046237 Mobile Safari/537.36 QQLiveBrowser/8.8.05.27133',
            'Content-Type':'application/json',
            'referer':'https://m.film.qq.com/magic-act/sj85gxwpc28azgd6wa6fydyqu5/index_index.html?ptag=ad.djtx.tc&ovscroll=0&page=index&aid=V0%24%242%3A8%244%3A3%248%3A4%243%3A8.8.10.27151%241%3A0%2444%3Aae092621&isDarkMode=0',
            'cookie':cookie
        }
        response = requests.get(url,headers=headers)
        result = response.json()
        print(result)
        if result['frame_resp']['msg'] == 'ok': 
            lotter_ext = result['lotter_ext']#中奖提示
            prize_list = result['prize_list']['lotter_name']#奖品信息
            msg += f"{lotter_ext}{prize_list}\n\n"
            print(msg)
        elif result['ret'] == -43:
            msg += f"{result['msg']}\n"
            print(msg) 
        else:
            print("未知错误\n") 
    except:
        msg += f"Cookie失效或脚本待更新\n"
        print(msg)
    return msg

def ql_env():
    if "txspcookie8" in os.environ:
        token_list = os.environ['txspcookie8'].split('\n')
        if len(token_list) > 0:
            return token_list
        else:
            print("txspcookie8变量未启用")
            sys.exit(1)
    else:
        print("未添加txspcookie8变量")
        sys.exit(0)

if __name__ == '__main__':
    msg = ""
    index = 1
    quantity = ql_env()
    print (f"共找到{len(quantity)}个账号")
    for cookie in quantity:
        print (f"------------正在执行第{index}个账号----------------")
        msg += f"第{str(index)}个账号运行结果: \n"
        msg += choujiang(cookie)
        time.sleep(2)
        index += 1
    print(msg)
   # send('腾讯视频礼遇日抽奖', msg)
   