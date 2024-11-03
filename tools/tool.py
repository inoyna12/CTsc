import requests
import json
import time

def rts(method, url, **kwargs):
        time_out = 10
        try:
            method = method.upper()
            if method not in ['GET', 'POST', 'PUT']:
                raise ValueError(f"不支持 {method} 请求方法")
            response = requests.request(method, url, timeout=time_out, **kwargs)
            try:
                return response.json()
            except ValueError:
                return response.text
        except requests.exceptions.Timeout as e:
            print(f"请求超时：{url}")
        except requests.exceptions.RequestException as e:
            print(f"请求错误：{url}")
        except Exception as e:
            print("其他错误:", str(e))
        return False

def randomSleep(min_val, max_val):
    num = random.randint(min_val, max_val)
    print(f"随机等待{num}秒后继续>>>>>>>>>>>")
    time.sleep(num)
