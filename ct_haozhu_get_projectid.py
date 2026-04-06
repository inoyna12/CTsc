import requests
import json,time,os

HOST = 'h5.haozhuma.cn'
haozhu_cookie = os.environ["haozhucookie"]
haozhu_projectname = os.environ["haozhu_projectname"]

def getid(name):
    url = f'https://{HOST}/api.php?type=30&gjc={name}'
    headers = {
        'Host': HOST,
        'User-Agent':'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36',
        'Cookie': haozhu_cookie
    }
    result = requests.get(url, headers=headers, allow_redirects=False).json()
    print(result)

getid(haozhu_projectname)
