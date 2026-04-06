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
import os
from tools.githubFile import GithubFile
from datetime import datetime,date
from decimal import Decimal
from notify import send

# 豪猪配置
haozhu_cookie = os.environ["haozhucookie"]
haozhu_projectdata = GithubFile('豪猪/projectdata.json')

  
token = 'eD/rrPvm7dDgzG8JXTUcu792PQ/c8e08bx7J7IOldlgLA2k5w ACe6zFz4FaU9pQKk1fm3VfaGH8i9aZ67K1U7EePTGS2ndOeis7sY4en4X02vT0xcI1qT59cIjKQIJpdAdG/pLURTlC Ztmvg1SNJcuSxXn6tkhkYGfwKJssUU=;'
request_count = 0

def rts(url, method='GET', resp_type='json', **kwargs):
    global request_count
    request_count += 1
    time.sleep(2)
    try:
        r = requests.request(method.upper(), url, timeout=10, **kwargs)
        r.raise_for_status()
        return r.json() if resp_type == 'json' else r.text
    except Exception as e:
        print(f"Error: {e}")
        return None

class HaoZhu:
    def __init__(self, cookie):
        self.cookie = cookie # 调用haozhu_api后会延长cookie有效期
        self.host = 'h5.haozhuma.cn'
        self.host2 = 'api.haozhuma.cn'
        self.RemoveLxfs = ["88888888888", "nezha77", "Szldh", "smsgfc", "zhgy888", "@cjang888", "cjang888", "jings888", "cocodou888", "yy2438"] # 查询项目时屏蔽的卡商ID
        self.RemoveSheng = ["江西"] # 查询项目时屏蔽的省
        self.use_quantity = 0
        self.use_money = Decimal('0')
        self.token = self.haozhu_api()
        if self.token:
            self.getSummary(self.token) # 查询余额
            #self.get_expenses() # 查询当日消费记录
            self.my_ydj: list[dict] = self.get_ydj() # 查询已对接的对接码(去除已暂停)
        else:
            exit()
            
    def headers(self):
        headers = {
            'Host': self.host,
            'User-Agent':'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36',
            'Cookie': self.cookie
        }
        return headers

    # 刷新token，同样会延长cookie时间        
    def haozhu_api(self):
        url = f'https://{self.host}/api.php'
        headers = self.headers()
        result = rts(url, headers=headers, allow_redirects=False)
        if result is None:
            exit()
        if result['code'] == 1:
            return result['token']
        else:
            print(result)
            send('豪猪', 'cookie失效')
            return False

    # 查询余额     
    def getSummary(self, token):
        url = f'https://{self.host2}/sms/?api=getSummary&token={token}'
        headers = {
            'Host': self.host2,
            'User-Agent':'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36'
        }
        result = rts(url, headers=headers)
        if result is None:
            exit()
        if result['code'] == 0:
            print(f"当前余额：{result['money']}")
        else:
            print(result)
    
    # 查询加入的对接码，并且状态是已对接的，自动删除可用数量不足的对接码
    def get_ydj(self) -> list[dict]:
        page = 1
        data = []
        max_pages = 50  # 安全限制
        headers = self.headers()
        while page <= max_pages:
            url = f'https://{self.host}/api.php?type=3&gjc=&page={page}'
            result = rts(url, headers=headers)
            if result is None:
                exit()
            if result['data'] is None:
                break
            for item in result['data']:
                zx = int(item['zxky'].split('/')[0].split(':')[1])
                ky = int(item['zxky'].split('/')[1].split(':')[1])
                if item['djzt'] == '已对接' and ky > 0:
                    data.append(item)
                    continue
                if item['djzt'] == '已对接' and ky == 0:
                    print(f"删除对接码：{item['mc']}----{item['uid']}（{item['zxky']}，价格:{item['yhj']}）")
                    self.del_uid(item['uid'])
            page += 1
        return data

    # 删除对接码
    def del_uid(self, uid):
        url = f'https://{self.host}/api.php?type=41&open=del&uid={uid}'
        headers = self.headers()
        result = rts(url, headers=headers)
        if result is None:
            exit()
        print(result['msg'])
        print(f"{'-'*40}")
    
    # 搜索项目公开对接码
    def get_project_uid(self, sid, sim_type):
        url = f'https://{self.host}/api.php?type=8&sid={sid}'
        headers = self.headers()
        result = rts(url, headers=headers)
        if result is None:
            exit()
        if result['code'] != 1:
            print(url)
            print(result)
            exit()
        new_data = []
        for item in result['data']:
            zx = int(item['zxky'].split('/')[0].split(':')[1])
            ky = int(item['zxky'].split('/')[1].split(':')[1])
            if ky <= 10 or (ky / zx) <= 0.2: # 如果 ky（可用数量）小于等于 10，或者（or） ky / zx 的比例小于等于 0.2，就跳过这条数据。
                continue
            if not any(s in item['yyy'] for s in sim_type): # 遍历 sim_type（比如 ['移动', '联通']），检查 item['yyy'] 里有没有包含它们。如果一个都没包含（not any），就跳过这条数据。
                continue
            if any(s in item['sheng'] for s in self.RemoveSheng): # 遍历黑名单 self.RemoveSheng（比如 ['北京', '上海']），只要发现 item['sheng'] 中包含了黑名单里的任何一个省份（any），就跳过这条数据。
                continue
            if item['lxfs'] in self.RemoveLxfs: # item的卡商用户名存在于RemoveLxfs中，则运行
                continue
            if item['hd'][0] != '1': # 号段开头不等于1，则运行
                continue
            new_data.append(item)
        sorted_data = sorted(new_data, key=lambda x: float(x['yhj']))
        return sorted_data
    
    # 加入对接码
    def add_uid(self, djm):
        url = f'https://{self.host}/api.php?type=4&djm={djm}'
        headers = self.headers()
        result = rts(url, headers=headers)
        if result is None:
            exit()
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
            headers = self.headers()
            result = rts(url, headers=headers)
            if result is None:
                exit()
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
    haozhu = HaoZhu(haozhu_cookie)
    for i in haozhu_projectdata.cont:
        if i['haozhu']['zddj']:
            haozhu.main(i['haozhu'])
        else:
            print(f"{i['project_name']}：自动对接已关闭")
            print(f"{'-'*40}")
    haozhu.process_and_print(haozhu.my_ydj) # 打印已对接的对接码
    print(f"总请求数量：{request_count}")
