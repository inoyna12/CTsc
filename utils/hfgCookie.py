#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/7/6 23:00
# @Author  : HarbourJ
# @TG      : https://t.me/HarbourToulu
# @File    : hfgCookie.py

import os
import time


def get_cookies():
    CookieJDs = []
    if os.environ.get("HFG_COOKIE"):
        print("已获取并使用Env环境 Cookie")
        if '&' in os.environ["HFG_COOKIE"]:
            CookieJDs = os.environ["HFG_COOKIE"].split('&')
        elif '\n' in os.environ["HFG_COOKIE"]:
            CookieJDs = os.environ["HFG_COOKIE"].split('\n')
        else:
            CookieJDs = [os.environ["HFG_COOKIE"]]
        # return CookieJDs
    else:
        if os.path.exists("HFG_COOKIE.txt"):
            with open("HFG_COOKIE.txt", 'r') as f:
                HFG_COOKIEs = f.read().strip()
                if HFG_COOKIEs:
                    if '&' in HFG_COOKIEs:
                        CookieJDs = HFG_COOKIEs.split('&')
                    elif '\n' in HFG_COOKIEs:
                        CookieJDs = HFG_COOKIEs.split('\n')
                    else:
                        CookieJDs = [HFG_COOKIEs]
                    CookieJDs = sorted(set(CookieJDs), key=CookieJDs.index)
                    # return CookieJDs
        else:
            print("未获取到正确✅格式的联通账号Cookie")
            return

    print(f"====================共{len(CookieJDs)}个联通账号Cookie=========\n")
    print(f"==================脚本执行- 北京时间(UTC+8)：{time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}=====================\n")
    return CookieJDs

# if __name__ == "__main__":
#     get_cookies()
#     print(os.environ.get("HFG_COOKIE"))