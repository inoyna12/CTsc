import requests,time
#import curl_cffi.requests as requests
# 提取代理API接口，获取1个代理IP
#api_url = "http://v2.api.juliangip.com/dynamic/getips?filter=1&num=1&pt=1&result_type=json&trade_no=1282958555546938&sign=31a2348320c6b0938bb566fdd4e37b7e"
api_url = "http://v2.api.juliangip.com/company/postpay/getips?num=1&pt=1&result_type=json&trade_no=6130652715138961&sign=3b1896626239e61a182b00ac5582d07f"
# 获取API接口返回的代理IP
# proxy_ip = requests.get(api_url).json()
# proxy_list_ip = proxy_ip['data']['proxy_list'][0]
# print("当前代理ip：" + proxy_list_ip)

# proxies = {
  # "http": proxy_list_ip,
  # "https": proxy_list_ip,
# }

def get_public_ip():
    try:
        response = requests.get('http://ipinfo.io/json', proxies=proxies)
        result = response.json()
        print(result['ip'])
    except Exception as e:
        print(e)


for i in range(10):
    proxy_ip = requests.get(api_url).json()
    print(proxy_ip)
    proxy_list_ip = proxy_ip['data']['proxy_list'][0]
    print("当前代理ip：" + proxy_list_ip)
    
    proxies = {
      "http": proxy_list_ip,
      "https": proxy_list_ip,
    }
    get_public_ip()
    time.sleep(10)
