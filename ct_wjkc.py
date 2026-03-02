import requests, json, base64, hashlib

user_list = [
    {"user_name": "inoyna@163.com", "passwd": "inoyna11"},
    {"user_name": "", "passwd": ""},
    {"user_name": "", "passwd": ""},
    {"user_name": "", "passwd": ""},
]
#https://wxpusher.dingliqc.com/docs/#/ 创建app后获取apptoken，然后关注生成的二维码后获取UID
wxpusher_config = {
    "appToken": "",
    "uid": ""
}

hosts = "https://wj-kc.com"
user_api = "/api/user/userinfo"
sign_api = "/api/user/sign_use"
login_api = "/api/user/login"
data = {"data": "e30="}


def pushplus_bot(title: str, content: str) -> None:
    """
    通过 push+ 推送消息。
    """
    if not wxpusher_config.get("appToken"):
        print("PUSHPLUS 服务的 appToken 未设置!!\n取消推送")
        return
    print("PUSHPLUS 服务启动")

    url = "https://wxpusher.zjiecode.com/api/send/message"
    data = {
        "appToken": wxpusher_config.get("appToken"),
        "content": content,
        "contentType": 1,
        "summary": title,
        "uids": [wxpusher_config.get("uid")],
    }
    body = json.dumps(data).encode(encoding="utf-8")
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, data=body, headers=headers).json()

    if response["code"] == 1000:
        print("WxPusher 推送成功！")
    else:
        print("WxPusher 推送失败！,response:", response)


def decode_data(base64_data):
    if base64_data:
        data = base64.b64decode(base64_data).decode('utf-8')
        data = json.loads(data)
        return data
    else:
        return base64_data


def user_info(headers, data):
    print("check auth ")
    print(headers)

    resp = requests.post(hosts + user_api, headers=headers, verify=False, json=data)
    if resp.status_code == 200:
        resp = resp.json()
        base64_data = resp.get("data")
        data = decode_data(base64_data)
        print(data)
        if isinstance(data, dict):
            email = data.get("data").get("email")
            return True
        else:
            return False
    else:
        return False


def sign(headers, data):
    print("start sign ing")
    resp = requests.post(hosts + sign_api, headers=headers, verify=False, json=data)
    if resp.status_code == 200:
        resp = resp.json()
        base64_data = resp.get("data")
        data = decode_data(base64_data)
        if isinstance(data, dict):
            if data.get("msg") in ["SUCCESS", "SIGN_USE_MULTY_TIMES"]:
                msg = "签到成功"
                print(msg)
                return msg
            else:
                return ("签到失败！", data.get("msg"))
        else:
            return ("签到失败:解析响应失败:", data)
    else:
        return ("签到失败:请求错误", resp.content)


def login(user_name, passwd):
    print("start login")
    login_data = {'email': user_name, 'password': hashlib.md5(passwd.encode()).hexdigest()}
    encoded_login_data = base64.b64encode(json.dumps(login_data).encode()).decode()
    print(encoded_login_data)
    final_data = {'data': encoded_login_data}
    resp = requests.post(hosts + login_api, json=final_data)
    if resp.status_code == 200:
        data = resp.json().get("data", "")
        data = decode_data(data)
        if data.get("msg", "") == "SUCCESS":
            token = resp.headers.get("Set-Cookie")
            token = token.split(";")[0].split("=")[1]
            if token:
                return token
            else:
                print("响应成功，获取token失败:", data)
                return False
        else:
            print("响应成功，状态异常：", data)
            return False
    else:
        print("请求异常:", resp.content.decode("utf-8"))
        return False


def run():
    for i in user_list:
        user_name = i["user_name"]
        passwd = i["passwd"]
        token = login(user_name, passwd)
        is_push = True
        title = "网际快车签到失败！"
        content = ""
        if token:
            headers = {"Cookie": "token={}".format(token)}
            if user_info(headers, data):
                sign_result = sign(headers, data)
                if sign_result == "签到成功":
                    is_push = False
                else:
                    content = sign_result
            else:
                content = "用户身份校验异常"
        else:
            content = "登陆失败！"
        if is_push:
            pushplus_bot(title, content)


if __name__ == '__main__':
    run()
