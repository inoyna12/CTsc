'''
cron: 6 9 * * *
new Env('福域');
'''

import requests
import os
import json
import time
import random
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from sendNotify import send
from os import environ

contents_list = ["666", "不错", "不错不错", "无与伦比", "羡慕了", "真好啊", "真好", "赞一个", "6666666", "不错点赞", "不错哦", "支持一下", "说得好", "棒棒哒", "加油加油", "真的强", "真的很不错哦"]

def headers_new(content, timestamp, letters):
#    letters = get_random_letters()
    data = data_new(content, timestamp, letters)
    sign = sign_new(data, timestamp)
    body = body_new(content)
    seccode = seccode_new(timestamp, letters)
    headers = {
        'appVersion': '1.2.9',
        'os': 'Android',
        'loginChannel': 'baidu',
        'sign': sign,
        'body': body,
        'operatorName': 'yd',
        'networkState': 'mobile',
        'token': token,
        'osVersion': '12',
        'seccode': seccode,
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
    return headers, data
 
def activate():
    timestamp = (int(time.time() * 1000))
    letters = get_random_letters()
    content = '{"pageNo":1,"pageSize":20}'
    url = 'https://evosapi.changanford.cn/con/recommend/list'
    headers, data = headers_new(content, timestamp, letters)
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
#    print(result)
    return result['msg']

def signIn():
    print("\n【【【【【【【签到】】】】】】】\n")
    timestamp = (int(time.time() * 1000))
    letters = get_random_letters()
    content = '{}'
    url = 'https://evosapi.changanford.cn/user/signIn'
    headers, data = headers_new(content, timestamp, letters)
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
    print(result['msg'])

def addPosts():
    print("\n【【【【【【【发帖】】】】】】】\n")
    timestamp = (int(time.time() * 1000))
    letters = get_random_letters()
    pics, title = recommendPosts_a()
    print(f"\n封面：{pics}\n标题：{title}\n")
    content = f'{{"actionCode":"community_post","content":"","imgUrl":[],"isPublish":2,"pics":"{pics}","plate":2,"tagIds":"","title":"{title}","type":4}}'
    url = 'https://evosapi.changanford.cn/con/posts/addPosts'
    headers, data = headers_new(content, timestamp, letters)
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
#    print(result)
    result_data = decrypt_data(result['data'], timestamp, letters)
    print(result_data)

def actionLike():
    print("\n【【【【【【【点赞】】】】】】】\n")
    postsId_list = recommendPosts()
    success_count = 0
    total_count = 0
    while success_count < 5 and total_count < 8:
        timestamp = (int(time.time() * 1000))
        letters = get_random_letters()
        postsId = postsId_list.pop(0)
        content = f'{{"postsId":"{postsId}"}}'
        url = 'https://evosapi.changanford.cn/con/posts/actionLike'
        headers, data = headers_new(content, timestamp, letters)
        response = requests.post(url=url, headers=headers, data=data)
        result = response.json()
        print(f"点赞{postsId}：{result['msg']}")
        if '点赞成功' in result['msg']:
            success_count += 1
        total_count += 1
        if success_count < 5 and total_count < 8:
            random_sleep(2, 5)

def callback_post():
    print("\n【【【【【【分享帖子】】】】】】\n")
    bizId_list = recommendPosts()
    for i in range(3):
        timestamp_sec = (int(time.time()))
        timestamp = (int(time.time() * 1000))
        letters = get_random_letters()
        bizId = random.choice(bizId_list)
        content_a = f'{{"bizId":"2005056","content":"{{\\"bizId\\":\\"2005056\\",\\"shareImg\\":\\"ford-base-provider/2023/05/14/1684048349986androidios3000_4000.jpg\\",\\"shareTitle\\":\\"记录生活\\",\\"shareUrl\\":\\"https://evosh5.changanford.cn/common/?from=singlemessage&t=%s#/postDetail?postsId=2005056&jumpDataType=4&jumpDataValue=2005056\\",\\"type\\":\\"2\\"}}","device":"","shareTime":%s,"shareTo":"3","type":"2","userId":"{userid}"}}'
        content_b = content_a % (timestamp_sec, timestamp)
        content = content_b.replace('2005056', str(bizId))
        url = 'https://evosapi.changanford.cn/con/share/callback'
        headers, data = headers_new(content, timestamp, letters)
        response = requests.post(url=url, headers=headers, data=data)
        result = response.json()
#        print(result)
        msg = f"分享{bizId}：{result['msg']}"
        print(msg)
        if i < 2:
            random_sleep(2, 5)

def callback_information():
    print("\n【【【【【【分享资讯】】】】】】\n")
    bizId_list = discoverArticleList()
    for i in range(3):
        timestamp_sec = (int(time.time()))
        timestamp = (int(time.time() * 1000))
        letters = get_random_letters()
        bizId = random.choice(bizId_list)
        content_a = f'{{"bizId":1290,"content":"{{\\"bizId\\":1290,\\"shareDesc\\":\\"星耀福域5.19会员日玩法全新升级\\",\\"shareImg\\":\\"ford-manager/2023/04/28/f1a7c3250069408a97ac838e7c81160c.jpeg\\",\\"shareTitle\\":\\"FUN肆会员日 幸运大乐透 \\",\\"shareUrl\\":\\"https://evosh5.changanford.cn/common/?from=singlemessage&t=%s#/articleDetail?artId=1290&jumpDataType=2&jumpDataValue=1290\\",\\"type\\":1}}","device":"","shareTime":%s,"shareTo":"3","type":1,"userId":"{userid}"}}'
        content_b = content_a % (timestamp_sec, timestamp)
        content = content_b.replace('1290', str(bizId))
        url = 'https://evosapi.changanford.cn/con/share/callback'
        headers, data = headers_new(content, timestamp, letters)
        response = requests.post(url=url, headers=headers, data=data)
        result = response.json()
#        print(result)
        msg = f"分享{bizId}：{result['msg']}"
        print(msg)
        if i < 2:
            random_sleep(2, 5)

def addComment():
    print("\n【【【【【【【评论】】】】】】】\n")
    bizId_list = myPostsList()
    if len(bizId_list) > 0:
        for i in range(5):
            timestamp = (int(time.time() * 1000))
            letters = get_random_letters()
            bizId = random.choice(bizId_list)
            contents = random.choice(contents_list)
            content = f'{{"bizId":"{bizId}","content":"{contents}","groupId":"","phoneModel":"22081212C","pid":"0"}}'
            url = 'https://evosapi.changanford.cn/con/posts/addComment'
            headers, data = headers_new(content, timestamp, letters)
            response = requests.post(url=url, headers=headers, data=data)
            result = response.json()
        #    print(result)
            result_data = decrypt_data(result['data'], timestamp, letters)
            print(f"评论帖子：{bizId}，内容：{contents}\n{result_data}")
            if i < 4:
                random_sleep(2, 5)
    else:
        print("请发帖后做此任务")

def luckDraw():
    print("\n【【【【【签到7天抽奖】】】】】\n")
    timestamp = (int(time.time() * 1000))
    letters = get_random_letters()
    content = '{"activityId":"3"}'
    data = data_new(content, timestamp, letters)
    sign = sign_new(data, timestamp)
    seccode = seccode_new(timestamp, letters)
    url = 'https://evosapi.changanford.cn/luckyBlessingBag/luckDraw/3'
    headers = {
        'Host': 'evosapi.changanford.cn',
        'Connection': 'keep-alive',
        'seccode': seccode,
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/110.0.5481.153 Mobile Safari/537.36 AgentWeb/5.0.0  UCBrowser/11.6.4.950  ford-evos',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'timestamp': f"{timestamp}",
        'token': token,
        'sign': sign,
        'appVersion': '1.2.9',
        'Origin': 'https://evosh5.changanford.cn',
        'X-Requested-With': 'com.changanford.evos',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://evosh5.changanford.cn/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
    print(result['msg'])

def delete():
    print("\n【【【【【【【删贴】】】】】】】\n")
    postIds_list = myPostsList()
    for postIds in postIds_list:
        timestamp = (int(time.time() * 1000))
        letters = get_random_letters()
        content = f'{{"postIds":[{postIds}]}}'
        url = 'https://evosapi.changanford.cn/con/posts/delete'
        headers, data = headers_new(content, timestamp, letters)
        response = requests.post(url=url, headers=headers, data=data)
        result = response.json()
#        print(result)
#        result_data = decrypt_data(result['data'], timestamp, letters)
        print(f"删除帖子{postIds}：{result['msg']}")

def getAllTasks():
    print("\n【【【【【任务状态列表】】】】】\n")
    timestamp = (int(time.time() * 1000))
    letters = get_random_letters()
    content = '{}'
    url = 'https://evosapi.changanford.cn/userTask/getAllTasks'
    headers, data = headers_new(content, timestamp, letters)
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
#    print(result)
    result_data = decrypt_data(result['data'], timestamp, letters)
#    print(result_data)
    for item in result_data:
        for task in item['list']:
            # 如果是特殊任务（邀请新用户，预约试驾，车主认证）则跳过
            if task['taskName'] in ['完善资料', '绑定第三方账号', '首次加入圈子', '邀请新用户', '预约试驾', '车主认证']:
                continue
            # 输出符合条件的任务
            done = "已完成" if task['taskDoneCount'] == task['taskAllCount'] else "未完成"
            print("{} -- {}/{}，{}".format(task['taskName'], task['taskDoneCount'], task['taskAllCount'], done))

def myInfo():
    print("\n【【【【【【查询福币】】】】】】\n")
    timestamp = (int(time.time() * 1000))
    letters = get_random_letters()
    content = '{}'
    url = 'https://evosapi.changanford.cn/user/myInfo'
    headers, data = headers_new(content, timestamp, letters)
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
#    print(result)
    result_data = decrypt_data(result['data'], timestamp, letters)
#    print(result_data)
    Phone = result_data['phone'][:3] + "****" + result_data['phone'][7:]
    totalIntegral = result_data['ext']['totalIntegral']
    Phone_totalIntegral = f"{Phone}：{totalIntegral}福币\n"
    print(Phone_totalIntegral)
    return Phone_totalIntegral

def myPostsList():
    print("【查询自己帖子ID】")
    timestamp = (int(time.time() * 1000))
    letters = get_random_letters()
    content = f'{{"pageNo":1,"pageSize":"20","queryParams":{{"userId":"{userid}"}}}}'
    url = 'https://evosapi.changanford.cn/con/posts/myPostsList'
    headers, data = headers_new(content, timestamp, letters)
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
#    print(result)
    result_data = decrypt_data(result['data'], timestamp, letters)
#    print(result_data)
    postsId_list = []
    for item in result_data['dataList']:
        postsId_list.append(item['postsId'])
    print(postsId_list)
    return postsId_list 

def recommendPosts():
    print("【爬取推荐帖子】")
    timestamp = (int(time.time() * 1000))
    letters = get_random_letters()
    content = '{"pageNo":1,"pageSize":20,"queryParams":{"type":1,"viewType":1}}'
    url = 'https://evosapi.changanford.cn/con/community/recommendPosts'
    headers, data = headers_new(content, timestamp, letters)
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
    result_data = decrypt_data(result['data'], timestamp, letters)
#    print(result_data)
    postsId_list = []
    for item in result_data['dataList']:
        postsId_list.append(item['postsId'])
    print(postsId_list)
    return postsId_list

def recommendPosts_a():
    print("【爬取最新帖子】")
    timestamp = (int(time.time() * 1000))
    letters = get_random_letters()
    pageNo = random.randint(2, 100)
    content_a = '{"pageNo":50,"pageSize":5,"queryParams":{"type":2,"viewType":2}}'
    content = content_a.replace("50", str(pageNo))
    url = 'https://evosapi.changanford.cn/con/community/recommendPosts'
    headers, data = headers_new(content, timestamp, letters)
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
    result_data = decrypt_data(result['data'], timestamp, letters)
#    print(result_data)
#    postsId_list = []
    title_list = []
    pics_list = []
    for item in result_data['dataList']:
#        postsId_list.append(item['postsId'])
        title_list.append(item['title'])
        pics_list.append(item['pics'])
#    print(postsId_list)
    print(pics_list)
    print(title_list)
    return random.choice(pics_list), random.choice(title_list)

def discoverArticleList():
    print("【爬取资讯】")
    timestamp = (int(time.time() * 1000))
    letters = get_random_letters()
    content = '{"pageNo":2,"pageSize":10}'
    url = 'https://evosapi.changanford.cn/con/article/discoverArticleList'
    headers, data = headers_new(content, timestamp, letters)
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
    result_data = decrypt_data(result['data'], timestamp, letters)
#    print(result_data)
    artId_list = []
    for item in result_data['dataList']:
        artId_list.append(item['artId'])
    print(artId_list)
    return artId_list

#rsa加密
def rsa_encrypt(text, public_key):
    # 将Base64编码的公钥转换成RSA对象
    rsa_key = RSA.importKey(base64.b64decode(public_key))
    cipher = PKCS1_v1_5.new(rsa_key)
    # 对文本进行加密
    ciphertext = cipher.encrypt(text.encode('utf-8'))
    # 返回Base64编码的加密结果
    return base64.b64encode(ciphertext).decode()

#AES加密
def encrypt_AES(data, key, iv):
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
    return base64_encrypted_data

#md5值大写加密
def md5_encrypt(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest().upper()
   
def random_sleep(min_val, max_val):
    num = random.randint(min_val, max_val)
    print(f"等待{num}秒后继续>>>>>>>>>>>")
    time.sleep(num)

def get_random_letters():
    letters = [chr(random.randint(65, 90)) for _ in range(3)]
    return ''.join(letters)

def data_new(content, timestamp, letters):
    key = f'{timestamp}{letters}'.encode('utf-8')
    iv = f'{timestamp}{letters}'.encode('utf-8')
    content_aes = encrypt_AES(content, key, iv)
    content_encrypt = f'{{"paramEncr":"{content_aes}"}}'
    return content_encrypt

def sign_new(data, timestamp):
     data_str = f"{data}{timestamp}hyzh-unistar-8KWAKH291IpaFB"
     data_str_md5 = md5_encrypt(data_str)
     return data_str_md5

def body_new(content):
    content_md5 = md5_encrypt(content)
    return content_md5

def seccode_new(timestamp, letters):
    text = f'{timestamp}{letters}'
    public_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDUUKw74ULuOMsQT9EO64Ij8y/DAgmW2JvbPIa7XTLibr0lfG7nnbXhnIWFwx1tfgG04P1jYZBHBVcvP7sVIWVvVDg8N43RErIu+kNCEMMfq22iUahKK1vi+y2bsXfVCa4SWS5eDegQOsuBfsP30HlcA4uvH3+/elFepv+6ep9ZmwIDAQAB'
#解密seccode密钥
    text_rsa = rsa_encrypt(text, public_key)
    return text_rsa

def decrypt_data(data, timestamp, letters):#aes解密
    key = f'{timestamp}{letters}'.encode('utf-8')
    iv = f'{timestamp}{letters}'.encode('utf-8')
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
    
def ql_env():
    if "FYtoken" in os.environ:
        token_list = os.environ['FYtoken'].split('\n')
        if len(token_list) > 0:
            return token_list
        else:
            print("变量未启用")
            sys.exit(1)
    else:
        print("未添加变量")
        sys.exit(0)

if __name__ == '__main__':
    msg = ""
    index = 0
    quantity = ql_env()
    print (f"共找到{len(quantity)}个账号")
    for token in quantity:
        userid = token.split(':')[3]
        print (f"------------正在执行第{index + 1}个账号----------------")
#        msg += f"第{index + 1}个账号运行结果: \n"
        if activate() == '操作成功':
            signIn()
            addPosts()
            actionLike()
            callback_post()
            callback_information()
            addComment()
            luckDraw()
            delete()
            getAllTasks()
            msg += myInfo()
            print(f"第{index + 1}个账号运行完成\n")
        else:
            msg += "token失效或脚本待更新\n" 
        index += 1
        if index < len(quantity):
            random_sleep(30, 60)
#    print(msg)
    send('福域', msg)
