'''
cron: 0 * * * *
new Env('ipv6动态域名解析');
'''

#https://dynv6.com/
#2235422323@qq.com
#Inoyna11

import requests

def get_ipv6():
    response = requests.get('https://api6.ipify.org/?format=json')
    if response.status_code == 200:
        ipv6 = response.json()['ip']
        print("当前IPv6地址:", ipv6)
        return ipv6
    else:
        print("无法获取 IPv6 地址！")
        return None

def update_dns_record(domain, ipv6, token):
    url = f'https://dynv6.com/api/update?hostname={domain}&ipv6={ipv6}&token={token}'
    response = requests.get(url)
    if response.status_code == 200:
        print("DNS 记录更新成功！")
    else:
        print("DNS 记录更新失败！")

# 填写要更新的信息
domain = 'inoyna.dynv6.net'
ipv6 = get_ipv6()
token = 'Dtj2BzhAxs6xTxMyxDryQucdLwS_V2'

if ipv6 is not None:
    # 调用函数更新 DNS 记录
    update_dns_record(domain, ipv6, token)
