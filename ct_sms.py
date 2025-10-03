import requests 
import json
import time
from datetime import datetime,date
from decimal import Decimal
from notify import send

cookie = 'PHPSESSID=g30b2dhlthv2i7lg1lih2vd9l3; sl-session=C04iQorRsWhxEGQZB5XWag==' #zhou808080
token = 'eD/rrPvm7dDgzG8JXTUcu792PQ/c8e08bx7J7IOldlgLA2k5w ACe6zFz4FaU9pQKk1fm3VfaGH8i9aZ67K1U7EePTGS2ndOeis7sY4en4X02vT0xcI1qT59cIjKQIJpdAdG/pLURTlC Ztmvg1SNJcuSxXn6tkhkYGfwKJssUU=;'

class HaoZhu:
    def __init__(self, cookie):
        self.cookie = cookie
        self.host = 'h5.haozhuyun.com'
        self.RemoveLxfs = ["88888888888", "nezha77"]
        self.use_quantity = 0
        self.use_money = Decimal(0)
        if self.haozhu_api():
           self.my_ydj: list[dict] = self.get_ydj()
           self.get_expenses()
    
    def headers(self):
        headers = {
            'Host': self.host,
            'Cookie': self.cookie
        }
        return headers

    # 延长cookie时间        
    def haozhu_api(self):
        url = f'https://{self.host}/api.php'
        result = requests.get(url, headers=self.headers(), allow_redirects=False).json()
        if result['code'] == 1:
            return True
        else:
            print(result)
            send('豪猪', 'cookie失效')
            return False
    
    # 查询加入的对接码，并且状态是已对接的，自动删除可用数量不足的对接码
    def get_ydj(self) -> list[dict]:
        page = 1
        data = []
        while True:
            url = f'https://{self.host}/api.php?type=3&gjc=&page={page}'
            result = requests.get(url, headers=self.headers()).json()
            if result['data'] is None:
                break 
            for item in result['data']:
                if item['djzt'] == '已对接':
                    ky = int(item['zxky'].split('/')[1].split(':')[1])
                    if ky == 0:
                        print(f"删除对接码：{item['uid']}（{item['zxky']}，价格:{item['yhj']}）")
                        self.del_uid(item['uid'])
                    else:
                        data.append(item)
            page += 1
        return data

    # 删除对接码
    def del_uid(self, uid):
        url = f'https://{self.host}/api.php?type=41&open=del&uid={uid}'
        result = requests.get(url, headers=self.headers()).json()
        print(result['msg'])
    
    # 搜索项目公开对接码
    def get_project_uid(self, sid, sim_type):
        url = f'https://{self.host}/api.php?type=8&sid={sid}'
        result = requests.get(url, headers=self.headers()).json()
        if result['msg'] != "Success":
            return []
        new_data = []
        for item in result['data']:
            zx = int(item['zxky'].split('/')[0].split(':')[1])
            ky = int(item['zxky'].split('/')[1].split(':')[1])
            if ky > 10 and ky / zx > 0.2 and any(s in item['yyy'] for s in sim_type) and item['lxfs'] not in self.RemoveLxfs and item['hd'][0] == '1':
                new_data.append(item)
        sorted_data = sorted(new_data, key=lambda x: float(x['yhj']))
        return sorted_data
    
    # 加入对接码
    def join_uid(self, djm):
        url = f'https://{self.host}/api.php?type=4&djm={djm}'
        result = requests.get(url, headers=self.headers()).json()
        print(result['msg']) 
           
    # 查询当日消费记录
    def get_expenses(self):
        nowdate = datetime.now().strftime('%Y-%m-%d')
        page = 1
        while True:
            url = f'https://{self.host}/api.php?type=9&page={page}&rq={nowdate}&sid=&uid=&phone='
            result = requests.get(url, headers=self.headers()).json()
            if result['data'] is None:
                break 
            self.use_quantity = result['total']
            for i in result['data']:
                self.use_money += Decimal(i['dj'])
            page += 1
        print(f"豪猪：消费数量{self.use_quantity}\n豪猪：消费金额{self.use_money}")
        print(f"{'-'*45}")

    # 自动对接
    def zddj(self, data):
        ydjsl = 0
        kysl = 0
        for item in self.my_ydj:
            if data['sid'] in item['mc']:
                print(f"{item['uid']}（{item['zxky']}，价格:{item['yhj']}）")
                ydjsl += 1
                kysl += int(item['zxky'].split('/')[1].split(':')[1])
        if ydjsl >= data['ydjsl'] and kysl >= data['kysl']:
            print(f"可用对接数量：{ydjsl}，可用号码数量：{kysl}")
            return
        
        uids_data = self.get_project_uid(data['search_sid'], data['sim_type'])
        for uids in uids_data:
            print(f"添加对接码：{uids['uid']}（{uids['zxky']}，价格:{uids['yhj']}）")
            self.join_uid(uids['uid'])
            ydjsl += 1
            kysl += int(uids['zxky'].split('/')[1].split(':')[1])
            if ydjsl >= data['ydjsl'] and kysl >= data['kysl']:
                print(f"可用对接数量：{ydjsl}，可用号码数量：{kysl}")
                return

    # 主线程                    
    def main(self, data: dict):
        self.zddj(data)

class YeZiYun:
    def __init__(self, token):
        self.token = token
        self.host = 'az.yezi56.com:90'
        self.use_quantity = 0
        self.use_money = Decimal(0)
    
    def headers(self):
        headers = {
            'Host': self.host,
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36 EdgA/132.0.0.0",
            'Accept': "application/json, text/plain, */*",
            'Accept-Encoding': "gzip, deflate",
            'Origin': "http://h5.yezi66.net:90",
            'X-Requested-With': "mark.via",
            'Referer': "http://h5.yezi66.net:90/",
            'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        return headers    
                
    # 获取消费记录
    def get_expenditure(self):
        url = f"http://{self.host}/api/get_expenditure"
        index = 0
        today_date = date.today()
        stop_while = True
        while stop_while:
            payload = {
                'token': f"{self.token}index={index}"
            }
            result = requests.post(url, headers=self.headers(), data=payload)
            if result.status_code != 200:
                return
            result = result.json()
            if result['data'] == []:
                break 
            for data in result['data']:
                data_time = date.fromtimestamp(int(data['time']) - 28800)
                if today_date == data_time:
                    self.use_quantity += 1
                    self.use_money -= Decimal(data['money'])
                else:
                    stop_while = False
                    break
            index += 40
        print(f"椰子云：消费数量{self.use_quantity}\n椰子云：消费金额{self.use_money}")
            
    def main(self):
        self.get_expenditure()

if __name__ == '__main__':
    with open('sms/data.json', 'r', encoding='utf-8') as f:
        deploy_data = json.load(f)
    haozhu = HaoZhu(cookie)
    for data in deploy_data:
        if data['haozhu']['zddj']:
            print(f"{data['project_name']}：")
            haozhu.main(data['haozhu'])
        else:
            print(f"{data['project_name']}：自动对接已关闭")
        print(f"{'-'*45}")
 
    yeziyun = YeZiYun(token)
    yeziyun.main()

print(f'总消费数量{haozhu.use_quantity + yeziyun.use_quantity}\n总消费金额{Decimal(haozhu.use_money) + Decimal(yeziyun.use_money)}')
