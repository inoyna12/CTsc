#!/usr/bin/python3
# -- coding: utf-8 --
# export PHONE_NUM="手机号&多账号"
# 2023.3.24 阅读失败更新


from tools.notify import send
from tools.ql_api import get_cookie
from requests import post, get
from time import sleep, time
from datetime import datetime
from hashlib import md5 as md5Encode
from random import randint, uniform, choice, randint
from os import environ
from sys import stdout, exit
from base64 import b64encode
from base64 import b64decode
from json import dumps
from tools.encrypt_symmetric import Crypt
from tools.send_msg import push
from tools.tool import get_environ, random_sleep
import threading
msg_str = "联通话费兑换路径：联通APP搜索阅读--->阅读专区--->我的--->话费红包，可兑换3元或者5元话费抵扣券，最后使用沃钱包支付即可\n\n"

"""主类"""


class China_Unicom:
    def __init__(self, phone_num, run_ua):
        self.phone_num = phone_num
        default_ua = f"Mozilla/5.0 (Linux; Android {randint(8, 13)}; SM-S908U Build/TP1A.220810.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/{randint(95, 108)}.0.5359.128 Mobile Safari/537.36; unicom{{version:android@9.0{randint(0,6)}00,desmobile:{self.phone_num}}};devicetype{{deviceBrand:,deviceModel:}};{{yw_code:}}"
        if run_ua is None or run_ua == "":
            run_ua = default_ua

        self.headers = {
            "Host": "10010.woread.com.cn",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json;charset=utf-8",
            "Origin": "https://10010.woread.com.cn",
            "User-Agent": run_ua,
            "Connection": "keep-alive",
            "Referer": "https://10010.woread.com.cn/ng_woread/",
        }
        self.fail_num = 0
        self.activeIndex = '26'

    def timestamp(self):
        return round(time() * 1000)

    def print_now(self, content):
        print(content)
        stdout.flush()
        
    def printAndMsg(self, msg):
        global msg_str
        self.print_now(f"{msg}")
        msg_str += f"{msg}\n"

    def md5(self, str):
        m = md5Encode(str.encode(encoding='utf-8'))
        return m.hexdigest()

    def req(self, url, crypt_text, retry_num=5):
        while retry_num > 0:
            body = {
                "sign": b64encode(Crypt(crypt_type="AES", key="update!@#1234567", iv="16-Bytes--String", mode="CBC").encrypt(crypt_text).encode()).decode()
            }
            self.headers["Content-Length"] = str(
                len(dumps(body).replace(" ", "")))
            try:
                res = post(url, headers=self.headers, json=body)
                data = res.json()
                return data
            except Exception as e:
                self.print_now(f"本次请求失败, 正在重新发送请求 剩余次数{retry_num}")
                self.print_now(f"本次请求失败url------{url}")
                self.print_now(f"本次请求失败crypt_text------{crypt_text}")
                self.print_now(f"本次请求失败原因------{e}")
                retry_num -= 1
                sleep(10)
                return self.req(url, crypt_text, retry_num)

    def referer_login(self):
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        timestamp = self.timestamp()
        url = f"https://10010.woread.com.cn/ng_woread_service/rest/app/auth/10000002/{timestamp}/{self.md5(f'100000027k1HcDL8RKvc{timestamp}')}"
        crypt_text = f'{{"timestamp":"{date}"}}'
        body = {
            "sign": b64encode(Crypt(crypt_type="AES", key="1234567890abcdef").encrypt(crypt_text).encode()).decode()
        }
        self.headers["Content-Length"] = str(len(str(body)) - 1)
        data = post(url, headers=self.headers, json=body).json()
        print(f'referer_login===>{data}')
        if data["code"] == "0000":
            self.headers["accesstoken"] = data["data"]["accesstoken"]
        else:
            self.printAndMsg(f"设备登录失败,日志为{data}")
            exit(0)

    def get_userinfo(self):
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        url = "https://10010.woread.com.cn/ng_woread_service/rest/account/login"
        crypt_text = f'{{"phone":"{self.phone_num}","timestamp":"{date}"}}'
        data = self.req(url, crypt_text)
        print(f"账号{self.phone_num}登录结果------{data}")
        if data["code"] == "0000":
            self.userinfo = data["data"]
        else:
            self.printAndMsg(f"手机号登录失败, 日志为{data}")
            exit(0)

    def read_novel(self):
        global msg_str  
        self.get_cardid()
        self.get_chapterallindex()
        self.readChapter()
        self.print_now(
            f"你的账号{self.phone_num} ：正在执行观看70次小说, 此过程较久, 最大时长为70 * 2min = 120min\n")
        for i in range(70):
            date = datetime.today().__format__("%Y%m%d%H%M%S")
            hour = datetime.now().hour  # 获取当前时刻
            if hasattr(self, "activitystatus") and self.activitystatus == 1:
                self.printAndMsg(f"当前账号{self.phone_num}活动已完成")
                break
            if hasattr(self, "totalreadnums") and self.totalreadnums >= 120:
                if hasattr(self, "activitystatus") and self.activitystatus == 0:
                    self.printAndMsg(f"当前账号{self.phone_num}去完成活动")
                    self.finishActivity()
                else:
                    self.printAndMsg(f"当前账号{self.phone_num}阅读满了，跳过")
                break
            if hasattr(self, "readtime") and self.readtime / 600000 > hour/2 and self.status == 0 or hasattr(self, "readtime") and self.readtime > 7200000:
                self.get_activetion_id()
            url = f"https://10010.woread.com.cn/ng_woread_service/rest/cnt/wordsDetail?catid={self.catid}&pageIndex={self.pageIndex}&cardid={self.cardid}&cntindex={self.cntindex}&chapterallindex={self.chapterallindex}&chapterseno=1"
            crypt_text = f'{{"chapterAllIndex":{self.chapterallindex},"cntIndex":{self.cntindex},"cntTypeFlag":"1","timestamp":"{date}","token":"{self.userinfo["token"]}","userId":"{self.userinfo["userid"]}","userIndex":{self.userinfo["userindex"]},"userAccount":"{self.userinfo["phone"]}","verifyCode":"{self.userinfo["verifycode"]}"}}'
            data = self.req(url, crypt_text)
            if self.fail_num == 3:
                self.printAndMsg(f"账号{self.phone_num}阅读任务出现异常 且错误次数达到3次 请手动检查")
                exit(0)
            if data["code"] != "0000":
                self.printAndMsg(f"阅读小说发生异常:{data}")
                return self.main()
            if self.status == 1:
                self.wakeRabbit()
            else:
                print(f"账号{self.phone_num}正在执行第{i+1}次阅读")
                self.addReadTime()

    # 获取活动信息
    def get_activetion_id(self):
        url = "https://10010.woread.com.cn/ng_woread_service/rest/rabbitActivity/queryActivityData"
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        crypt_text = f'{{"activeIndex":"{self.activeIndex}","timestamp":"{date}","token":"{self.userinfo["token"]}","userId":"{self.userinfo["userid"]}","userIndex":{self.userinfo["userindex"]},"userAccount":"{self.userinfo["phone"]}","verifyCode":"{self.userinfo["verifycode"]}"}}'
        data = self.req(url, crypt_text)
        print(f"获取活动信息：{data}")
        if data["code"] == "0000":
            self.status = data["data"]["status"]
            self.totalreadnums = data["data"]["totalreadnums"]
            self.activitystatus = data["data"]["activitystatus"]
            return True
        else:
            self.print_now(data["message"])
            return False

    # 加入游戏
    def joinRuning(self):
        global msg_str  
        url = "https://10010.woread.com.cn/ng_woread_service/rest/rabbitActivity/joinRuning"
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        crypt_text = f'{{"activeIndex":{self.activeIndex},"timestamp":"{date}","token":"{self.userinfo["token"]}","userId":"{self.userinfo["userid"]}","userIndex":{self.userinfo["userindex"]},"userAccount":"{self.userinfo["phone"]}","verifyCode":"{self.userinfo["verifycode"]}"}}'
        data = self.req(url, crypt_text)
        self.printAndMsg(f"账号：{self.phone_num}{data}")

    # 上报阅读时间
    def addReadTime(self):
        global msg_str  
        url = "https://10010.woread.com.cn/ng_woread_service/rest/history/addReadTime"
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        crypt_text = f'{{"readTime":"2","cntIndex":"{self.cntindex}","cntType":"1","catid":"0","pageIndex":"","cardid":"{self.cardid}","cntindex":"{self.cntindex}","cnttype":"1","chapterallindex":"{self.chapterallindex}","chapterseno":"1","channelid":"","chapterid":"{self.chapterid}","readtype":1,"isend":"0","timestamp":"{date}","token":"{self.userinfo["token"]}","userId":"{self.userinfo["userid"]}","userIndex":{self.userinfo["userindex"]},"userAccount":"{self.userinfo["phone"]}","verifyCode":"{self.userinfo["verifycode"]}"}}'
        self.print_now(f"crypt_text:{crypt_text}\n")
        data = self.req(url, crypt_text)
        if data["code"] == '0000':
            self.readtime = data["data"]["readtime"]
            self.printAndMsg(f"账号：{self.phone_num}更新时间成功,当前阅读时间：{data['data']['readtime']}")
        elif data["code"] == '9999':
            self.fail_num += 1
            print(f"当前账号{self.phone_num}上报阅读时间：{data['message']}")
            self.main()
        self.print_now("---等待2分钟---\n")
        sleep(120)

    # 唤醒兔子
    def wakeRabbit(self):
        global msg_str  
        url = "https://10010.woread.com.cn/ng_woread_service/rest/rabbitActivity/wakeRabbit"
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        crypt_text = f'{{"activeIndex":"{self.activeIndex}","sactivitIndex":"7246","timestamp":"{date}","token":"{self.userinfo["token"]}","userId":"{self.userinfo["userid"]}","userIndex":{self.userinfo["userindex"]},"userAccount":"{self.userinfo["phone"]}","verifyCode":"{self.userinfo["verifycode"]}"}}'
        data = self.req(url, crypt_text)
        self.printAndMsg(f"账号：{self.phone_num}:wakeRabbit:{data}")
        self.get_activetion_id()

    # 结束活动
    def finishActivity(self):
        global msg_str  
        url = "https://10010.woread.com.cn/ng_woread_service/rest/rabbitActivity/finishActivity"
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        crypt_text = f'{{"activeIndex":"{self.activeIndex}","timestamp":"{date}","token":"{self.userinfo["token"]}","userId":"{self.userinfo["userid"]}","userIndex":{self.userinfo["userindex"]},"userAccount":"{self.userinfo["phone"]}","verifyCode":"{self.userinfo["verifycode"]}"}}'
        data = self.req(url, crypt_text)
        self.printAndMsg(f"账号：{self.phone_num}:finishActivity:{data}")

    def get_cardid(self):
        """
        获取cardid
        :return:
        """
        url = "https://10010.woread.com.cn/ng_woread_service/rest/basics/getIntellectRecommend"
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        crypt_text = f'{{"cntsize":8,"recommendsize":5,"recommendid":0,"timestamp":"{date}","token":"{self.userinfo["token"]}","userId":"{self.userinfo["userid"]}","userIndex":{self.userinfo["userindex"]},"userAccount":"{self.userinfo["phone"]}","verifyCode":"{self.userinfo["verifycode"]}"}}'
        data = self.req(url, crypt_text)
        self.pageIndex = data["data"]["recommendindex"] if "recommendindex" in data["data"] else "10725"
        self.cardid = data["data"]["catindex"] if "catindex" in data["data"] else "119056"
        self.catid = self.cardid if self.cardid else 0
        catlist = data["data"]["catlist"]
        rand_index = randint(0, len(catlist) - 1)
        self.cntindex = catlist[rand_index]["cntindex"]
        
    def get_chapterallindex(self):
        url = f"https://10010.woread.com.cn/ng_woread_service/rest/cnt/chalist?catid={self.catid}&pageIndex={self.pageIndex}&cardid={self.cardid}&cntindex={self.cntindex}"
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        crypt_text = f'{{"curPage":1,"limit":30,"index":"{self.cntindex}","sort":0,"finishFlag":1,"timestamp":"{date}","token":"{self.userinfo["token"]}","userId":"{self.userinfo["userid"]}","userIndex":{self.userinfo["userindex"]},"userAccount":"{self.userinfo["phone"]}","verifyCode":"{self.userinfo["verifycode"]}"}}'
        data = self.req(url, crypt_text)
        chapterallindexlist = data["list"][0]["charptercontent"]
        chapterallindex_num = len(chapterallindexlist)
        self.chapterallindex_list = [0] * chapterallindex_num
        i = 0
        while i < chapterallindex_num:
            self.chapterallindex_list[i] = chapterallindexlist[i]["chapterallindex"]
            i += 1
        self.chapterallindex = choice(self.chapterallindex_list)

    def readChapter(self):
        url = f"https://10010.woread.com.cn/ng_woread_service/rest/cnt/readChapter?catid={self.catid}&chapterallindex={self.chapterallindex}&cardid={self.cardid}&cntindex={self.cntindex}&chapterseno=1"
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        crypt_text = f'{{"chapterSeno":1,"cntIndex":"{self.cntindex}","beginChapter":4,"timestamp":"{date}","token":"{self.userinfo["token"]}","userId":"{self.userinfo["userid"]}","userIndex":{self.userinfo["userindex"]},"userAccount":"{self.userinfo["phone"]}","verifyCode":"{self.userinfo["verifycode"]}"}}'
        data = self.req(url, crypt_text)
        if "chapterid" in data["list"][0] and data["list"][0]["chapterid"]:
            self.chapterid = data["list"][0]["chapterid"]
            print(f"chapterid:{self.chapterid}\n")
        else:
            self.chapterid = self.cntindex + "001"

    def query_red(self):
        global msg_str  
        url = "https://10010.woread.com.cn/ng_woread_service/rest/phone/vouchers/queryTicketAccount"
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        crypt_text = f'{{"timestamp":"{date}","token":"{self.userinfo["token"]}","userId":"{self.userinfo["userid"]}","userIndex":{self.userinfo["userindex"]},"userAccount":"{self.userinfo["phone"]}","verifyCode":"{self.userinfo["verifycode"]}"}}'
        data = self.req(url, crypt_text)
        if data["code"] == "0000":
            can_use_red = data["data"]["usableNum"] / 100
            if can_use_red >= 3:
                self.printAndMsg(f"账号{self.phone_num}查询成功 你当前有话费红包{can_use_red} 可以去兑换了")
            else:
                self.printAndMsg(f"账号{self.phone_num}查询成功 你当前有话费红包{can_use_red} 不足兑换的最低额度")

    def main(self):
        self.referer_login()
        self.get_userinfo()
        if not self.get_activetion_id():
            self.joinRuning()
            self.get_activetion_id()
        self.read_novel()
        self.query_red()


def start(phone, run_ua):
    if phone == "":
        print("没有用户")
        exit(0)
    China_Unicom(phone, run_ua).main()
    print("\n")
    print("\n")

if __name__ == "__main__":
    unicom_lotter = ""
    """读取环境变量"""
    l = []
    user_map = []
    cklist = get_cookie("PHONE_NUM")
    for i in range(len(cklist)):
        # 以#分割开的ck
        split1 = cklist[i].split("&")
        if len(split1) > 1:
            for j in range(len(split1)):
                user_map.append(split1[j])
        else:
            user_map.append(cklist[i])

    for i in range(len(user_map)):
        phone = ""
        info = user_map[i].split("&")[0]
        # 以#分割开的ck
        split1 = info.split("#")
        run_ua = ""
        phone = split1[0]
        if len(split1) > 1:
            run_ua = split1[1] + \
                f";devicetype{{deviceBrand:,deviceModel:}};{{yw_code:}}"

        print('开始执行第{}个账号：{}'.format((i+1), phone))
        if phone == "":
            print("当前账号未填写手机号 跳过")
            print("\n")
            continue
        p = threading.Thread(target=start, args=(phone, run_ua))
        l.append(p)
        p.start()
        print("\n")
    for i in l:
        sleep(uniform(20, 80))
        i.join()
    send("联通阅读", msg_str)
