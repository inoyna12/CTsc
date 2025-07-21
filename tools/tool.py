import requests
import json
import time
import random
from datetime import datetime

# 网络请求
def rts(method, url, respType='json', **kwargs):
        time_out = 10
        try:
            method = method.upper()
            if method not in ['GET', 'POST', 'PUT']:
                raise ValueError(f"不支持 {method} 请求方法")
            response = requests.request(method, url, timeout=time_out, **kwargs)
            if respType == 'text':
                return response.text
            return response.json()
        except requests.exceptions.Timeout as e:
            print(f"请求超时：{url}")
        except requests.exceptions.RequestException as e:
            print(f"请求错误：{url}")
        except Exception as e:
            print("其他错误:", str(e))
        return False

# 随机延时
def randomSleep(min_val, max_val):
    num = random.randint(min_val, max_val)
    print(f"随机等待{num}秒后继续>>>>>>>>>>>")
    time.sleep(num)

# 系统时间，格式：2024-12-04 10:54:23.740
def current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

# ip代理，获取代理链接需直接返回ip:端口
def proxy(proxyUrl, testUrl, isTest=False):
    for i in range(8):
        result = rts('get', proxyUrl, respType='text')
        if result:
            if result.count('.') == 3:
                print(f"使用代理：{result}")
                proxy = {
                    "http": f"http://{result}",
                    "https": f"http://{result}"
                }
                if not isTest:
                    return proxy
                test_result = rts('get', testUrl, respType='text', proxies=proxy)
                if test_result:
                    return proxy
                else:
                    time.sleep(10)
                    continue
            else:
                print(result)
        time.sleep(30)
    print("获取代理ip失败")
    return None
