'''
cron: 26 9 * * *
new Env('福域');
'''
import hashlib
import requests
import os
import json
import time
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
#print(f"==================脚本执行- 北京时间(UTC+8)：{time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}=====================\n")
from sendNotify import send
from os import environ

def rsa_encrypt(text, public_key):
    # 将Base64编码的公钥转换成RSA对象
    rsa_key = RSA.importKey(base64.b64decode(public_key))
    cipher = PKCS1_v1_5.new(rsa_key)
    # 对文本进行加密
    ciphertext = cipher.encrypt(text.encode('utf-8'))
    # 返回Base64编码的加密结果
    return base64.b64encode(ciphertext).decode()

def md5_encrypt(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest().upper()

def encrypt_data(data, key, iv):
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
    public_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDUUKw74ULuOMsQT9EO64Ij8y/DAgmW2JvbPIa7XTLibr0lfG7nnbXhnIWFwx1tfgG04P1jYZBHBVcvP7sVIWVvVDg8N43RErIu+kNCEMMfq22iUahKK1vi+y2bsXfVCa4SWS5eDegQOsuBfsP30HlcA4uvH3+/elFepv+6ep9ZmwIDAQAB'
    #解密seccode密钥
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
        print(result)
        time.sleep(5)
        if '点赞成功' in result['msg']:
            success_count += 1
            print(f"点赞{success_count}次成功！")     
        total_count += 1
    msg += f"点赞：{success_count}次！\n"
    print(msg)
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
    public_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDUUKw74ULuOMsQT9EO64Ij8y/DAgmW2JvbPIa7XTLibr0lfG7nnbXhnIWFwx1tfgG04P1jYZBHBVcvP7sVIWVvVDg8N43RErIu+kNCEMMfq22iUahKK1vi+y2bsXfVCa4SWS5eDegQOsuBfsP30HlcA4uvH3+/elFepv+6ep9ZmwIDAQAB'
    #解密seccode密钥
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
    print(result)
    msg += f"签到：{result['msg']}！\n"
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
    public_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDUUKw74ULuOMsQT9EO64Ij8y/DAgmW2JvbPIa7XTLibr0lfG7nnbXhnIWFwx1tfgG04P1jYZBHBVcvP7sVIWVvVDg8N43RErIu+kNCEMMfq22iUahKK1vi+y2bsXfVCa4SWS5eDegQOsuBfsP30HlcA4uvH3+/elFepv+6ep9ZmwIDAQAB'
    #解密seccode密钥
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
        print(result)
        time.sleep(5)
        if '操作成功' in result['msg']:
            success_count += 1
            print(f"分享资讯{success_count}次成功！")     
        total_count += 1
    msg += f"分享资讯：{success_count}次！\n"
    print(msg)
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
    public_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDUUKw74ULuOMsQT9EO64Ij8y/DAgmW2JvbPIa7XTLibr0lfG7nnbXhnIWFwx1tfgG04P1jYZBHBVcvP7sVIWVvVDg8N43RErIu+kNCEMMfq22iUahKK1vi+y2bsXfVCa4SWS5eDegQOsuBfsP30HlcA4uvH3+/elFepv+6ep9ZmwIDAQAB'
    #解密seccode密钥
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
        print(result)
        time.sleep(5)
        if '操作成功' in result['msg']:
            success_count += 1
            print(f"分享帖子{success_count}次成功！")     
        total_count += 1
    msg += f"分享帖子：{success_count}次！\n"
    print(msg)
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
    public_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDUUKw74ULuOMsQT9EO64Ij8y/DAgmW2JvbPIa7XTLibr0lfG7nnbXhnIWFwx1tfgG04P1jYZBHBVcvP7sVIWVvVDg8N43RErIu+kNCEMMfq22iUahKK1vi+y2bsXfVCa4SWS5eDegQOsuBfsP30HlcA4uvH3+/elFepv+6ep9ZmwIDAQAB'
    #解密seccode密钥
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
        print(result)
        time.sleep(10)
        if '操作成功' in result['msg']:
            success_count += 1
            print(f"评论|回复{success_count}次成功！")     
        total_count += 1
    msg += f"评论|回复：{success_count}次！\n"
    print(msg)
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
    public_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDUUKw74ULuOMsQT9EO64Ij8y/DAgmW2JvbPIa7XTLibr0lfG7nnbXhnIWFwx1tfgG04P1jYZBHBVcvP7sVIWVvVDg8N43RErIu+kNCEMMfq22iUahKK1vi+y2bsXfVCa4SWS5eDegQOsuBfsP30HlcA4uvH3+/elFepv+6ep9ZmwIDAQAB'
    #解密seccode密钥
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
    print(result)
    msg += f"发帖：{result['msg']}！\n"
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
        msg += qiandao(cookie)  
        msg += fatie(cookie)       
        msg += dianzan(cookie)   
        msg += zixun(cookie, userid)
        msg += tiezi(cookie, userid)
        msg += huifu(cookie)      
    #    msg += choujiang(cookie)
    #    msg += chaxun()
        time.sleep(5)
        index += 1
  #  print(msg)
    send('福域', msg)

