'''
cron: 36 12 * * *
new Env('笛杨新闻');
'''
import requests,json,random,datetime,time,urllib
from utils.utils import randomSleep,timeStamp,sha256Encode
from uuid import uuid4
from notify import send
from datetime import timedelta

title_name = '笛杨新闻'
version = '3.0.3'

filepath = "/ql/data/env/dyxw.json"

comment_list = ["赞一个", "非常好", "666"]

debug = 0

def send_request(url, method='GET', **kwargs):
    attempt = 0
    MAX_RETRIES = 3  # 重试次数
    sleep_time = 30  # 重试等待时间
    time_out = 30  # 请求超时
    while attempt < MAX_RETRIES:
        try:
            method = method.upper()
            if method not in ['GET', 'POST']:
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
            time.sleep(10)
        else:
            print("超过最大重试次数")
            return None

# 随机ua
def randomUA():
    random_uuid = str(uuid4())
    ua_uuid = "00000000" + random_uuid[8:][:11] + "0000" + random_uuid[23] + "0000" + random_uuid[28:]
    UA = f"{version};{ua_uuid};Xiaomi 22081212C;Android;12;Release"
    return UA

# 处理id
def getId(id, timestamp):
    input_time = datetime.datetime.fromtimestamp(timestamp / 1000)
    formatted_time = input_time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"{id} - {formatted_time}")
    time_difference = now - input_time
    if time_difference <= timedelta(days=2) and id > 0:
        id_day2_list.append(id)
    if time_difference <= timedelta(days=100) and id > 0:
        id_day100_list.append(id)

# 获取个人评论
def getAccountComment():
    url = 'https://vapp.tmuyun.com/api/account_comment/comment_list?size=20'
    requestid = str(uuid4())
    timestamp = int(time.time() * 1000)
    signature = f"/api/account_comment/comment_list&&{userData['sessionId']}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
    headers = {
        "X-SESSION-ID": userData['sessionId'],
        "X-REQUEST-ID": requestid,
        "X-TIMESTAMP": str(timestamp),
        "X-SIGNATURE": sha256Encode(signature),
        "X-TENANT-ID": "68",
        "User-Agent": randomUA(),
        "Host": "vapp.tmuyun.com"
    }
    result = send_request(url, 'GET', headers=headers)
    comment_list = []
    if result['message'] == "success":
        for item in result['data']['comment_list']:
            comment_list.append(item['id'])
        return comment_list
    print("获取个人评论失败")
    return comment_list

# 删除个人评论        
def delete():
    comment_list = getAccountComment()
    url = 'https://vapp.tmuyun.com/api/comment/delete'
    for comment_id in comment_list:
        requestid = str(uuid4())
        timestamp = int(time.time() * 1000)
        signature = f"/api/comment/delete&&{userData['sessionId']}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
        headers = {
            "X-SESSION-ID": userData['sessionId'],
            "X-REQUEST-ID": requestid,
            "X-TIMESTAMP": str(timestamp),
            "X-SIGNATURE": sha256Encode(signature),
            "X-TENANT-ID": "68",
            "User-Agent": randomUA(),
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "35",
            "Host": "vapp.tmuyun.com"
        }
        data = f"comment_id={comment_id}"
        result = send_request(url, 'POST', headers=headers, data=data)
        print(f"删除评论{comment_id}：{result['message']}")

# 个人信息
def accountDetail():
    url = 'https://vapp.tmuyun.com/api/user_mumber/account_detail'
    requestid = str(uuid4())
    timestamp = int(time.time() * 1000)
    signature = f"/api/user_mumber/account_detail&&{userData['sessionId']}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
    headers = {
        "X-SESSION-ID": userData['sessionId'],
        "X-REQUEST-ID": requestid,
        "X-TIMESTAMP": str(timestamp),
        "X-SIGNATURE": sha256Encode(signature),
        "X-TENANT-ID": "68",
        "User-Agent": randomUA(),
        "Host": "vapp.tmuyun.com"
    }
    result = send_request(url, 'GET', headers=headers)
    if result['message'] == "success":
        mobile = result['data']['rst']['mobile']
        total_integral = result['data']['rst']['total_integral']
        ref_code = result['data']['rst']['ref_code']
        userData['ref_code'] = ref_code
    else:
        print(result)
        send(title_name, f"{userData['phone']}〖{index}〗：个人信息获取失败")
        return False

# 邀请好友
def updateRefCode(num):
    url = 'https://vapp.tmuyun.com/api/account/update_ref_code'
    for i in range(num):
        session_id = getSessionid()
        if session_id is None:
            print("获取随机用户失败，跳过此任务。")
            return
        requestid = str(uuid4())
        timestamp = int(time.time() * 1000)
        signature = f"/api/account/update_ref_code&&{session_id}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
        headers = {
            "X-SESSION-ID": session_id,
            "X-REQUEST-ID": requestid,
            "X-TIMESTAMP": str(timestamp),
            "X-SIGNATURE": sha256Encode(signature),
            "X-TENANT-ID": "68",
            "User-Agent": randomUA(),
            "Host": "vapp.tmuyun.com"
        }
        data = {
            "ref_code": userData['ref_code']
        }
        result = send_request(url, 'POST', headers=headers, data=data)
        print(result)
        print(result['message'])

# 签到
def sign():
    url = 'https://vapp.tmuyun.com/api/user_mumber/sign'
    requestid = str(uuid4())
    timestamp = int(time.time() * 1000)
    signature = f"/api/user_mumber/sign&&{userData['sessionId']}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
    headers = {
        "X-SESSION-ID": userData['sessionId'],
        "X-REQUEST-ID": requestid,
        "X-TIMESTAMP": str(timestamp),
        "X-SIGNATURE": sha256Encode(signature),
        "X-TENANT-ID": "68",
        "User-Agent": randomUA(),
        "Host": "vapp.tmuyun.com"
    }
    result = send_request(url, 'GET', headers=headers)
    if result['message'] == "success":
        print(f"签到：{result['data']['reason']}，获得：积分{result['data']['signIntegral']}，经验{result['data']['signExperience']}")
   
#阅读
def detail(num):
    detail_id_list = list(id_day2_list)
    url = 'https://vapp.tmuyun.com/api/article/detail'
    for i in range(num):
        id = random.choice(detail_id_list)
        detail_id_list.remove(id)
        params = {
            'id': id
        }
        requestid = str(uuid4())
        timestamp = int(time.time() * 1000)
        signature = f"/api/article/detail&&{userData['sessionId']}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
        headers = {
            "X-SESSION-ID": userData['sessionId'],
            "X-REQUEST-ID": requestid,
            "X-TIMESTAMP": str(timestamp),
            "X-SIGNATURE": sha256Encode(signature),
            "X-TENANT-ID": "68",
            "User-Agent": randomUA(),
            "Host": "vapp.tmuyun.com"
        }
        result = send_request(url, 'GET', params=params, headers=headers)
        print(f"阅读{id}：{result['message']}")
        if i < num - 1:
            randomSleep(5, 10)

#点赞
def like(num):
    like_id_list = list(id_day2_list)
    url = 'https://vapp.tmuyun.com/api/favorite/like'
    for i in range(num):
        id = random.choice(like_id_list)
        like_id_list.remove(id)
        requestid = str(uuid4())
        timestamp = int(time.time() * 1000)
        signature = f"/api/favorite/like&&{userData['sessionId']}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
        headers = {
            "X-SESSION-ID": userData['sessionId'],
            "X-REQUEST-ID": requestid,
            "X-TIMESTAMP": str(timestamp),
            "X-SIGNATURE": sha256Encode(signature),
            "X-TENANT-ID": "68",
            "User-Agent": randomUA(),
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "22",
            "Host": "vapp.tmuyun.com"
        }
        data = f"action=true&id={id}"
        result = send_request(url, 'POST', headers=headers, data=data)
        print(f"点赞{id}：{result['message']}")
        if i < num - 1:
            randomSleep(5, 10)

#分享
def doTask(num):
    doTask_id_list = list(id_day2_list)
    url = 'https://vapp.tmuyun.com/api/user_mumber/doTask'
    for i in range(num):
        id = random.choice(doTask_id_list)
        doTask_id_list.remove(id)
        requestid = str(uuid4())
        timestamp = int(time.time() * 1000)
        signature = f"/api/user_mumber/doTask&&{userData['sessionId']}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
        headers = {
            "X-SESSION-ID": userData['sessionId'],
            "X-REQUEST-ID": requestid,
            "X-TIMESTAMP": str(timestamp),
            "X-SIGNATURE": sha256Encode(signature),
            "X-TENANT-ID": "68",
            "User-Agent": randomUA(),
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "44",
            "Host": "vapp.tmuyun.com"
        }
        data = f"memberType=3&member_type=3&target_id={id}"
        result = send_request(url, 'POST', headers=headers, data=data)
        print(f"分享{id}：{result['message']}")
        if i < num - 1:
            randomSleep(5, 10)

#评论
def create(num):
    url = 'https://vapp.tmuyun.com/api/comment/create'
    create_id_list = list(id_day100_list)
    createNum = 0
    for i in range(10):
        id = random.choice(create_id_list)
        create_id_list.remove(id)
        requestid = str(uuid4())
        timestamp = int(time.time() * 1000)
        signature = f"/api/comment/create&&{userData['sessionId']}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
        headers = {
            "X-SESSION-ID": userData['sessionId'],
            "X-REQUEST-ID": requestid,
            "X-TIMESTAMP": str(timestamp),
            "X-SIGNATURE": sha256Encode(signature),
            "X-TENANT-ID": "68",
            "User-Agent": randomUA(),
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "vapp.tmuyun.com"
        }
        content = random.choice(comment_list)
        data = f"channel_article_id={id}&content={urllib.parse.quote(content)}"
        result = send_request(url, 'POST', headers=headers, data=data)
        print(f"评论{id}：{result['message']}")
        if result['message'] == 'success':
            createNum += 1
        else:
            id_day100_list.remove(id)
        if createNum == num:
            return
        randomSleep(5, 10)

# 获取sessionid
def getSessionid():
    url = 'https://vapp.tmuyun.com/api/account/init'
    requestid = str(uuid4())
    timestamp = int(time.time() * 1000)
    signature = f"/api/account/init&&&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
    headers = {
        "X-REQUEST-ID": requestid,
        "X-TIMESTAMP": str(timestamp),
        "X-SIGNATURE": sha256Encode(signature),
        "X-TENANT-ID": "68",
        "User-Agent": randomUA(),
        "Host": "vapp.tmuyun.com"
    }
    result = send_request(url, 'POST', headers=headers)
    if result['message'] == "success":
        id = result['data']['session']['id']
        name = result['data']['account']['nick_name']
        print(name + '：' + id)
        return id
    print(result)
    print("获取sessionid失败")
    return None  

# 获取首页参数
def getNavParameter():
    sessionid = getSessionid()
    if sessionid is None:
        return None, None
    url = 'https://vapp.tmuyun.com/api/app_nav/list'
    requestid = str(uuid4())
    timestamp = int(time.time() * 1000)
    signature = f"/api/app_nav/list&&{sessionid}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
    headers = {
        "X-SESSION-ID": sessionid,
        "X-REQUEST-ID": requestid,
        "X-TIMESTAMP": str(timestamp),
        "X-SIGNATURE": sha256Encode(signature),
        "X-TENANT-ID": "68",
        "User-Agent": randomUA(),
        "Host": "vapp.tmuyun.com"
    }
    result = send_request(url, 'GET', headers=headers)
    for item in result['data']['focus']:
        if item['name'] == '首页':
            return sessionid, item['nav_parameter']
    print("获取首页参数失败")
    return None, None

# 获取首页id
def getChannelId():
    sessionid, channel_id = getNavParameter()
    if channel_id is None:
        print("获取首页ID失败")
        return
    url = 'https://vapp.tmuyun.com/api/article/channel_list'
    cycles = 15
    list_count = 0
    params = {
            'channel_id': channel_id,
            'isDiFangHao': 'false',
            'is_new': 'true',
            'list_count': str(list_count),
            'size': '20'
        }
    for i in range(cycles):
        requestid = str(uuid4())
        timestamp = int(time.time() * 1000)
        signature = f"/api/article/channel_list&&{sessionid}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
        headers = {
            "X-SESSION-ID": sessionid,
            "X-REQUEST-ID": requestid,
            "X-TIMESTAMP": str(timestamp),
            "X-SIGNATURE": sha256Encode(signature),
            "X-TENANT-ID": "68",
            "User-Agent": randomUA(),
            "Host": "vapp.tmuyun.com"
        }
        result = send_request(url, 'GET', headers=headers)
        start = result['data']['article_list'][-1]['sort_number']
        for article in result['data']['article_list']:
            if 'published_at' in article:
                getId(article['id'], article['published_at'])
            else:
                for column_news in article.get('column_news_list', []):
                    if 'published_at' in column_news:
                        getId(column_news['id'], column_news['published_at'])            
        list_count += 20
        params['list_count'] = str(list_count)
        params['start'] = str(start)
        if i < cycles - 1:
            randomSleep(10, 20)
    print("id_day2_list：",len(id_day2_list))
    print("id_day100_list：",len(id_day100_list))

#任务状态
def numberCenter():
    url = 'https://vapp.tmuyun.com/api/user_mumber/numberCenter?is_new=1'
    for i in range(5):
        requestid = str(uuid4())
        timestamp = int(time.time() * 1000)
        signature = f"/api/user_mumber/numberCenter&&{userData['sessionId']}&&{requestid}&&{timestamp}&&FR*r!isE5W&&68"
        headers = {
            "X-SESSION-ID": userData['sessionId'],
            "X-REQUEST-ID": requestid,
            "X-TIMESTAMP": str(timestamp),
            "X-SIGNATURE": sha256Encode(signature),
            "X-TENANT-ID": "68",
            "User-Agent": randomUA(),
            "Host": "vapp.tmuyun.com"
        }
        result = send_request(url, 'GET', headers=headers)
        if result['message'] != "success":
            print(result)
            return False
        mobile = result['data']['rst']['mobile']
        total_integral = result['data']['rst']['total_integral']
        userData['total_integral'] = total_integral
        user_task_list = result['data']['rst']['user_task_list']
        sign_list = result['data']['daily_sign_info']['daily_sign_list']
        sign_info = next((item for item in sign_list if item.get("current") == "今天"), None)
        if  sign_info['signed'] is False:
            sign()
        for user_task in user_task_list:
            name = user_task['name']
            finish_times = user_task['finish_times']
            frequency = user_task['frequency']
            print(f"{name}：{finish_times}/{frequency}")
            if user_task['completed'] == 0:
                handleTasks(name, frequency - finish_times)
        all_completedStatus = all(
            task['completed'] == 1
            for task in user_task_list
            if task['name'] != '邀请好友'
        )
        if all_completedStatus:
            userData['taskStatus'] = True
            print("任务已全部完成")
            return
        else:
            randomSleep(10, 20)

# 执行任务
def handleTasks(name, num):
    if name == "新闻资讯阅读":
        detail(num) 
    elif name == "分享资讯给好友":
        doTask(num)
    elif name == "新闻资讯点赞":
        like(num)
    elif name == "新闻资讯评论":
        create(num)
    elif name == "邀请好友":
#        updateRefCode(num)
        pass
    else:
        send(title_name, f"未知任务：{name}")

def main():
    if accountDetail() is False:
        return
    numberCenter()
    randomSleep(20, 30)
    delete()
    
# 推送 
def msgSend():
    new_data_list = sorted(data_list, key=lambda x: float(x['total_integral']), reverse=True)#从大到小排序
    for new_data in new_data_list:
        phone = new_data['phone']
        total_integral = new_data['total_integral']
        taskStatus = new_data['taskStatus']
        msg.append(f"{phone}：{total_integral}积分：{taskStatus}")
    send(f"{title_name}：{len(new_data_list)}", '\n'.join(msg))

if __name__ == '__main__':
    msg = []
    id_day2_list = []
    id_day100_list = []
    with open(filepath, 'r', encoding='utf-8') as f:
        data_list = json.load(f)
    print(f"共找到{len(data_list)}个账号")
    now = datetime.datetime.now()
    getChannelId()
    for index, userData in enumerate(data_list, start = 1):
        print(f"\n{'-' * 13}正在执行第{index}个账号{'-' * 13}")
        userData['taskStatus'] = False
        main()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, indent=2)
        if index < len(data_list):
            randomSleep(60, 120)
    msgSend()
