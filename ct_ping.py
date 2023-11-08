'''
cron: 36 9 * * *
new Env('网络测试');
'''

import requests
import time

def test_network_stability(url, times=100, delay=2, timeout=10):
    response_times = []
    success_count = 0
    failure_count = 0

    for i in range(times):
        start_time = time.time()
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Raises stored HTTPError, if one occurred.
            print(f"请求 {i+1} 成功。")
            success_count += 1
        except (requests.HTTPError, requests.ConnectionError, requests.Timeout) as err:
            print(f"请求 {i+1} 失败，网络错误：{err}")
            failure_count += 1
        end_time = time.time()
        response_times.append(end_time - start_time)

        time.sleep(delay)  # wait for 2 seconds before next request

    average_response_time = sum(response_times) / len(response_times)
    print(f"{times} 次请求的平均响应时间：{average_response_time} 秒")
    print(f"成功次数：{success_count}，失败次数：{failure_count}")

test_network_stability("https://gitee.com")
