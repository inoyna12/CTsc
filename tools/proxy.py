import time
# 使用绝对路径导入，避免多次加载tool.py
from tools.tool import rts
        
def xiequ():
    # 计算流量
    # url = 'http://api.xiequ.cn/VAD/GetIp.aspx?act=getturn51&uid=148434&vkey=BD4E75D34471DA872A158633C8E543EB&num=1&time=6&plat=1&re=0&type=7&so=1&group=51&ow=1&spl=1&addr=&db=1'
    #计算次数
    url = 'http://api.xiequ.cn/VAD/GetIp.aspx?act=get&uid=148434&vkey=1FB88D53032912792BD945D41B22AD0B&num=1&time=30&plat=1&re=1&type=2&so=1&ow=1&spl=1&addr=&db=1'
    testUrl = "https://www.xiequ.cn/OnlyIp.aspx?yyy=123"
    for i in range(8):
        result = rts('get', url, respType='text')
        if result:
            if 12 <= len(result) <= 20:
                print(f"代理：{result}")
                proxy = {
                    "http": f"http://{result}",
                    "https": f"http://{result}"
                }
                result = rts('get', testUrl, respType='text', proxies=proxy)
                if result:
                    return proxy
                else:
                    time.sleep(10)
                    continue
            else:
                print(result)
        time.sleep(30)
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
