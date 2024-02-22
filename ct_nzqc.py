'''
cron: 36 9 * * *
new Env('哪吒汽车');
'''
import requests,json,random,time,os,datetime

from utils.utils import randomSleep,sha256encode,random_number
from notify import send
from utils.github_file_manager import GithubFileManager

title_name = '哪吒汽车'
appVersion = "6.0.0"
filepath = "/ql/data/env/nzqc.json"
appKey = 'e0ae89fb37b6151889c6de3ba6b84e0d3a67f52cd5767758d4186fefff8f763c'
sign_string = '8b53846c4eb40e3f58df334a2f2ca0af6fba86f7999afd0b2ba794edc450b937'
xiaoquan_openId_list = os.getenv("nz_xq").split('\n')

miScales2 = {"spuId": "1639094260312801281", "skuId": "1639094260384104450", "paymentPrice": 69, "stock": 0}
miHairDryer = {"spuId": "1747913042685448194", "skuId": "1747913042731585537", "paymentPrice": 88, "stock": 0}

debug = 0

def get_stock(goods):
    url = 'https://shop-wap.hozonauto.com/gateway/mallapi/goodsspu/detail/' + goods['spuId']
    headers = {
        'Host': 'shop-wap.hozonauto.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/119.0.6045.193 Mobile Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    if result['ok'] is True:
        stock = result['data']['skus'][0]['stock']
        skuId = result['data']['skuId']
        salesPrice = int(result['data']['salesPrice'])
        spuId = result['data']['skus'][0]['spuId']
        if stock > 0:
            goods['skuId'] = skuId
            goods['paymentPrice'] = salesPrice
            goods['stock'] = stock

def send_request(url, method='GET', **kwargs):
    attempt = 0
    MAX_RETRIES = 3  # 重试次数
    sleep_time = 30  # 重试等待时间
    time_out = 30  # 请求超时
    while attempt < MAX_RETRIES:
        try:
            method = method.upper()
            if method not in ['GET', 'POST', 'PUT']:
                raise ValueError(f'Unsupported HTTP method "{method}" provided.')
            response = requests.request(method, url, timeout=time_out, **kwargs)
            response.raise_for_status()
            if debug:
                print(response.json())
            return response.json()
        except requests.exceptions.Timeout as e:
            print(f"请求超时 (尝试 {attempt + 1}/{MAX_RETRIES}):", str(e))
        except requests.exceptions.RequestException as e:
            print(f"请求错误 (尝试 {attempt + 1}/{MAX_RETRIES}):", str(e))
        except ValueError as e:
            print(f"值错误 (尝试 {attempt + 1}/{MAX_RETRIES}):", str(e))
        except Exception as e:
            print(f"其他错误 (尝试 {attempt + 1}/{MAX_RETRIES}):", str(e))
        attempt += 1
        if attempt < MAX_RETRIES:
            time.sleep(sleep_time)
        else:
            print("超过最大重试次数")
            return None

# 刷新token
def refreshApiToken():
    url = 'https://appapi-pki.chehezhi.cn/customer/account/info/refreshApiToken'
    now = datetime.datetime.now()
    formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
    nonce = random_number(10)
    timestamp = int(time.time() * 1000)
    sign = f"POST%2Fcustomer%2Faccount%2Finfo%2FrefreshApiTokenappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}refreshtoken%3A{user['refresh_token']}{sign_string}"
    headers = {
        "Authorization": user['access_token'],
        "appId": "HOZON-B-xKrgEvMt",
        "appKey": appKey,
        "appVersion": appVersion,
        'login_channel': '1',
        'channel': 'android',
        "nonce": str(nonce),
        "phoneModel": "Redmi 22081212C",
        "timestamp": str(timestamp),
        "sign": sha256encode(sign),
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "appapi-pki.chehezhi.cn:18443"
    }
    data = {
        "refreshToken": user['refresh_token']
    }
    result = send_request(url, 'POST', headers=headers, data=data)
    if result is None:
        return False
    if result['success'] is True:
        print("刷新Authorization成功")
        user['access_token'] = result['data']['access_token']
        user['refresh_token'] = result['data']['refresh_token']
        user['token_time'] = str(formatted_time)
        return True
    else:
        print(result)
        send(f"哪吒token获取失败：{index}", result)
        return False

#签到
def sign():
    url = 'https://appapi-pki.chehezhi.cn/hznz/customer/sign'
    nonce = random_number(10)
    timestamp = int(time.time() * 1000)
    sign = f'GET%2Fhznz%2Fcustomer%2Fsignappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}{sign_string}'
    headers = {
        'appId': 'HOZON-B-xKrgEvMt',
        'appKey': appKey,
        'appVersion': appVersion,
        'login_channel': '1',
        'channel': 'android',
        'nonce': str(nonce),
        'phoneModel': 'Redmi 22081212C',
        'timestamp': str(timestamp),
        'sign': sha256encode(sign),
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 12; zh-cn; 22081212C Build/SKQ1.220303.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
        'Authorization': f"Bearer {user['access_token']}",
        'Host': 'appapi-pki.chehezhi.cn:18443',
        'Connection': 'Keep-Alive'
    }
    result = send_request(url, 'GET', headers=headers)
    if result is None:
        return None
    print(result['message'])
    if "积分" in result['message']:
        user['sign'] = True
        return 0
    elif result['message'] == "请不要重复签到":
        user['sign'] = True
        return 1
    else:
        print(result)
        send(f"哪吒签到失败：{index}", result)

# 转发  
def forwarArticle():
    url = 'https://appapi-pki.chehezhi.cn/hznz/app_article/forwarArticle'
    for i in range(5):
        articleId = random.choice(xiaoquan_openId_list)
        nonce = random_number(10)
        timestamp = int(time.time() * 1000)
        sign = f'PUT%2Fhznz%2Fapp_article%2FforwarArticleappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}{sign_string}'
        headers = {
            'Accept': 'application/json',
            'appId': 'HOZON-B-xKrgEvMt',
            'appKey': appKey,
            'appVersion': appVersion,
            'login_channel': '1',
            'channel': 'android',
            'nonce': str(nonce),
            'phoneModel': 'Redmi 22081212C',
            'timestamp': str(timestamp),
            'sign': sha256encode(sign),
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 12; zh-cn; 22081212C Build/SKQ1.220303.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
            'Authorization': f"Bearer {user['access_token']}",
            'Content-Type': 'application/json',
            'Content-Length': '48',
            'Host': 'appapi-pki.chehezhi.cn:18443',
            'Connection': 'Keep-Alive'
        }
        json_data = {
            'articleId': articleId,
            'forwardTo': '1'
        }
        result = send_request(url, 'PUT', headers=headers, json=json_data)
        if result is None:
            continue
        print(f"转发{articleId}：{result['message']}")
        if "转发成功" in result['message']:
            user['share'] = user['share'] + 1
        if user['share'] == 3:
            return
        time.sleep(random.randint(2, 6))
    send(f"哪吒转发失败：{index}", result)

#查询
def getCustomer():
    url = 'https://appapi-pki.chehezhi.cn/hznz/customer/getCustomer'
    nonce = random_number(10)
    timestamp = int(time.time() * 1000)
    sign = f'GET%2Fhznz%2Fcustomer%2FgetCustomerappid%3AHOZON-B-xKrgEvMtappkey%3A{appKey}nonce%3A{nonce}timestamp%3A{timestamp}{sign_string}'
    headers = {
        'appId': 'HOZON-B-xKrgEvMt',
        'appKey': appKey,
        'appVersion': appVersion,
        'login_channel': '1',
        'channel': 'android',
        'nonce': str(nonce),
        'phoneModel': 'Redmi 22081212C',
        'timestamp': str(timestamp),
        'sign': sha256encode(sign),
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 12; zh-cn; 22081212C Build/SKQ1.220303.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
        'Authorization': f"Bearer {user['access_token']}",
        'Host': 'appapi-pki.chehezhi.cn:18443',
        'Connection': 'Keep-Alive'
    }
    result = send_request(url, 'GET', headers=headers)
    if result is None:
        return
    if result['message'] == "成功":
        creditScore = result['data']['creditScore']
        phone = result['data']['phone']
        user['mobile'] = phone
        user['creditScore'] = creditScore
        print(f"{phone}：{creditScore}积分")
    else:
        print(result)
        send(f"哪吒查询失败：{index}", result)

# 查询限购
def orderinfo(goods):
    url = 'https://shop-wap.hozonauto.com/gateway/mallapi/orderinfo'
    headers = {
        'Host': 'shop-wap.hozonauto.com',
        'Content-Length': '279',
        'Authorization': f"Bearer {user['access_token']}",
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.144 Mobile Safari/537.36',
        'Content-Type': 'application/json',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    json_data = {
        "payType": "CASH",
        "deliveryWay": "1",
        "isRecommend": 0,
        "orderType": "0",
        "userAddressId": "",
        "userType": 0,
        "skus": [
            {
                "freightPrice": 0,
                "paymentPoints": 0,
                "paymentPointsPrice": 0,
                "paymentPrice": goods['paymentPrice'],
                "quantity": 1,
                "skuId": goods['skuId'],
                "spuId": goods['spuId']
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=json_data)
        result = response.json()
        print(result)
        if result['msg'] is None:
            return True
        else:
            return False
    except Exception as e:
        send(f"哪吒查询限购失败：{index}", result)
    return None

# 消息推送
def msg_send():
    msg = []
    msg_miScales2 = []
    msg_miHairDryer = []
    new_data_list = sorted(data_list, key=lambda x: x['creditScore'], reverse=True)#从大到小排序
    for new_data in new_data_list:
        phone = new_data['mobile']
        creditScore = new_data['creditScore']
        msg.append(f"{phone}：{creditScore}积分")
        if new_data['miScales2'] is True:
            msg_miScales2.append(phone)
        if new_data['miHairDryer'] is True:
            msg_miHairDryer.append(phone)
    print('\n'.join(msg))
    send("小米体重秤2", '\n'.join(msg_miScales2))
    time.sleep(60)
    send("小米吹风机", '\n'.join(msg_miHairDryer))

# github推送
def git_github():
    access_token = os.getenv('github_token')
    file_manager = GithubFileManager(access_token)
    repo_name = "inoyna12/updateTeam"
    branch = "master"
    file_path = "哪吒汽车/nzqc.json"
    new_content = data_list
    commit_message = f"Update {file_path}"
    file_manager.update_file_content(repo_name, file_path, new_content, commit_message, branch)

# 主线程
def main():
    if refreshApiToken() is False:
        return
    if user['sign'] is False:
        if sign() == 0:  #0：成功签到，1：重复签到
            forwarArticle()
    getCustomer()
    if miScales2['stock'] > 0 and user['creditScore'] >= 690 and user['miScales2'] is not False:
        user['miScales2'] = orderinfo(miScales2)
    if miHairDryer['stock'] > 0 and user['creditScore'] >= 880 and user['miHairDryer'] is not False:
        user['miHairDryer'] = orderinfo(miHairDryer)

if __name__ == '__main__':
    with open(filepath, 'r', encoding='utf-8') as f:
        data_list = json.load(f)
    print(f"共找到{len(data_list)}个账号")
    get_stock(miScales2)
    get_stock(miHairDryer)
    for index, user in enumerate(data_list, start = 1):
        print(f"\n{'-' * 13}正在执行第{index}/{len(data_list)}个账号{'-' * 13}")
        main()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_list, f)
        if index < len(data_list):
            randomSleep(10, 30)
    msg_send()
    git_github()
