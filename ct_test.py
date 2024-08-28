import requests, json
from notify import send

notAdd = ['流量包', '畅听包', '畅享包', '娱乐包']
msg = []

headers = {
    'appVersion': '6.4.1',
    'login_channel': '1',
    'channel': 'android',
    'phoneModel': 'Redmi 22081212C',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Linux; U; Android 12; zh-cn; 22081212C Build/SKQ1.220303.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
    'Host': 'shop-gw.hozonauto.com',
    'Connection': 'Keep-Alive',
    # 'Accept-Encoding': 'gzip',
    'Cache-Control': 'no-cache',
}

params = {
    'current': '1',
    'size': '50',
    'categoryId': '',
    'priceSort': '1',
}

response = requests.get('https://shop-gw.hozonauto.com/mallapi/goodsspu/page/category', params=params, headers=headers)
result = response.json()
for i in result['data']['records']:
    if int(i['salesPrice']) > 200:
        break
    goods = f"{i['name']}，价格：{i['salesPrice']}，库存：{i['stock']}"
    print(goods)
    if any(name in i['name'] for name in notAdd):
        pass
    else:
        if i['stock'] > 0:
            msg.append(goods)
send("哪吒库存", '\n'.join(msg))
