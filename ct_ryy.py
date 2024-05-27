'''
cron: 0 */3 * * *
new Env('仁源云库存监控');
'''

import requests
from bs4 import BeautifulSoup
from notify import send

# 目标网页的URL
url = 'http://www.renyuanyun.com/cart'

# 发送GET请求
response = requests.get(url)

# 确保请求成功
if response.status_code == 200:
    # 创建BeautifulSoup对象来解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到所有产品项的列表
    product_containers = soup.find_all('div', class_='card cartitem')

    for container in product_containers:
        # 对于每个产品，获取产品名称
        product_name = container.find('h5').get_text(strip=True)
        
        # 查找包含‘库存’文字的标签，假定库存信息在“库存：”之后
        stock_info_elem = container.find(string=lambda text: '库存' in text)
        stock_number_text = stock_info_elem.split('：')[-1].strip() if stock_info_elem else '0'  # 默认为0
        try:
            stock_number = int(stock_number_text.split(' ')[0])  # 从库存信息中提取数字部分并转换为整数
        except ValueError:
            stock_number = 0  # 如果转换失败，可能是库存文字后没有数字

        # 输出产品名称和库存
        print(f'产品名称: {product_name}')
        print(f'库存: {stock_number}')
        print('-------------------------')

        # 特定产品的库存判断
        if "免费Linux版本-NAT-30天" in product_name and stock_number > 0:
            send("仁源云监控库存", f"{product_name}：{stock_number}")
else:
    print('网页请求失败，状态码:', response.status_code)
