import requests 
import json
from datetime import datetime
from decimal import Decimal
from notify import send

cookie = 'PHPSESSID=g30b2dhlthv2i7lg1lih2vd9l3; sl-session=MM8bSw/nr2j43G0frZqSZw=='

class HaoZhu:
    def __init__(self, cookie):
        self.cookie = cookie
    
    def headers(self):
        headers = {
            'Host': 'h5.haozhuyun.com',
            'Cookie': self.cookie
        }
        return headers

    # 延长cookie时间        
    def haozhu_api(self):
        url = 'https://h5.haozhuyun.com/api.php'
        result = requests.get(url, headers=self.headers()).json()
        if result['code'] == 1:
            return True
        else:
            print(result)
            return False
    
    # 查询加入的对接码
    def get_docked(self):
        page = 1
        docked_list = []
        while True:
            url = f'https://h5.haozhuyun.com/api.php?type=3&gjc=&page={page}'
            result = requests.get(url, headers=self.headers()).json()
            if result['data'] is None:
                break 
            docked_list.extend(result['data'])
            page += 1
        return docked_list
        
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
            if i['djsl'] < 3 or i['kysl'] < 100:
                list1.append(str1)
        send('豪猪', '\n'.join(list1))
    
 
    # 查询当日消费记录
    def get_expenses(self):
        nowdate = datetime.now().strftime('%Y-%m-%d')
        page = 1
        money = Decimal(0)
        while True:
            url = f'https://h5.haozhuyun.com/api.php?type=9&page={page}&rq={nowdate}&sid=&uid=&phone='
            result = requests.get(url, headers=self.headers()).json()
            if result['data'] is None:
                break 
            total = result['total']
            for i in result['data']:
                money += Decimal(i['dj'])
            page += 1
        print(f"当日消费数量{total}\n当日消费金额{money}")
              
    def main(self):
        if self.haozhu_api():
            self.get_expenses()
            self.statistics_docked()
        
haozhu = HaoZhu(cookie)
haozhu.main()