'''
cron: 0 */1 * * *
new Env('哪吒商品库存');
'''
import requests,json,time
from notify import send

goods_list = [1639094260312801281,1747913042685448194]
msg = []
headers = {
    'Host': 'shop-wap.hozonauto.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/119.0.6045.193 Mobile Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}

for goods in goods_list:
    url = 'https://shop-wap.hozonauto.com/gateway/mallapi/goodsspu/detail/' + str(goods)
    response = requests.get(url, headers=headers)
    result = response.json()
    if result['ok'] is True:
        name = result['data']['name']
        stock = result['data']['skus'][0]['stock']
        aaa = f"{name}：{stock}"
        print(aaa)
        msg.append(aaa)
    time.sleep(5)
send("哪吒库存", '\n'.join(msg))
