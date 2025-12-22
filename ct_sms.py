'''
sms对接价格最低的对接码

已对接的对接码信息  列表A
可对接的对接码信息  列表B
合并AB变成C  从小到大排序

初始化：已对接数量0 已对接号码0

for循环C判断对接

    判断已对接数量和已对接号码数量是否足够

    如果已对接：
        删除列表A中的已对接元素
   如果未对接：
        启动对接

   数量加上 

for循环A列表取消对接
        
'''

import requests 
import json
import time
from datetime import datetime,date
from decimal import Decimal
from notify import send

cookie = 'PHPSESSID=409rspqv2un57n4fm1pldfqc91; sl-session=QS2BcNktSWkNwwsDBaqYUQ==' #zhou808080
token = 'eD/rrPvm7dDgzG8JXTUcu792PQ/c8e08bx7J7IOldlgLA2k5w ACe6zFz4FaU9pQKk1fm3VfaGH8i9aZ67K1U7EePTGS2ndOeis7sY4en4X02vT0xcI1qT59cIjKQIJpdAdG/pLURTlC Ztmvg1SNJcuSxXn6tkhkYGfwKJssUU=;'

class HaoZhu:
    def __init__(self, cookie):
        self.cookie = cookie # 调用haozhu_api后会延长cookie有效期
        self.host = 'h5.haozhuyun.com'
        self.RemoveLxfs = ["88888888888", "nezha77", "Szldh", "gzgfc"] # 查询项目时屏蔽的卡商ID
        self.use_quantity = 0
        self.use_money = Decimal('0')
        self.token = self.haozhu_api()
        if self.token:
            self.getSummary(self.token) # 查询余额
            self.get_expenses() # 查询当日消费记录
            self.my_ydj: list[dict] = self.get_ydj() # 查询已对接的对接码(去除已暂停)
        else:
            exit()
            
    def headers(self):
        headers = {
            'Host': self.host,
            'Cookie': self.cookie
        }
        return headers

    # 延长cookie时间        
    def haozhu_api(self):
        url = f'https://{self.host}/api.php'
        response = requests.get(url, headers=self.headers(), allow_redirects=False)
        if response.status_code != 200:
            print(f"请求失败，状态码：{response.status_code}")
            print("响应内容：", response.text)
            return False
        result = response.json()
        if result['code'] == 1:
            return result['token']
        else:
            print(result)
            send('豪猪', 'cookie失效')
            return False

    # 查询余额     
    def getSummary(self, token):
        url = f'https://api.haozhuwang.com/sms/?api=getSummary&token={token}'
        headers = {
            'Host': 'api.haozhuwang.cn'
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"请求失败，状态码：{response.status_code}")
            print("响应内容：", response.text)
            return False
        result = response.json()
        if result['code'] == 0:
            print(f"当前余额：{result['money']}")
        else:
            print(result)
    
    # 查询加入的对接码，并且状态是已对接的，自动删除可用数量不足的对接码
    def get_ydj(self) -> list[dict]:
        page = 1
        data = []
        max_pages = 50  # 安全限制
        while page <= max_pages:
            url = f'https://{self.host}/api.php?type=3&gjc=&page={page}'
            response = requests.get(url, headers=self.headers())
            if response.status_code != 200:
                print(f"请求失败，状态码：{response.status_code}")
                print("响应内容：", response.text)
                return False
            result = response.json()
            if result['data'] is None:
                break 
            for item in result['data']:
                if item['djzt'] == '已对接':
                    ky = int(item['zxky'].split('/')[1].split(':')[1])
                    if ky == 0:
                        # if '沐瞳科技' in item['mc']:
                        #     print('沐瞳科技暂不删除')
                        #     continue
                        print(f"删除对接码：{item['mc']}----{item['uid']}（{item['zxky']}，价格:{item['yhj']}）")
                        self.del_uid(item['uid'])
                    else:
                        data.append(item)
            page += 1
            time.sleep(2)
        return data

    # 删除对接码
    def del_uid(self, uid):
        url = f'https://{self.host}/api.php?type=41&open=del&uid={uid}'
        result = requests.get(url, headers=self.headers()).json()
        print(result['msg'])
        print(f"{'-'*40}")
    
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
    def add_uid(self, djm):
        url = f'https://{self.host}/api.php?type=4&djm={djm}'
        result = requests.get(url, headers=self.headers()).json()
        print(result['msg']) 
        print(f"{'-'*40}")
           
    # 查询当日消费记录
    def get_expenses(self):
        nowdate = datetime.now().strftime('%Y-%m-%d')
        stats = {}
        result_list = []
        page = 1
        max_pages = 100  # 安全限制
        while page <= max_pages:
            url = f'https://{self.host}/api.php?type=9&page={page}&rq={nowdate}&sid=&uid=&phone='
            result = requests.get(url, headers=self.headers()).json()
            if result['data'] is None:
                break 
            self.use_quantity = result['total']
            for item in result['data']:
                mc = item['mc']
                dj = Decimal(item['dj'])
                self.use_money += dj
            
                if mc not in stats:
                    stats[mc] = {
                        'quantity': 1,
                        'money': dj
                    }
                else:
                    stats[mc]['quantity'] += 1
                    stats[mc]['money'] += dj
            page += 1
            time.sleep(2)
        
        print(f"消费数量：{self.use_quantity}，消费金额：{self.use_money}")
        print(f"{'-'*40}")

        for mc, data in stats.items():
            result_list.append({
                "mc": mc,
                "quantity": data['quantity'],
                "money": data['money']
            })
        sorted_result = sorted(result_list, key=lambda x: x['quantity'], reverse=True)
        for item in sorted_result:
            print(f"项目: {item['mc']}, 数量: {item['quantity']}, 金额: {item['money']}")

        print(f"{'-'*40}")

    # 自动对接（data为自动对接的配置参数，my_ydj为已对接的对接码）
    def zddj(self, my_ydj, data):
        ydjsl = 0 # 已对接的对接码数量
        kysl = 0 # 已对接的可用号码数量
        for item in my_ydj:
            # 判断配置文件中的项目名称是否在已对接的对接码中，如果存在就把已对接的对接码数量和可用号码数量加起来
            if data['sid'] in item['mc']:
                ydjsl += 1
                kysl += int(item['zxky'].split('/')[1].split(':')[1])

        # 判断已对接的对接码数量和可用号码数量是否满足配置文件中的要求，如果满足就退出                
        if ydjsl >= data['ydjsl'] and kysl >= data['kysl']:
            return
        
        # 查询项目公开对接码
        uids_data = self.get_project_uid(data['search_sid'], data['sim_type'])

        # 加入对接码，加入后添加到my_ydj中，直到满足配置文件中的要求为止
        for uids in uids_data:
            print(f"添加对接码：{uids['mc']}----{uids['uid']}（{uids['zxky']}，价格:{uids['yhj']}）")
            self.add_uid(uids['uid'])
            ydjsl += 1
            kysl += int(uids['zxky'].split('/')[1].split(':')[1])
            my_ydj.append(uids)
            if ydjsl >= data['ydjsl'] and kysl >= data['kysl']:
                return

    # 打印已对接的对接码
    def process_and_print(self, data):
        # 1. 分组：将数据按名称 (mc) 归类
        grouped_data = {}
        for item in data:
            name = item['mc']
            if name not in grouped_data:
                grouped_data[name] = []
            grouped_data[name].append(item)

        # 2. 准备排序用的列表
        # 结构：[ {'name': 名称, 'items': [项目列表], 'max_price': 该组最高价}, ... ]
        sorted_groups = []

        for name, items in grouped_data.items():
            # 先对组内的项目按价格降序排序
            items.sort(key=lambda x: float(x['yhj']), reverse=True)
            
            # 获取该组中最高的一个价格，用于组与组之间的排序
            max_price = float(items[0]['yhj']) if items else 0
            
            sorted_groups.append({
                'name': name,
                'items': items,
                'max_price': max_price
            })

        # 3. 对组进行排序：按 'max_price' 从高到低排
        sorted_groups.sort(key=lambda x: x['max_price'], reverse=True)

        # 4. 格式化打印
        for group in sorted_groups:
            print(f"\n{group['name']}：")

            total_available = 0  # 统计可用号码数量
            items = group['items']
            
            for item in items:
                uid = item['uid']
                zxky = item['zxky']
                price = item['yhj']
                
                # 打印单行详情
                print(f"{uid}（{zxky}，价格:{price}）")
                
                # 提取"可用"后面的数字进行累加
                total_available += int(zxky.split('/')[1].split(':')[1])

            # 打印统计信息
            print(f"可用对接数量：{len(items)}，可用号码数量：{total_available}")
            print(f"\n{'-'*40}")   

    # 主线程                    
    def main(self, data: dict):
        self.zddj(self.my_ydj, data) # 自动对接

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
            haozhu.main(data['haozhu'])
        else:
            print(f"{data['project_name']}：自动对接已关闭")
            print(f"{'-'*40}")
    haozhu.process_and_print(haozhu.my_ydj) # 打印已对接的对接码
