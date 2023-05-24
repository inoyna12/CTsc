'''
cron: 26 9 * * *
new Env('福域');
'''
import hashlib
import requests
import random
import os
import json
import time
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
#print(f"==================脚本执行- 北京时间(UTC+8)：{time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}=====================\n")
from sendNotify import send
from os import environ

public_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDUUKw74ULuOMsQT9EO64Ij8y/DAgmW2JvbPIa7XTLibr0lfG7nnbXhnIWFwx1tfgG04P1jYZBHBVcvP7sVIWVvVDg8N43RErIu+kNCEMMfq22iUahKK1vi+y2bsXfVCa4SWS5eDegQOsuBfsP30HlcA4uvH3+/elFepv+6ep9ZmwIDAQAB'
#解密seccode密钥

def random_sleep(min_val, max_val):
    num = random.randint(min_val, max_val)
    print(f"等待{num}秒后继续>>>>>>>>>>>")
    time.sleep(num)
    return num  

def decrypt_data(data, key, iv):#aes解密
    # 将Base64编码的数据解码为二进制格式
    encrypted_data = base64.b64decode(data)
    # 创建AES解密器
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 对数据进行解密
    decrypted_data = cipher.decrypt(encrypted_data)
    # 使用PKCS7Padding方式进行去位
    unpadded_data = unpad(decrypted_data, AES.block_size, style='pkcs7')
    # 将字节转换为字符串，并删除多余的空格
    decrypted_str = unpadded_data.decode('utf-8').strip()
    # 将JSON字符串转换为字典并返回
    decrypted_data = json.loads(decrypted_str)
    return decrypted_data

def rsa_encrypt(text, public_key):#rsa加密
    # 将Base64编码的公钥转换成RSA对象
    rsa_key = RSA.importKey(base64.b64decode(public_key))
    cipher = PKCS1_v1_5.new(rsa_key)
    # 对文本进行加密
    ciphertext = cipher.encrypt(text.encode('utf-8'))
    # 返回Base64编码的加密结果
    return base64.b64encode(ciphertext).decode()

def md5_encrypt(string):#md5值大写加密
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest().upper()

def encrypt_data(data, key, iv):#aes加密
    # 将字典转换为字符串
    data_str = str(data)
    # 将字符串转换为UTF-8编码格式的字节
    data_bytes = data_str.encode('utf-8')
    # 使用PKCS7Padding方式进行补位
    padded_data = pad(data_bytes, AES.block_size, style='pkcs7')
    # 创建AES加密器
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 对数据进行加密
    encrypted_data = cipher.encrypt(padded_data)
    # 对加密后的数据进行Base64编码
    base64_encrypted_data = base64.b64encode(encrypted_data).decode('utf-8')
    sign_1 = '{"paramEncr":"paramEncr_1"}'
    new_str = sign_1.replace('"paramEncr_1"', f'"{base64_encrypted_data}"')
    return new_str
  
def dianzan(cookie):
    timestamp = str(int(time.time() * 1000))
    msg = ""
    sign = '{"postsId":"2005056"}'
    #sign明文内容，5338账号第一个帖子明文id
    key = f'{timestamp}XLK'.encode('utf-8')
    iv = f'{timestamp}XLK'.encode('utf-8')
    text = f'{timestamp}XLK'
    #当前系统时间戳
    sign_aes = encrypt_data(sign, key, iv)
    #帖子明文+时间戳通过AES加密
    sign_aes_time = sign_aes + f"{timestamp}hyzh-unistar-8KWAKH291IpaFB"
    #AES加密后加上当前系统时间戳等参数
    sign_aes_time_md5 = md5_encrypt(sign_aes_time)
    #加上当前系统时间戳等参数后转换成md5值，sign加密完成
    body_md5 = md5_encrypt(sign)
    #将帖子明文id转换成md5值，body加密完成
    seccode_rsa = rsa_encrypt(text, public_key)
    #当前系统时间戳+解密seccode密钥使用rsa加密，seccode加密完成
    url = 'https://evosapi.changanford.cn/con/posts/actionLike'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': sign_aes_time_md5,
        'body': body_md5,
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': seccode_rsa,
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': f"{timestamp}",
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'ford-evos',
    }
    data = sign_aes
    success_count = 0 # 记录成功次数
    total_count = 0   # 记录总共尝试次数
    while success_count < 5 and total_count < 12:
        response = requests.post(url=url, headers=headers, data=data)
        result = response.json()
#        print(result)
        if '点赞成功' in result['msg']:
            success_count += 1
            print(f"点赞{success_count}次成功")     
        total_count += 1
        if success_count < 5 and total_count < 12:
            random_sleep(30, 50)
    msg += f"点赞：{success_count}次\n"
    return msg

def qiandao(cookie):
    timestamp = str(int(time.time() * 1000))
    msg = ""
    sign = '{}'
    #sign签到明文内容
    key = f'{timestamp}XLK'.encode('utf-8')
    iv = f'{timestamp}XLK'.encode('utf-8')
    text = f'{timestamp}XLK'
    #当前系统时间戳
    sign_aes = encrypt_data(sign, key, iv)
    #帖子明文+时间戳通过AES加密
    sign_aes_time = sign_aes + f"{timestamp}hyzh-unistar-8KWAKH291IpaFB"
    #AES加密后加上当前系统时间戳等参数
    sign_aes_time_md5 = md5_encrypt(sign_aes_time)
    #加上当前系统时间戳等参数后转换成md5值，sign加密完成
    body_md5 = md5_encrypt(sign)
    #将sign明文转换成md5值，body加密完成
    seccode_rsa = rsa_encrypt(text, public_key)
    #当前系统时间戳+解密seccode密钥使用rsa加密，seccode加密完成
    url = 'https://evosapi.changanford.cn/user/signIn'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': sign_aes_time_md5,
        'body': body_md5,
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': seccode_rsa,
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': f"{timestamp}",
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'ford-evos',
    }
    data = sign_aes
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
#    print(result)
    msg += f"签到：{result['msg']}\n"
    print(msg)
    return msg
    
def zixun(cookie, userid):
    timestamp_sec = str(int(time.time()))
    timestamp = str(int(time.time() * 1000))
    msg = ""
    sign_1 = f'{{"bizId":1222,"content":"{{\\"bizId\\":1222,\\"shareDesc\\":\\"星耀福域5.19会员日玩法全新升级\\",\\"shareImg\\":\\"ford-manager/2023/04/28/f1a7c3250069408a97ac838e7c81160c.jpeg\\",\\"shareTitle\\":\\"FUN肆会员日 幸运大乐透 \\",\\"shareUrl\\":\\"https://evosh5.changanford.cn/common/?from=singlemessage&t=%s#/articleDetail?artId=1222&jumpDataType=2&jumpDataValue=1222\\",\\"type\\":1}}","device":"","shareTime":%s,"shareTo":"3","type":1,"userId":"{userid}"}}'
    #sign签到明文内容，最后是用户id
    sign = sign_1 % (timestamp_sec, timestamp)
    #替换sign明文内容中的时间戳，10位和13位
    key = f'{timestamp}XLK'.encode('utf-8')
    iv = f'{timestamp}XLK'.encode('utf-8')
    text = f'{timestamp}XLK'
    #当前系统时间戳
    sign_aes = encrypt_data(sign, key, iv)
    #帖子明文+时间戳通过AES加密
    sign_aes_time = sign_aes + f"{timestamp}hyzh-unistar-8KWAKH291IpaFB"
    #AES加密后加上当前系统时间戳等参数
    sign_aes_time_md5 = md5_encrypt(sign_aes_time)
    #加上当前系统时间戳等参数后转换成md5值，sign加密完成
    body_md5 = md5_encrypt(sign)
    #将sign明文转换成md5值，body加密完成
    seccode_rsa = rsa_encrypt(text, public_key)
    #当前系统时间戳+解密seccode密钥使用rsa加密，seccode加密完成
    url = 'https://evosapi.changanford.cn/con/share/callback'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': sign_aes_time_md5,
        'body': body_md5,
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': seccode_rsa,
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': f"{timestamp}",
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'ford-evos',
    }
    data = sign_aes
    success_count = 0 # 记录成功次数
    total_count = 0   # 记录总共尝试次数
    while success_count < 3 and total_count < 5:
        response = requests.post(url=url, headers=headers, data=data)
        result = response.json()
#        print(result)
        if '操作成功' in result['msg']:
            success_count += 1
            print(f"分享资讯{success_count}次成功")     
        total_count += 1
        if success_count < 3 and total_count < 5:
            random_sleep(30, 60)
    msg += f"分享资讯：{success_count}次\n"
    return msg
    
def tiezi(cookie, userid):
    timestamp_sec = str(int(time.time()))
    timestamp = str(int(time.time() * 1000))
    msg = ""
    sign_1 = f'{{"bizId":"2005056","content":"{{\\"bizId\\":\\"2005056\\",\\"shareImg\\":\\"ford-base-provider/2023/05/14/1684048349986androidios3000_4000.jpg\\",\\"shareTitle\\":\\"记录生活\\",\\"shareUrl\\":\\"https://evosh5.changanford.cn/common/?from=singlemessage&t=%s#/postDetail?postsId=2005056&jumpDataType=4&jumpDataValue=2005056\\",\\"type\\":\\"2\\"}}","device":"","shareTime":%s,"shareTo":"3","type":"2","userId":"{userid}"}}'
    #sign明文内容，最后是用户id
    sign = sign_1 % (timestamp_sec, timestamp)
    #替换sign明文内容中的时间戳，10位和13位
    key = f'{timestamp}XLK'.encode('utf-8')
    iv = f'{timestamp}XLK'.encode('utf-8')
    text = f'{timestamp}XLK'
    #当前系统时间戳
    sign_aes = encrypt_data(sign, key, iv)
    #帖子明文+时间戳通过AES加密
    sign_aes_time = sign_aes + f"{timestamp}hyzh-unistar-8KWAKH291IpaFB"
    #AES加密后加上当前系统时间戳等参数
    sign_aes_time_md5 = md5_encrypt(sign_aes_time)
    #加上当前系统时间戳等参数后转换成md5值，sign加密完成
    body_md5 = md5_encrypt(sign)
    #将sign明文转换成md5值，body加密完成
    seccode_rsa = rsa_encrypt(text, public_key)
    #当前系统时间戳+解密seccode密钥使用rsa加密，seccode加密完成
    url = 'https://evosapi.changanford.cn/con/share/callback'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': sign_aes_time_md5,
        'body': body_md5,
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': seccode_rsa,
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': f"{timestamp}",
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'ford-evos',
    }
    data = sign_aes
    success_count = 0 # 记录成功次数
    total_count = 0   # 记录总共尝试次数
    while success_count < 3 and total_count < 5:
        response = requests.post(url=url, headers=headers, data=data)
        result = response.json()
#        print(result)
        if '操作成功' in result['msg']:
            success_count += 1
            print(f"分享帖子{success_count}次成功")     
        total_count += 1
        if success_count < 3 and total_count < 5:
            random_sleep(30, 60)
    msg += f"分享帖子：{success_count}次\n"
    return msg
    
def huifu(cookie):
    timestamp = str(int(time.time() * 1000))
    msg = ""
    sign = '{"bizId":"2005056","content":"666","groupId":"","phoneModel":"22081212C","pid":"0"}'
    #sign明文内容，回复5338第一个帖子，内容666
    key = f'{timestamp}XLK'.encode('utf-8')
    iv = f'{timestamp}XLK'.encode('utf-8')
    text = f'{timestamp}XLK'
    #当前系统时间戳
    sign_aes = encrypt_data(sign, key, iv)
    #帖子明文+时间戳通过AES加密
    sign_aes_time = sign_aes + f"{timestamp}hyzh-unistar-8KWAKH291IpaFB"
    #AES加密后加上当前系统时间戳等参数
    sign_aes_time_md5 = md5_encrypt(sign_aes_time)
    #加上当前系统时间戳等参数后转换成md5值，sign加密完成
    body_md5 = md5_encrypt(sign)
    #将sign明文转换成md5值，body加密完成
    seccode_rsa = rsa_encrypt(text, public_key)
    #当前系统时间戳+解密seccode密钥使用rsa加密，seccode加密完成
    url = 'https://evosapi.changanford.cn/con/posts/addComment'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': sign_aes_time_md5,
        'body': body_md5,
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': seccode_rsa,
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': f"{timestamp}",
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'ford-evos',
    }
    data = sign_aes
    success_count = 0 # 记录成功次数
    total_count = 0   # 记录总共尝试次数
    while success_count < 5 and total_count < 6:
        response = requests.post(url=url, headers=headers, data=data)
        result = response.json()
#        print(result)
        if '操作成功' in result['msg']:
            success_count += 1
            print(f"评论|回复{success_count}次成功")     
        total_count += 1
        if success_count < 5 and total_count < 6:
            random_sleep(40, 60)
    msg += f"评论|回复：{success_count}次\n"
    return msg

def fatie(cookie):
    timestamp = str(int(time.time() * 1000))
    msg = ""
    sign = '{"actionCode":"community_post","addrName":"","address":"","circleId":"","city":"","cityCode":"","content":"","imgUrl":[{"imgDesc":"每天一杯奶茶，提神又醒脑","imgUrl":""}],"isPublish":2,"keywords":"","lat":0,"lon":0,"pics":"temp/2023/05/15/1684108775599androidios3000_4000.jpg","plate":2,"province":"","tagIds":"","title":"记录生活","topicId":"","type":"4"}'
    #sign发帖明文内容
    key = f'{timestamp}XLK'.encode('utf-8')
    iv = f'{timestamp}XLK'.encode('utf-8')
    text = f'{timestamp}XLK'
    #当前系统时间戳
    sign_aes = encrypt_data(sign, key, iv)
    #帖子明文+时间戳通过AES加密
    sign_aes_time = sign_aes + f"{timestamp}hyzh-unistar-8KWAKH291IpaFB"
    #AES加密后加上当前系统时间戳等参数
    sign_aes_time_md5 = md5_encrypt(sign_aes_time)
    #加上当前系统时间戳等参数后转换成md5值，sign加密完成
    body_md5 = md5_encrypt(sign)
    #将sign明文转换成md5值，body加密完成
    seccode_rsa = rsa_encrypt(text, public_key)
    #当前系统时间戳+解密seccode密钥使用rsa加密，seccode加密完成
    url = 'https://evosapi.changanford.cn/con/posts/addPosts'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': sign_aes_time_md5,
        'body': body_md5,
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': seccode_rsa,
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': f"{timestamp}",
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'ford-evos',
    }
    data = sign_aes
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
#    print(result)
    msg += f"发帖：{result['msg']}\n"
    print(msg)
    return msg
    
def chaxun(cookie):
    timestamp = str(int(time.time() * 1000))
    msg = ""
    sign = '{}'
    #sign查询明文内容
    key = f'{timestamp}XLK'.encode('utf-8')
    iv = f'{timestamp}XLK'.encode('utf-8')
    text = f'{timestamp}XLK'
    #当前系统时间戳
    sign_aes = encrypt_data(sign, key, iv)
    #帖子明文+时间戳通过AES加密
    sign_aes_time = sign_aes + f"{timestamp}hyzh-unistar-8KWAKH291IpaFB"
    #AES加密后加上当前系统时间戳等参数
    sign_aes_time_md5 = md5_encrypt(sign_aes_time)
    #加上当前系统时间戳等参数后转换成md5值，sign加密完成
    body_md5 = md5_encrypt(sign)
    #将sign明文转换成md5值，body加密完成
    #解密seccode密钥
    seccode_rsa = rsa_encrypt(text, public_key)
    #当前系统时间戳+解密seccode密钥使用rsa加密，seccode加密完成
    url = 'https://evosapi.changanford.cn/user/myInfo'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': sign_aes_time_md5,
        'body': body_md5,
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': seccode_rsa,
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': f"{timestamp}",
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'ford-evos',
    }
    data = sign_aes
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
    result_data = result['data']
    #返回需要解密的内容
    result_data_res = decrypt_data(result_data, key, iv)
    #返回解密内容
#    print(result_data_res)
    phone = result_data_res['phone']
    Phone = phone[:3] + "****" + phone[7:]
    totalIntegral = result_data_res['ext']['totalIntegral']
    msg += f"{Phone}，福币：{totalIntegral}\n\n"
    print(msg)
    return msg

def jihuo(cookie):
    timestamp = str(int(time.time() * 1000))
    sign = '{"pageNo":1,"pageSize":20}'
    #sign明文内容
    key = f'{timestamp}XLK'.encode('utf-8')
    iv = f'{timestamp}XLK'.encode('utf-8')
    text = f'{timestamp}XLK'
    #当前系统时间戳
    sign_aes = encrypt_data(sign, key, iv)
    #帖子明文+时间戳通过AES加密
    sign_aes_time = sign_aes + f"{timestamp}hyzh-unistar-8KWAKH291IpaFB"
    #AES加密后加上当前系统时间戳等参数
    sign_aes_time_md5 = md5_encrypt(sign_aes_time)
    #加上当前系统时间戳等参数后转换成md5值，sign加密完成
    body_md5 = md5_encrypt(sign)
    #将sign明文转换成md5值，body加密完成
    seccode_rsa = rsa_encrypt(text, public_key)
    #当前系统时间戳+解密seccode密钥使用rsa加密，seccode加密完成
    url = 'https://evosapi.changanford.cn/con/recommend/list'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': sign_aes_time_md5,
        'body': body_md5,
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': seccode_rsa,
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': f"{timestamp}",
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'ford-evos',
    }
    data = sign_aes
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
    if result['msg'] == '操作成功':
        print("激活成功")
#    print(result)
    return result['msg']

def tieziID(cookie, userid):
    timestamp = str(int(time.time() * 1000))
    sign = f'{{"pageNo":1,"pageSize":"20","queryParams":{{"userId":"{userid}"}}}}'
    #sign查询明文内容
    key = f'{timestamp}XLK'.encode('utf-8')
    iv = f'{timestamp}XLK'.encode('utf-8')
    text = f'{timestamp}XLK'
    #当前系统时间戳
    sign_aes = encrypt_data(sign, key, iv)
    #帖子明文+时间戳通过AES加密
    sign_aes_time = sign_aes + f"{timestamp}hyzh-unistar-8KWAKH291IpaFB"
    #AES加密后加上当前系统时间戳等参数
    sign_aes_time_md5 = md5_encrypt(sign_aes_time)
    #加上当前系统时间戳等参数后转换成md5值，sign加密完成
    body_md5 = md5_encrypt(sign)
    #将sign明文转换成md5值，body加密完成
    #解密seccode密钥
    seccode_rsa = rsa_encrypt(text, public_key)
    #当前系统时间戳+解密seccode密钥使用rsa加密，seccode加密完成
    url = 'https://evosapi.changanford.cn/con/posts/myPostsList'
    headers = {
        'appVersion': '1.2.7',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': sign_aes_time_md5,
        'body': body_md5,
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': cookie,
        'osVersion': '12',
        'seccode': seccode_rsa,
        'model': '22081212C',
        'brand': 'Xiaomi',
        'timestamp': f"{timestamp}",
        'codelab': 'codelabs',
        'Content-Type': 'application/json',
        'Host': 'evosapi.changanford.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'ford-evos',
    }
    data = sign_aes
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
    result_data = result['data']
    #返回需要解密的内容
    result_data_res = decrypt_data(result_data, key, iv)
    #返回解密内容
#    print(result_data_res)
    posts_id_list = []
    for item in result_data_res['dataList']:
        posts_id_list.append(item['postsId'])
    print('帖子ID:', posts_id_list)
    if 2005056 in posts_id_list:
        posts_id_list.remove(2005056)
#        print('去除帖子ID2005056:', posts_id_list)
#    else:
#        print('帖子ID:', posts_id_list)
    return posts_id_list

def deleteID(cookie):
    tieID = tieziID(cookie, userid)
    b = '{"postIds":[2006594]}'
    b_dict = json.loads(b)
    for item in tieID:
        new_b = b_dict.copy()
        new_b["postIds"] = [item]
        sign = json.dumps(new_b)
        print(sign)
        timestamp = str(int(time.time() * 1000))
        key = f'{timestamp}XLK'.encode('utf-8')
        iv = f'{timestamp}XLK'.encode('utf-8')
        text = f'{timestamp}XLK'
        #当前系统时间戳
        sign_aes = encrypt_data(sign, key, iv)
        #帖子明文+时间戳通过AES加密
        sign_aes_time = sign_aes + f"{timestamp}hyzh-unistar-8KWAKH291IpaFB"
        #AES加密后加上当前系统时间戳等参数
        sign_aes_time_md5 = md5_encrypt(sign_aes_time)
        #加上当前系统时间戳等参数后转换成md5值，sign加密完成
        body_md5 = md5_encrypt(sign)
        #将sign明文转换成md5值，body加密完成
        seccode_rsa = rsa_encrypt(text, public_key)
        #当前系统时间戳+解密seccode密钥使用rsa加密，seccode加密完成
        url = 'https://evosapi.changanford.cn/con/posts/delete'
        headers = {
            'appVersion': '1.2.7',
            'os': 'Android',
            'loginChannel': 'baidu',
            'sign': sign_aes_time_md5,
            'body': body_md5,
            'operatorName': 'yd',
            'networkState': 'mobile',
            'token': cookie,
            'osVersion': '12',
            'seccode': seccode_rsa,
            'model': '22081212C',
            'brand': 'Xiaomi',
            'timestamp': f"{timestamp}",
            'codelab': 'codelabs',
            'Content-Type': 'application/json',
            'Host': 'evosapi.changanford.cn',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'ford-evos',
        }
        data = sign_aes
        response = requests.post(url=url, headers=headers, data=data)
        result = response.json()
        print(f"删除帖子{item}：{result['msg']}")

def choujiang(cookie):
    timestamp = str(int(time.time() * 1000))
    msg = ""
    sign = '{"activityId":"3"}'
    #sign明文内容
    key = f'{timestamp}XLK'.encode('utf-8')
    iv = f'{timestamp}XLK'.encode('utf-8')
    text = f'{timestamp}XLK'
    #当前系统时间戳
    sign_aes = encrypt_data(sign, key, iv)
    #帖子明文+时间戳通过AES加密
    sign_aes_time = sign_aes + f"{timestamp}hyzh-unistar-8KWAKH291IpaFB"
    #AES加密后加上当前系统时间戳等参数
    sign_aes_time_md5 = md5_encrypt(sign_aes_time)
    #加上当前系统时间戳等参数后转换成md5值，sign加密完成
    body_md5 = md5_encrypt(sign)
    #将sign明文转换成md5值，body加密完成
    seccode_rsa = rsa_encrypt(text, public_key)
    #当前系统时间戳+解密seccode密钥使用rsa加密，seccode加密完成
    url = 'https://evosapi.changanford.cn/luckyBlessingBag/luckDraw/3'
    headers = {
        'Host': 'evosapi.changanford.cn',
        'Connection': 'keep-alive',
        'seccode': seccode_rsa,
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36 AgentWeb/5.0.0  UCBrowser/11.6.4.950  ford-evos',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'timestamp': f"{timestamp}",
        'token': cookie,
        'sign': sign_aes_time_md5,
        'appVersion': '1.2.7',
        'Origin': 'https://evosh5.changanford.cn',
        'X-Requested-With': 'com.changanford.evos',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://evosh5.changanford.cn/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    data = sign_aes
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json() 
    print(result)
    if result['msg'] == '操作成功':
        msg += f"签到7天抽奖：{result['msg']}\n"
        print(msg)
        return msg
         
def ql_env():
    if "FYtoken" in os.environ:
        token_list = os.environ['FYtoken'].split('\n')
        if len(token_list) > 0:
            return token_list
        else:
            print("FYtoken变量未启用")
            sys.exit(1)
    else:
        print("未添加FYtoken变量")
        sys.exit(0)

if __name__ == '__main__':
    msg = ""
    index = 1
    quantity = ql_env()
    print (f"共找到{len(quantity)}个账号")
    for cookie in quantity:
        userid = cookie.split(':')[3]
        print(f"------------正在执行第{index}个账号----------------")
        msg += f"第{str(index)}个账号运行结果: \n"
        activate = jihuo(cookie)
        if activate == '操作成功':
            print("签到")
            msg += qiandao(cookie) 
            print("发帖")
            random_sleep(30, 60) 
            msg += fatie(cookie)
            print("点赞")
            random_sleep(30, 60) 
            msg += dianzan(cookie)
            print("分享资讯")
            random_sleep(30, 60)
            msg += zixun(cookie, userid)
            print("分享帖子")
            random_sleep(30, 60)
            msg += tiezi(cookie, userid)
            print("回复帖子")
            random_sleep(30, 60)
            msg += huifu(cookie)
            print("删除帖子")
            random_sleep(10, 20)
            deleteID(cookie)
            print("签到7天抽奖")
            msg += choujiang(cookie)
            print("查询")
            msg += chaxun(cookie)
            print(f"第{str(index)}个账号运行完成")
        elif activate != '操作成功':
            msg += "token失效或脚本待更新\n"
        index += 1
    send('福域', msg)
