'''
{'sid': '76980', 'mc': '[76980]海马云', 'uid': '76980-3BLHWSGDGM', 'yhj': '0.330', 'zxky': '可用数量:147', 'yyy': '电信|移动|', 'sheng': '|广东', 'haoduan': '正常号段', 'hd': '199|191|190|189|181|136|135|', 'lxfs': 'tonghua66', 'minute': None, 'open': '0', 'time': '2025-05-25 18:11:50', 'zd': '1'}
{'sid': '76980', 'mc': '[76980]海马云', 'uid': '76980-WIIB6H70AG', 'yhj': '11.000', 'zxky': '可用数量:61', 'yyy': '移动|', 'sheng': '广东', 'haoduan': '正常号段', 'hd': '198|188|158|157|150|139|138|137|136|135|134|', 'lxfs': '未留', 'minute': None, 'open': '0', 'time': '2026-02-04 21:33:28', 'zd': '0'}
        
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
cookie = os.environ["haozhucookie"]
hz_config = GithubFile('豪猪/config.json').cont
notAdd_lxfs = hz_config['notAdd_lxfs']
notAdd_sheng = hz_config['notAdd_sheng']

request_count = 0

def rts(url, method='GET', resp_type='json', **kwargs):
    global request_count
    request_count += 1
    time.sleep(5)
    try:
        r = requests.request(method.upper(), url, timeout=20, **kwargs)
        r.raise_for_status()
        return r.json() if resp_type == 'json' else r.text
    except Exception as e:
        print(f"Error: {e}")
        print(url)
        exit()
        return None

class HaoZhu:
    def __init__(self, cookie):
        self.cookie = cookie # 调用haozhu_api后会延长cookie有效期
        self.host = 'h5.haozhuma.cn'
        self.host2 = 'api.haozhuma.cn'
        self.use_quantity = 0
        self.use_money = Decimal('0')
        self.token = self.haozhu_api()
            
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
            exit()

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
    
    # 查询加入的对接码
    def get_ydj(self, gic, page=1) -> list[dict]:
        data = []
        headers = self.headers()
        for i in range(page):
            url = f'https://{self.host}/api.php?type=3&gjc={gic}&page={i+1}'
            result = rts(url, headers=headers)
            if result['data'] is None:
                break
            data.extend(result['data'])  #追加到data列表末尾中
        return data

    # 更新已对接的对接码
    def update_ydj(self, ydj):
        data = []
        for i in ydj:
            ky = int(i['zxky'].split(':')[-1])
            if i['djzt'] == '已对接' and ky > 0:
                data.append(i)
                continue
            #if ky == 0:
            if i['djzt'] == '已对接' and ky == 0:
                print(f"删除对接码：{i['mc']}----{i['uid']}（{i['zxky']}，价格:{i['yhj']}）")
                self.del_uid(i['uid'])
        return data

    # 删除对接码
    def del_uid(self, uid):
        url = f'https://{self.host}/api.php?type=41&open=del&uid={uid}'
        headers = self.headers()
        result = rts(url, headers=headers)
        if result is None:
            exit()
        print(f"删除对接码：{uid}")
        print(result['msg'])
    
    # 搜索项目公开对接码
    def get_project_uid(self, sid, not_hd_list):
        url = f'https://{self.host}/api.php?type=8&sid={sid}'
        headers = self.headers()
        result = rts(url, headers=headers)
        if result['data'] is None:
            print(url)
            print(result)
            exit()
        new_data = []
        for item in result['data']:
            ky = int(item['zxky'].split(':')[-1])
            hd_list = item['hd'].strip('|').split('|')
            if ky <= 50: #可用数量不足跳过
                continue
            if set(hd_list).issubset(set(not_hd_list)): # 判断对接码的列表号段元素是否全部存在于not_hd_list列表中，如果全部存在则跳过
                continue
            if any(s in item['sheng'] for s in notAdd_sheng): # 遍历黑名单 self.RemoveSheng（比如 ['北京', '上海']），只要发现 item['sheng'] 中包含了黑名单里的任何一个省份（any），就跳过这条数据。
                continue
            if item['lxfs'] in notAdd_lxfs: # item的卡商用户名存在于RemoveLxfs中，则运行
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

    # 自动对接（config为自动对接的配置参数，my_ydj为已对接的对接码）
    def zddj_1(self, ydj_list, config):
        ydjsl = 0 # 已对接的对接码数量
        kysl = 0 # 已对接的可用号码数量
        
        for d in ydj_list:
            zxky = int(d['zxky'].split(':')[-1])
            ydjsl += 1
            kysl += zxky
            all_ydj.append(d)
            if ydjsl >= config['ydjsl'] and kysl >= config['kysl']:
                return
                
        uid_config_list = self.get_project_uid(config['search_sid'], config['notAdd_hd'])
        for dd in uid_config_list:
            print(f"添加对接码：{dd['mc']}----{dd['uid']}（{dd['zxky']}，价格:{dd['yhj']}）")
            self.add_uid(dd['uid'])
            zxky = int(dd['zxky'].split(':')[-1])
            ydjsl += 1
            kysl += zxky
            all_ydj.append(dd)
            if ydjsl >= config['ydjsl'] and kysl >= config['kysl']:
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
                total_available += int(zxky.split(':')[-1])

            # 打印统计信息
            print(f"可用对接数量：{len(items)}，可用号码数量：{total_available}")
            print(f"\n{'-'*40}")   


        
    def check_hd(self, ydj_list, not_hd_list):
        new_ydj_list = []
        for d in ydj_list:
            if d['hd'] is None:
                new_ydj_list.append(d)
                continue
            hd_list = d['hd'].strip('|').split('|')
            
            # 判断hd_list的任意一个元素是否不存在于not_hd_list，如果有一个不存在，则返回true
            if any(i not in not_hd_list for i in hd_list):
                new_ydj_list.append(d)
            else:
                print(f"{d['uid']}：{d['hd']}")
                print("号段不符合，删除")
                self.del_uid(d['uid'])
        return new_ydj_list
        
    def zddj_2(self, ydj_list, config):
        ydjsl = 0 # 已对接的对接码数量
        kysl = 0 # 已对接的可用号码数量
        list1 = []
        
        # 1. 提取已有对接码的 uid 集合
        ydj_uids = {d['uid'] for d in ydj_list}
        
        # 2. 获取候选项目列表
        get_project_list = self.get_project_uid(config['search_sid'], config['notAdd_hd'])
        
        # 3. 将已对接的和候选的合并（按 uid 去重）
        all_projects_dict = {d['uid']: d for d in ydj_list}
        for d in get_project_list:
            if d['uid'] not in all_projects_dict:
                all_projects_dict[d['uid']] = d
                
        # 4. 【核心改动】多级排序逻辑：
        #   - 权重 1: float(x['yhj'])           -> 价格越低越靠前
        #   - 权重 2: 0 if is_docked else 1      -> 同价格下，已对接的(0)排在未对接的(1)前面
        #   - 权重 3: str(x['uid'])              -> 同价格且状态相同下，按 UID 固定排序，保证结果稳定
        project_list = sorted(
            all_projects_dict.values(),
            key=lambda x: (
                float(x['yhj']), 
                0 if x['uid'] in ydj_uids else 1, 
                str(x['uid'])
            )
        )
        
        # 5. 遍历挑选
        for d in project_list:
            # 如果没对接过，执行添加
            if d['uid'] not in ydj_uids:
                print(f"添加对接码：{d['mc']}----{d['uid']}（{d['zxky']}，价格:{d['yhj']}）")
                self.add_uid(d['uid'])
                ydj_uids.add(d['uid'])
            
            zxky = int(d['zxky'].split(':')[-1])
            ydjsl += 1
            kysl += zxky
            list1.append(d)
            all_ydj.append(d)
            
            if ydjsl >= config['ydjsl'] and kysl >= config['kysl']:
                break
          
        # 6. 删除多余/被淘汰的对接码
        selected_uids = {d['uid'] for d in list1}
        for d in ydj_list:
            if d['uid'] not in selected_uids:
                print(f"删除多余/高价{d['mc']}对接码")
                self.del_uid(d['uid'])
                

        # 主线程                    
    def main(self, config):
        print(f"{'-'*40}")
        print(f"{config['project_name']}：")
        if config['zddj'] == "0":
            print("自动对接已关闭")
            return
        
        var = self.get_ydj(config['sid'])
        project_ydj = self.update_ydj(var)
        if len(project_ydj) > 0:
            project_ydj = self.check_hd(project_ydj, config['notAdd_hd'])
        
        if config['zddj'] == "1":
            self.zddj_1(project_ydj, config)
        elif config['zddj'] == "2":
            self.zddj_2(project_ydj, config)
            
           
if __name__ == '__main__':
    haozhu = HaoZhu(cookie)
    haozhu.getSummary(haozhu.token)
    all_ydj = []
    
    for d in hz_config['data']:
        haozhu.main(d)
    
    haozhu.process_and_print(all_ydj) # 打印已对接的对接码
    print(f"总请求数量：{request_count}")
