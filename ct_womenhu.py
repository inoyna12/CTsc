'''
cron: 2 0 * * *
new Env('联通沃门户签到');

变量： wmhcks
export wmhcks="号码1&authToken"
# 号码1 手机号
# authToken 签到页面抓到的请求头Authentication
# 多账号换行隔开
'''

import requests
import time
import datetime
import threading
import re
import os

################################ 配置区开始 ################################
# 使用 www.pushplus.plus 进行消息推送
PUSH_PLUS_TOKEN = 'PUSH_PLUS_TOKEN'
config_list = []
# 获取环境变量
env_dist = os.environ
wmhcks = env_dist.get("wmhcks")
cookies = wmhcks.split("\n")
for index, ck in enumerate(cookies):
    tempList = ck.split("&")
    config_list.append({"mobile": tempList[0],"authToken": tempList[1]})


################################ 配置区结束 ################################


headers = {"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; M2011K2C Build/SKQ1.211006.001)"}
msg_list = []


class TimeUtil(object):
    @classmethod
    def parse_timezone(cls, timezone):
        """
        解析时区表示
        :param timezone: str eg: +8
        :return: dict{symbol, offset}
        """
        result = re.match(r'(?P<symbol>[+-])(?P<offset>\d+)', timezone)
        symbol = result.groupdict()['symbol']
        offset = int(result.groupdict()['offset'])

        return {
            'symbol': symbol,
            'offset': offset
        }

    @classmethod
    def convert_timezone(cls, dt, timezone="+0"):
        """默认是utc时间，需要"""
        result = cls.parse_timezone(timezone)
        symbol = result['symbol']

        offset = result['offset']

        if symbol == '+':
            return dt + datetime.timedelta(hours=offset)
        elif symbol == '-':
            return dt - datetime.timedelta(hours=offset)
        else:
            raise Exception('dont parse timezone format')


def pushplus(title, content):
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": PUSH_PLUS_TOKEN,
        "title": title,
        "content": content
    }
    # print(requests.post(url=url, json=data).json())

def timorNotify(title, content):
    url = 'http://setfrp.timor.3344love.cn/notify/send'
    data = {
        "title": title,
        "content": content,
        "from": "沃门户"
    }
    # print(requests.post(url=url, json=data).json())


def format_msg():
    str1 = ''
    for item in msg_list:
        str1 += str(item) + "\r\n"
    return str1


def get(url, data):
    # print(data)
    ret = requests.get(url=url, params=data, headers=headers).json()
    # print(ret)
    return ret


def post(url, data, token=None):
    # print(data)
    ret = requests.post(url=url, params=data, headers={"Authorization": token, **headers}).json()
    # print(ret)
    return ret


def refresh(refresh_token):
    url = 'https://account.bol.wo.cn/cuuser/cuauth/token'
    data = {
        "clientSecret": "ybdkqwvi5hulnckjm255gvxqsb8elygo",
        "clientId": "woportal",
        "grantType": "refresh_token",
        "refreshToken": refresh_token,
    }
    return get(url, data)


def user_info(access_token):
    url = 'https://wo.cn/woportalapi/cuuser/auth/userinfo'
    data = {
        "accessToken": access_token,
        "channelId": "202"
    }
    return get(url, data)

def get_all_page(token):
    url = 'https://w2ol.wo.cn/woportalapi/woportal/rewarding/getAllPage'
    data = {
        "pageId": "092adcce-fc3e-463f-8cc2-96b516b045c7",
        "channel": "Android",
        "appName": ""
    }
    return post(url, data, token)


def sign(policy_id, trail_id, task_id, rewarding_task_id, token):
    url = 'https://w2ol.wo.cn/woportalapi/woportal/rewarding/sign'
    data = {
        "policyId": policy_id,
        "trailId": trail_id,
        "taskId": task_id,
        "rewardingTaskId": rewarding_task_id,
        "disposable": "true",
    }
    return post(url, data, token)


def gift_list(token):
    url = 'https://w2ol.wo.cn/woportalapi/woportal/gift/giftList'
    data = {
        "pageNum": "1",
        "pageSize": "20",
        "consumptionStatus": ""
    }
    return post(url, data, token)


def get_prize(history_id, token):
    url = 'https://w2ol.wo.cn/woportalapi/woportal/gift/getPrize'
    data = {
        "historyId": history_id,
        "disposable": "true"
    }
    return post(url, data, token)


# 与当前相差天数
def get_diff_days_2_now(date_str):
    utc_now = datetime.datetime.utcnow()
    now_time = TimeUtil.convert_timezone(utc_now, '+8')
    compare_time = time.strptime(date_str, "%Y-%m-%d")
    # 比较日期
    date1 = datetime.datetime(compare_time[0], compare_time[1], compare_time[2])
    date2 = datetime.datetime(now_time.year, now_time.month, now_time.day)
    diff_days = (date2 - date1).days
    return diff_days


def task(config):
    mobile = config['mobile']
    msg = ['开始执行: ' + mobile]
    token = config['authToken']
    ret = get_all_page(token)
    if ret['code'] != '0000':
        msg.append('token失效')
        msg.append("----------------------------------------------")
        msg_list.extend(msg)
        return
    policy_id = ret['data']['continuationRewardingTask']['rewardingTaskInfo']['policyId']
    # print("policyId: " + policy_id)
    for item in ret['data']['creditPolicies']:
        if item['policyId'] == policy_id:
            rewarding_task_id = item['creditRewardingTaskId']
            # print("rewardingTaskId: " + rewarding_task_id)
            first_sign = item['tasks'][0]['effectiveFrom']
            # print(first_sign)
            days = get_diff_days_2_now(first_sign.split(' ')[0])
            print("相差天数: " + str(days))
            msg.append("第 " + str(days + 1) + " 天")
            if item['tasks'][days]['updateTime'] is not None:
                msg.append("今日已签到, 签到时间: " + item['tasks'][days]['updateTime'])
            else:
                for task_info in ret['data']['getRewardingTask']['rewardingTaskInfos']:
                    if task_info['policyId'] == policy_id:
                        rewarding_trails = task_info['rewardingTrails']
                        trail_id = rewarding_trails[days]['trailId']
                        task_id = rewarding_trails[days]['taskId']
                        # print("trailId: " + trail_id)
                        # print("taskId: " + task_id)
                        sign_ret = sign(policy_id, trail_id, task_id, rewarding_task_id, token)
                        msg.append(sign_ret['msg'])
    # 兑换奖品
    ret = gift_list(token)
    for item in ret['data']:
        if item['consumptionStatus'] == 0:
            result = get_prize(item['historyId'], token)
            msg.append(result['msg'])
    msg.append("----------------------------------------------")
    msg_list.extend(msg)


def main_handler(event, context):
    l = []
    for config in config_list:
        p = threading.Thread(target=task, args=(config,))
        l.append(p)
        p.start()
    for i in l:
        i.join()
    content = format_msg()
    if PUSH_PLUS_TOKEN != '':
        count = 0
        error_count = 0
        for item in msg_list:
            if '----------------------------------------------' == item:
                count = count + 1
            if 'token失效' == item:
                error_count = error_count + 1
        if error_count > 0:
            # pushplus('沃门户任务Token失效请及时更新, 成功执行 ' + str(count), content)
            timorNotify('沃门户任务Token失效请及时更新, 成功执行 ' + str(count), content)
        else:
            # pushplus('沃门户任务, 成功执行 ' + str(count), content)
            timorNotify('沃门户任务, 成功执行 ' + str(count), content)
    print(content)
    return content


if __name__ == '__main__':
    main_handler('', '')