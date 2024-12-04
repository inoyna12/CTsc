import time
# 使用绝对路径导入，避免多次加载tool.py
from tools.tool import rts
        
def xiequ():
    url = 'http://api.xiequ.cn/VAD/GetIp.aspx?act=get&uid=148434&vkey=1FB88D53032912792BD945D41B22AD0B&num=1&time=30&plat=0&re=1&type=2&so=1&ow=1&spl=1&addr=&db=1'
    testUrl = "https://www.xiequ.cn/OnlyIp.aspx?yyy=123"
    for i in range(5):
        result = rts('get', url)
        if result and result['code'] == 0:
            ip = result["data"][0]["IP"]
            port = result["data"][0]["Port"]
            print(f"代理：{ip}:{port}")
            proxy = {
                "http": f"http://{ip}:{port}",
                "https": f"http://{ip}:{port}"
            }
            result = rts('get', testUrl, respType='text', proxies=proxy)
            if result:
                return proxy
        time.sleep(5)
    print("获取代理ip失败")
    return None
        
def juliang():
    url = 'http://v2.api.juliangip.com/company/postpay/getips?num=1&pt=1&result_type=json&trade_no=6130652715138961&sign=3b1896626239e61a182b00ac5582d07f'
    testUrl = "https://www.juliangip.com/api/general/Test"
    for i in range(5):
        result = rts('get', url)
        if result and result['code'] == 200:
            ip_port = result['data']['proxy_list'][0]
            print("代理：" + ip_port)
            proxy = {
                "http": f"http://{ip_port}",
                "https": f"http://{ip_port}"
            }
            result = rts('get', testUrl, respType='text', proxies=proxy)
            if result:
                return proxy
        time.sleep(5)
    print("获取代理ip失败")
    return None
