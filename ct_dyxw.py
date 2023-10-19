'''
cron: 36 12 * * *
new Env('笛杨新闻');
'''
import requests,os,json,time,random,datetime,sys
import urllib,uuid,hashlib
from sendNotify import send

version = '3.0.2'
not_task = ['邀请好友']

def random_sleep(min_val, max_val):
    num = random.randint(min_val, max_val)
    print(f"等待{num}秒后继续>>>>>>>>>>>")
    time.sleep(num)

def ql_env(name):
    if name in os.environ:
        token_list = os.environ[name].split('\n')
        if len(token_list) > 0:
            return token_list
        else:
            print("变量未启用" + name)
            sys.exit(1)
    else:
        print("未添加变量" + name)
        sys.exit(0)

def timestamp_ct(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp // 1000)
    current_date = datetime.datetime.now().date()
    dt_date = dt.date()
    if dt_date == current_date:
        print(f"{dt_date}：{current_date}----加入")
        return True
    else:
        print(f"{dt_date}_{current_date}----不加入")
        return False

def format_timestamp(timestamp):
    timestamp_sec = timestamp / 1000
    dt = datetime.datetime.fromtimestamp(timestamp_sec)
    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

def random_ua():
    random_uuid = str(uuid.uuid4())
    ua_uuid = "00000000" + random_uuid[8:][:11] + "0000" + random_uuid[23] + "0000" + random_uuid[28:]
    UA = f"{version};{ua_uuid};Xiaomi 22081212C;Android;12;Release"
    return UA

def sha256(string):
    hash_object = hashlib.sha256(string.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig
    
def random_uuid():
    random_uuid = str(uuid.uuid4())
    return random_uuid

def account_comment():
    print("【遍历个人评论】")
    url = 'https://vapp.tmuyun.com/api/account_comment/comment_list?size=20'
    requestid = random_uuid()
    timestamp = (int(time.time() * 1000))
    signature = f"/api/account_comment/comment_list&&{session}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
    headers = {
        "X-SESSION-ID": session,
        "X-REQUEST-ID": requestid,
        "X-TIMESTAMP": str(timestamp),
        "X-SIGNATURE": sha256(signature),
        "X-TENANT-ID": "68",
        "User-Agent": random_ua(),
        "Host": "vapp.tmuyun.com"
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    comment_list = []
    if result['message'] == "success":
        for item in result['data']['comment_list']:
            comment_list.append(item['id'])
    print(comment_list)
    return comment_list
        
def delete():
    print("【删除评论】")
    comment_list = account_comment()
    url = 'https://vapp.tmuyun.com/api/comment/delete'
    for comment_id in comment_list:
        requestid = random_uuid()
        timestamp = (int(time.time() * 1000))
        signature = f"/api/comment/delete&&{session}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
        headers = {
            "X-SESSION-ID": session,
            "X-REQUEST-ID": requestid,
            "X-TIMESTAMP": str(timestamp),
            "X-SIGNATURE": sha256(signature),
            "X-TENANT-ID": "68",
            "User-Agent": random_ua(),
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "35",
            "Host": "vapp.tmuyun.com"
        }
        data = f"comment_id={comment_id}"
        response = requests.post(url, headers=headers, data=data)
        result = response.json()
        print(f"删除{comment_id}：{result['message']}")

#签到
def sign():
    url = 'https://vapp.tmuyun.com/api/user_mumber/sign'
    requestid = random_uuid()
    timestamp = (int(time.time() * 1000))
    signature = f"/api/user_mumber/sign&&{session}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
    headers = {
        "X-SESSION-ID": session,
        "X-REQUEST-ID": requestid,
        "X-TIMESTAMP": str(timestamp),
        "X-SIGNATURE": sha256(signature),
        "X-TENANT-ID": "68",
        "User-Agent": random_ua(),
        "Host": "vapp.tmuyun.com"
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    if result['message'] == "success":
        print(f"签到：{result['data']['reason']}，获得：积分{result['data']['signIntegral']}，经验{result['data']['signExperience']}")
    
#阅读
def detail(inx):
    if len(id_list) < 10:
        print("id_list数量不足，不进行此任务", len(id_list))
        return
    detail_id_list = list(id_list)
    url = 'https://vapp.tmuyun.com/api/article/detail'
    for i in range(inx):
        id = random.choice(detail_id_list)
        detail_id_list.remove(id)
        params = {
            'id': id
        }
        requestid = random_uuid()
        timestamp = (int(time.time() * 1000))
        signature = f"/api/article/detail&&{session}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
        headers = {
            "X-SESSION-ID": session,
            "X-REQUEST-ID": requestid,
            "X-TIMESTAMP": str(timestamp),
            "X-SIGNATURE": sha256(signature),
            "X-TENANT-ID": "68",
            "User-Agent": random_ua(),
            "Host": "vapp.tmuyun.com",
            "Connection": "Keep-Alive"
        }
        timeout = random.randint(11, 15)
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        result = response.json()
        print(f"阅读{id}：{result['message']}")
        random_sleep(timeout + 1, timeout + 3)

#点赞
def like(inx):
    if len(id_list) < 10:
        print("id_list数量不足，不进行此任务", len(id_list))
        return
    like_id_list = list(id_list)
    url = 'https://vapp.tmuyun.com/api/favorite/like'
    for i in range(inx):
        id = random.choice(like_id_list)
        like_id_list.remove(id)
        requestid = random_uuid()
        timestamp = (int(time.time() * 1000))
        signature = f"/api/favorite/like&&{session}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
        headers = {
            "X-SESSION-ID": session,
            "X-REQUEST-ID": requestid,
            "X-TIMESTAMP": str(timestamp),
            "X-SIGNATURE": sha256(signature),
            "X-TENANT-ID": "68",
            "User-Agent": random_ua(),
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "22",
            "Host": "vapp.tmuyun.com"
        }
        data = f"action=true&id={id}"
        response = requests.post(url, headers=headers, data=data)
        result = response.json()
        print(f"点赞{id}：{result['message']}")
        if i < inx - 1:
            random_sleep(10, 15)

#分享
def doTask(inx):
    if len(id_list) < 10:
        print("id_list数量不足，不进行此任务", len(id_list))
        return
    doTask_id_list = list(id_list)
    url = 'https://vapp.tmuyun.com/api/user_mumber/doTask'
    for i in range(inx):
        id = random.choice(doTask_id_list)
        doTask_id_list.remove(id)
        requestid = random_uuid()
        timestamp = (int(time.time() * 1000))
        signature = f"/api/user_mumber/doTask&&{session}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
        headers = {
            "X-SESSION-ID": session,
            "X-REQUEST-ID": requestid,
            "X-TIMESTAMP": str(timestamp),
            "X-SIGNATURE": sha256(signature),
            "X-TENANT-ID": "68",
            "User-Agent": random_ua(),
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "44",
            "Host": "vapp.tmuyun.com"
        }
        data = f"memberType=3&member_type=3&target_id={id}"
        response = requests.post(url, headers=headers, data=data)
        result = response.json()
        print(f"分享{id}：{result['message']}")
        if i < inx - 1:
            random_sleep(5, 10)

#评论
def create(inx):
    url = 'https://vapp.tmuyun.com/api/comment/create'
    create_id_list = list(id_list)
    for i in range(inx):
        id = random.choice(create_id_list)
        create_id_list.remove(id)
        requestid = random_uuid()
        timestamp = (int(time.time() * 1000))
        signature = f"/api/comment/create&&{session}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
        headers = {
            "X-SESSION-ID": session,
            "X-REQUEST-ID": requestid,
            "X-TIMESTAMP": str(timestamp),
            "X-SIGNATURE": sha256(signature),
            "X-TENANT-ID": "68",
            "User-Agent": random_ua(),
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "vapp.tmuyun.com"
        }
        content = "赞一个"
        data = f"channel_article_id={id}&content={urllib.parse.quote(content)}"
        response = requests.post(url, headers=headers, data=data)
        result = response.json()
        print(f"评论{id}：{result['message']}")
        if result['message'] != 'success':
            id_list.remove(id)
        if i < inx - 1:
            random_sleep(5, 10)
    
def main(task_name, inx=None):
    if task_name == "每日签到":
        sign()
    elif task_name == "新闻资讯阅读":
        detail(inx + 2) 
    elif task_name == "分享资讯给好友":
        doTask(inx)
    elif task_name == "新闻资讯点赞":
        like(inx + 3)
    elif task_name == "新闻资讯评论":
        create(inx)
    elif task_name == "邀请好友":
        print("跳过")

def account_init():
    url = 'https://vapp.tmuyun.com/api/account/init'
    requestid = random_uuid()
    timestamp = (int(time.time() * 1000))
    signature = f"/api/account/init&&&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
    headers = {
        "X-REQUEST-ID": requestid,
        "X-TIMESTAMP": str(timestamp),
        "X-SIGNATURE": sha256(signature),
        "X-TENANT-ID": "68",
        "User-Agent": random_ua(),
        "Host": "vapp.tmuyun.com"
    }
    response = requests.post(url, headers=headers)
    result = response.json()
    if result['message'] == "success":
        print("获取随机用户成功")
        id = result['data']['session']['id']
        name = result['data']['account']['nick_name']
        print(name + '：' + id)
        return id
    else:
        return False    

def app_nav_list():
    sessionid = account_init()
    if sessionid == False:
        return False
    url = 'https://vapp.tmuyun.com/api/app_nav/list'
    requestid = random_uuid()
    timestamp = (int(time.time() * 1000))
    signature = f"/api/app_nav/list&&{sessionid}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
    headers = {
        "X-SESSION-ID": sessionid,
        "X-REQUEST-ID": requestid,
        "X-TIMESTAMP": str(timestamp),
        "X-SIGNATURE": sha256(signature),
        "X-TENANT-ID": "68",
        "User-Agent": random_ua(),
        "Host": "vapp.tmuyun.com"
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    for item in result['data']['focus']:
        if item['name'] == '首页':
            return sessionid, item['nav_parameter']
    return False

def channel_list_1():
    sessionid, channel_id = app_nav_list()
    if channel_id == False:
        return False
    url = 'https://vapp.tmuyun.com/api/article/channel_list'
    params = {
        'channel_id': channel_id,
        'isDiFangHao': 'false',
        'is_new': 'true',
        'list_count': '0',
        'size': '100',
    }
    requestid = random_uuid()
    timestamp = (int(time.time() * 1000))
    signature = f"/api/article/channel_list&&{sessionid}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
    headers = {
        "X-SESSION-ID": sessionid,
        "X-REQUEST-ID": requestid,
        "X-TIMESTAMP": str(timestamp),
        "X-SIGNATURE": sha256(signature),
        "X-TENANT-ID": "68",
        "User-Agent": random_ua(),
        "Host": "vapp.tmuyun.com"
    }
    response = requests.get(url, params=params, headers=headers)
    result = response.json()
    for article_list in result['data']['article_list']:
        if 'column_news_list' in article_list:
            for column_news_list in article_list['column_news_list']:
                if column_news_list['id'] > 0:
                    print(column_news_list['id'], format_timestamp(column_news_list['updated_at']))
                    if timestamp_ct(column_news_list['updated_at']) == True:     
                        id_list.append(column_news_list['id'])
        else:
            print(article_list['id'], format_timestamp(article_list['updated_at']))
            if timestamp_ct(article_list['updated_at']) == True:
                id_list.append(article_list['id'])

def channel_list():
    sessionid, channel_id = app_nav_list()
    if channel_id == False:
        return False
    url = 'https://vapp.tmuyun.com/api/article/channel_list'
    params = {
        'channel_id': channel_id,
        'isDiFangHao': 'false',
        'is_new': 'true',
        'list_count': '0',
        'size': '200',
    }
    requestid = random_uuid()
    timestamp = (int(time.time() * 1000))
    signature = f"/api/article/channel_list&&{sessionid}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
    headers = {
        "X-SESSION-ID": sessionid,
        "X-REQUEST-ID": requestid,
        "X-TIMESTAMP": str(timestamp),
        "X-SIGNATURE": sha256(signature),
        "X-TENANT-ID": "68",
        "User-Agent": random_ua(),
        "Host": "vapp.tmuyun.com"
    }
    response = requests.get(url, params=params, headers=headers)
    result = response.json()
    for article_list in result['data']['article_list']:
        if 'column_news_list' in article_list:
            for column_news_list in article_list['column_news_list']:
                if column_news_list['id'] > 0:
                    print(column_news_list['id'], format_timestamp(column_news_list['updated_at']))
                    id_list.append(column_news_list['id'])
        else:
            print(article_list['id'], format_timestamp(article_list['updated_at']))
            id_list.append(article_list['id'])

#任务状态
def numberCenter():
    url = 'https://vapp.tmuyun.com/api/user_mumber/numberCenter?is_new=1'
    task_cond = []
    for i in range(5):
        requestid = random_uuid()
        timestamp = (int(time.time() * 1000))
        signature = f"/api/user_mumber/numberCenter&&{session}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
        headers = {
            "X-SESSION-ID": session,
            "X-REQUEST-ID": requestid,
            "X-TIMESTAMP": str(timestamp),
            "X-SIGNATURE": sha256(signature),
            "X-TENANT-ID": "68",
            "User-Agent": random_ua(),
            "Host": "vapp.tmuyun.com"
        }
        response = requests.get(url, headers=headers)
        result = response.json()
        if result['code'] != 0:
            print(result)
            return False
        mobile = result['data']['rst']['mobile']
        total_integral = result['data']['rst']['total_integral']
        sign_name = result['data']['daily_sign_info']['name']
        for daily_sign in result['data']['daily_sign_info']['daily_sign_list']:
            if 'current' in daily_sign:
                if daily_sign['signed'] == False:
                    print(f"执行任务：{sign_name}")
                    main(sign_name)
                    if sign_name not in task_cond:
                        task_cond.append(sign_name)
                elif daily_sign['signed'] == True and sign_name in task_cond:
                    task_cond.remove(sign_name)
        for item in result['data']['rst']['user_task_list']:
            if item['name'] not in not_task and item['frequency'] - item['finish_times'] > 0:
                remain = item['frequency'] - item['finish_times']
                print(f"执行任务：{item['name']} * {remain}")
                main(item['name'], remain)
                if item['name'] not in task_cond:
                    task_cond.append(item['name'])
            elif item['frequency'] == item['finish_times'] and item['name'] in task_cond:
                task_cond.remove(item['name'])
        if len(task_cond) == 0:
            print("任务已全部完成")
            break
        else:
            print("等待10秒刷新任务状态")
            time.sleep(10)
    m_total = f"{mobile}：{total_integral}"
    msg.append(m_total)
    print(m_total)
    return True

if __name__ == '__main__':
    title_name = '笛杨新闻'
    env_session = "DYsession"
    msg = []
    id_list = []
    session_list = []
    phone_list = []
    index = 0
    quantity = ql_env(env_session)
    print(f"共找到{len(quantity)}个账号")
    channel_list()
    print(id_list,len(id_list))
    for session in quantity:
        print(f"\n------------正在执行第{index + 1}个账号----------------")
        if numberCenter():
            delete()
        else:
            print("账号过期")
        index += 1
        if index < len(quantity):
            random_sleep(1, 100)
    send(f"{title_name}：{index}", '\n'.join(msg))
