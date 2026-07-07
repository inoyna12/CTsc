'''
获取验证码逻辑
首先设置基准ID，一般第1个是最大的ID

判断：id大于基准id and 短信标题是否存在 and 号码后四位数字是否一样

[{"id":10904,"number":"10687452311625603345","content":"【海马云】757708为您的登录验证码，请于5分钟内填写，如非本人操作，请忽略本短信。","com":174,"time":"2026-04-16 11:21:34","simnum":"18****4840"},{"id":10872,"number":"10687452999999351997","content":"【多点】您正在设置登录密码，验证码809598。请勿泄漏验证码。","com":12,"time":"2026-04-16 11:18:57","simnum":"17****2140"},{"id":10858,"number":"10687452311625603345","content":"【海马云】306521为您的登录验证码，请于5分钟内填写，如非本人操作，请忽略本短信。","com":10,"time":"2026-04-16 11:18:00","simnum":"17****4982"},{"id":10810,"number":"10687452999999351997","content":"【多点】您正在设置支付密码，验证码为：639227 。请勿泄漏验证码。","com":12,"time":"2026-04-16 11:14:44","simnum":"17****2140"},{"id":10798,"number":"10687452999999351997","content":"【多点】您正在设置支付密码，验证码为：978176 。请勿泄漏验证码。","com":12,"time":"2026-04-16 11:13:26","simnum":"17****2140"},{"id":10796,"number":"10681436664458260003","content":"【多点】您正在设置支付密码，验证码为：565548 。请勿泄漏验证码。","com":12,"time":"2026-04-16 11:13:25","simnum":"17****2140"},{"id":10790,"number":"10687452999999351997","content":"【多点】验证码737593，您正在登录多点账户，请勿转发或泄露。任何索要验证码的，疑为诈骗。","com":12,"time":"2026-04-16 11:12:50","simnum":"17****2140"},{"id":10466,"number":"10684682800000780668","content":"【螃蟹账号】商品编号SYJWE8584（游戏：三角洲行动）的取消需要您确认，目前距离系统自动确认仅剩 1 小时。请您尽快登录平台完成操作以确保流程顺利推进。如遇问题，可联系平台客服协助，感谢您的配合！","com":33,"time":"2026-04-16 11:01:27","simnum":"18****7914"},{"id":10392,"number":"10684682800000780668","content":"【螃蟹账号】商品编号WMZFZ6036（游戏：王者荣耀）的取消需要您确认，目前距离系统自动确认仅剩 1 小时。请您尽快登录平台完成操作以确保流程顺利推进。如遇问题，可联系平台客服协助，感谢您的配合！","com":13,"time":"2026-04-16 11:00:22","simnum":"17****0754"}]
'''


import requests, json, re, time, uuid
from tools.githubFile import GithubFile

HOST = 'sms.szfangmm.com:3000'  #host
SF_TOKEN = 'neTgGKNHpBkQ7vcQKqXoGk'  #每个号码组对应的token
CODE_TITLE = '生数科技'  #短信标题
simnum = ''  #手机号
MAX_POLLING_ATTEMPTS = 20  # 验证码轮询最大尝试次数（网络错误时也会继续轮询）
POLL_INTERVAL_MS = 3  # 轮询间隔时间（秒）

invite_code = "RICOMM"

# 获取id
def get_id(token):
    url = f'http://{HOST}/api/smslist?token={token}'
    headers = {
        'Host': HOST
    }
    result = requests.get(url, headers=headers).json()
    if len(result) > 0:
        id = result[0]['id']
        return id
    else:
        return 0

# 提取验证码
def extract_verification_code(text):
  pattern = r'(?<!\d)\d{4,6}(?!\d)'
  match = re.search(pattern, text)

  if match:
    return match.group(0)
  else:
    # 如果没有找到，返回 None
    return None

# 获取验证码 
def get_code(token, title, id, simnum):
    url = f'http://{HOST}/api/smslist?token={token}'
    headers = {
        'Host': HOST
    }
    # id = get_id(host, token)
    for i in range(MAX_POLLING_ATTEMPTS):
        result = requests.get(url, headers=headers).json()
        for item in result:
            print(item)
            encrypted_num = re.sub(r'\D', '', item['simnum'])

            if item['id'] > id and title in item['content'] and simnum[:2] == encrypted_num[:2] and simnum[-4:] == encrypted_num[-4:]:
                content = item['content']
                code = extract_verification_code(content)
                print(code)
                return
        time.sleep(POLL_INTERVAL_MS)


def send_auth_code(phone_number: str):
    url = "https://service.vidu.cn/iam/v1/users/send-auth-code"

    payload = {
        "channel": "sms",
        "receiver": f'+86{phone_number}',
        "purpose": "login",
        "locale": "en"
    }

    # 动态生成 uuid 作为请求标识，避免被服务器风控或去重
    request_id = str(uuid.uuid4())

    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'Content-Type': "application/json",
        'x-platform': "web",
        'x-request-id': request_id,
        'sec-ch-ua-platform': "\"Android\"",
        'accept-language': "zh",
        'sec-ch-ua': "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Android WebView\";v=\"150\"",
        'sec-ch-ua-mobile': "?1",
        'x-app-version': "-",
        'origin': "https://www.vidu.cn",
        'x-requested-with': "mark.via",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://www.vidu.cn/",
        'priority': "u=1, i"
    }

    # 使用 json 参数会自动进行 json.dumps 并设置 header
    result = requests.post(url, json=payload, headers=headers).json()
    print(result)

def login_by_auth_code(phone_number: str, auth_code: str, device_id: str = None):
 
    url = "https://service.vidu.cn/iam/v1/users/login"


    # 如果未指定 device_id，则动态生成一个符合格式要求的 ID
    if not device_id:
        device_id = f"DEVICE_{uuid.uuid4()}"

    payload = {
        "id_type": "phone",
        "identity": f"+86{phone_number}",
        "auth_type": "authcode",
        "credential": str(auth_code).strip(),
        "device_id": device_id,
        "invite_code": invite_code,
        "team_invite_code": "",
        "receive_marketing_msg": False
    }

    # 动态生成本次请求的唯一的 x-request-id
    request_id = str(uuid.uuid4())

    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'Content-Type': "application/json",
        'x-platform': "web",
        'x-request-id': request_id,
        'sec-ch-ua-platform': "\"Android\"",
        'accept-language': "zh",
        'sec-ch-ua': "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Android WebView\";v=\"150\"",
        'sec-ch-ua-mobile': "?1",
        'x-app-version': "-",
        'origin': "https://www.vidu.cn",
        'x-requested-with': "mark.via",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://www.vidu.cn/",
        'priority': "u=1, i"
    }

    result = requests.post(url, json=payload, headers=headers).json()
    print(result)
    return result['token']

def get_my_credits(jwt_token: str):
    url = "https://service.vidu.cn/credit/v1/credits/me"

    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'x-platform': "web",
        'sec-ch-ua-platform': "\"Android\"",
        'x-app-version': "-",
        'accept-language': "zh",
        'sec-ch-ua': "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Android WebView\";v=\"150\"",
        'sec-ch-ua-mobile': "?1",
        'origin': "https://www.vidu.cn",
        'x-requested-with': "mark.via",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'referer': "https://www.vidu.cn/",
        'priority': "u=1, i",
        # 动态拼接传入的 JWT Token 到 Cookie 中
        'Cookie': f"JWT={jwt_token.strip()}"
    }

    result = requests.get(url, headers=headers).json()
    print(result)

if __name__ == '__main__':
    sifang_phone = GithubFile(f'四方/{SF_TOKEN}.txt', as_json=False).cont
    phone_lst = [line.strip() for line in sifang_phone.strip().split('\n') if line.strip()]
    for item in phone_lst:
        phone = re.search(r'\d{11}', item)
        sifangID = get_id(SF_TOKEN)
        send_auth_code(phone)
        sifang_code = get_code(SF_TOKEN, CODE_TITLE, sifangID, phone)
        token = login_by_auth_code(phone, sifang_code)
        get_my_credits(token)
        exit()
