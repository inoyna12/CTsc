import requests 
import json
from datetime import datetime
from decimal import Decimal
from notify import send

cookie = 'PHPSESSID=g30b2dhlthv2i7lg1lih2vd9l3; sl-session=C04iQorRsWhxEGQZB5XWag=='
token = 'eD/rrPvm7dDgzG8JXTUcu792PQ/c8e08bx7J7IOldlgLA2k5w+ACe6zFz4FaU9pQKk1fm3VfaGH8i9aZ67K1U7EePTGS2ndOeis7sY4en4X02vT0xcI1qT59cIjKQIJpdAdG/pLURTlC+Ztmvg1SNJcuSxXn6tkhkYGfwKJssUU='

class HaoZhu:
    def __init__(self, cookie):
        self.cookie = cookie
        self.host = 'h5.haozhuyun.com'
        self.use_quantity = 0
        self.use_money = Decimal(0)
    
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
    
    # 查询加入的对接码
    def get_docked(self):
        page = 1
        docked_list = []
        while True:
            url = f'https://{self.host}/api.php?type=3&gjc=&page={page}'
            result = requests.get(url, headers=self.headers()).json()
            if result['data'] is None:
                break 
            docked_list.extend(result['data'])
            page += 1
        return docked_list

    # 删除对接码
    def del_uid(self, uid):
        url = f'https://{self.host}/api.php?type=41&open=del&uid={uid}'
        result = requests.get(url, headers=self.headers()).json()
        print(result['msg'])

    # 删除对接码
    def ydj_del_uid(self):
        json_data = self.get_docked()
        for item in json_data:
            if item['djzt'] == '已对接':
                parts = item['zxky'].split('/')
                zx = parts[0].split(':')[1]
                ky = parts[1].split(':')[1]
                if int(ky) == 0:
                    print(item)
                    self.del_uid(item['uid'])
        
    def statistics_docked(self):
        json_data = self.get_docked()
        stats = {}
        # 遍历data列表中的每个字典元素
        for item in json_data:
            # 检查'djzt'键的值是否为'已对接'
            if item.get('djzt') == '已对接':
                mc = item.get('mc')
                zxky = item.get('zxky')
                
                # 提取'zxky'中的可用数量
                available_count = 0
                if zxky and '可用:' in zxky:
                    try:
                        # 分割字符串以获取数字部分
                        count_str = zxky.split('可用:')[1]
                        available_count = int(count_str)
                    except (IndexError, ValueError):
                        # 如果格式不正确或无法转换为整数，则保持为0
                        available_count = 0
                
                # 如果mc键值是第一次出现，则在stats字典中创建新条目
                if mc not in stats:
                    stats[mc] = {
                        'mc_count': 1,
                        'available_total': available_count
                    }
                # 如果mc键值已存在，则更新计数和总数
                else:
                    stats[mc]['mc_count'] += 1
                    stats[mc]['available_total'] += available_count
        # 将统计结果从字典转换为列表格式
        result_list = []
        for mc, data in stats.items():
            result_list.append({
                "mc": mc,
                "djsl": data['mc_count'],
                "kysl": data['available_total']
            })
        list1 = []
        for i in result_list:
            str1 = f"{i['mc']}：已对接{i['djsl']}，可用号码{i['kysl']}"
            print(str1)
            if i['djsl'] < 2 or i['kysl'] < 100:
                list1.append(str1)
        send('豪猪', '\n'.join(list1))
    
 
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
              
    def main(self):
        if self.haozhu_api():
            self.get_expenses()
            self.ydj_del_uid()
            self.statistics_docked()

class YeZiYun:
    def __init__(self, token):
        self.token = token
        self.host = 'az.yezi56.com:90'
        self.use_quantity = 0
        self.use_money = Decimal(0)
    
    def headers(self):
        headers = {
            'Host': self.host,
            'Content-Length': '0'
        }
        return headers    
                
    # 获取消费记录
    def get_expenditure(self):
        url = f"http://{self.host}/api/get_expenditure"
        index = 0
        today_date = datetime.date.today()
        while True:
            data = {
                "token": self.token,
                "index": str(index)
            }
            result = requests.get(url, headers=self.headers()).json()
            if result['data'] is None:
                break 
            for data in result['data']:
                data_time = datetime.date.fromtimestamp(int(data['time']))
                if today_date == data_time:
                    self.use_quantity += 1
                    self.use_money += Decimal(data['money'])
                index += 40
        print(f"椰子云：消费数量{self.use_quantity}\n椰子云：消费金额{self.use_money}")
            
        def main(self):
            self.get_expenditure()
        
haozhu = HaoZhu(cookie)
haozhu.main()

yeziyun = YeZiYun(token)
yeziyun.main()
