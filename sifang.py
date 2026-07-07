'''
获取验证码逻辑
首先设置基准ID，一般第1个是最大的ID

判断：id大于基准id and 短信标题是否存在 and 号码后四位数字是否一样

[{"id":10904,"number":"10687452311625603345","content":"【海马云】757708为您的登录验证码，请于5分钟内填写，如非本人操作，请忽略本短信。","com":174,"time":"2026-04-16 11:21:34","simnum":"18****4840"},{"id":10872,"number":"10687452999999351997","content":"【多点】您正在设置登录密码，验证码809598。请勿泄漏验证码。","com":12,"time":"2026-04-16 11:18:57","simnum":"17****2140"},{"id":10858,"number":"10687452311625603345","content":"【海马云】306521为您的登录验证码，请于5分钟内填写，如非本人操作，请忽略本短信。","com":10,"time":"2026-04-16 11:18:00","simnum":"17****4982"},{"id":10810,"number":"10687452999999351997","content":"【多点】您正在设置支付密码，验证码为：639227 。请勿泄漏验证码。","com":12,"time":"2026-04-16 11:14:44","simnum":"17****2140"},{"id":10798,"number":"10687452999999351997","content":"【多点】您正在设置支付密码，验证码为：978176 。请勿泄漏验证码。","com":12,"time":"2026-04-16 11:13:26","simnum":"17****2140"},{"id":10796,"number":"10681436664458260003","content":"【多点】您正在设置支付密码，验证码为：565548 。请勿泄漏验证码。","com":12,"time":"2026-04-16 11:13:25","simnum":"17****2140"},{"id":10790,"number":"10687452999999351997","content":"【多点】验证码737593，您正在登录多点账户，请勿转发或泄露。任何索要验证码的，疑为诈骗。","com":12,"time":"2026-04-16 11:12:50","simnum":"17****2140"},{"id":10466,"number":"10684682800000780668","content":"【螃蟹账号】商品编号SYJWE8584（游戏：三角洲行动）的取消需要您确认，目前距离系统自动确认仅剩 1 小时。请您尽快登录平台完成操作以确保流程顺利推进。如遇问题，可联系平台客服协助，感谢您的配合！","com":33,"time":"2026-04-16 11:01:27","simnum":"18****7914"},{"id":10392,"number":"10684682800000780668","content":"【螃蟹账号】商品编号WMZFZ6036（游戏：王者荣耀）的取消需要您确认，目前距离系统自动确认仅剩 1 小时。请您尽快登录平台完成操作以确保流程顺利推进。如遇问题，可联系平台客服协助，感谢您的配合！","com":13,"time":"2026-04-16 11:00:22","simnum":"17****0754"}]
'''


import requests, json, re, time

sfHost = 'sms.szfangmm.com:3000'  #host
token = '4FwTXvFkiPt7ThU7NkPfS'  #每个号码组对应的token
content_title = '迅游网络'  #短信标题
simnum = '18531297207'  #手机号
MAX_POLLING_ATTEMPTS = 60  # 验证码轮询最大尝试次数（网络错误时也会继续轮询）
POLL_INTERVAL_MS = 3000  # 轮询间隔时间（毫秒）

# 获取id
def get_id(host, token):
    url = f'http://{host}/api/smslist?token={token}'
    headers = {
        'Host': host
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
def get_code(host, token, title, simnum):
    url = f'http://{host}/api/smslist?token={token}'
    headers = {
        'Host': host
    }
    id = get_id(host, token)
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
        time.sleep(POLL_INTERVAL_MS / 1000.0)

get_code(sfHost, token, content_title, simnum)
