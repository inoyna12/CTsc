'''
{"code":0,"message":"ok","data":{"list":[{"code":"76980-MNKOZACSVE","projectId":"76980","projectName":"海马云","price":"0.330","available":40,"operators":["虚拟运营商"],"provinces":["吉林","四川","安徽","广东","河南","辽宁","重庆","黑龙江"],"prefixes":["171","170","167","165"],"segmentType":"虚拟号段","contact":"未留","lastUsedAt":"2026-10-22T11:25:02Z","status":"joined"}],"total":1,"page":1,"size":20}}
        
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
token = os.environ["haozhutoken"]
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
    def __init__(self, token):
        self.token = token
        self.host = 'api.veeto.cn'
        self.host2 = 'api.haozhuma.cn'
        self.use_quantity = 0
        self.use_money = Decimal('0')
            
    def headers(self):
        headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36 Edg/155.0.0.0",
        'Accept': "application/json, text/plain, */*",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'sec-ch-ua-platform': "\"Windows\"",
        'Authorization': f"Bearer {self.token}",
        'sec-ch-ua': "\"Microsoft Edge\";v=\"155\", \"Chromium\";v=\"155\", \"Not(A:Brand\";v=\"24\"",
        'sec-ch-ua-mobile': "?0",
        'Origin': "https://h5.haozhuma.cn",
        'Sec-Fetch-Site': "cross-site",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://h5.haozhuma.cn/",
        'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
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
    def getSummary(self):
        url = f'https://{self.host}/v1/me'
        headers = self.headers()
        result = rts(url, headers=headers)
        if result['code'] == 0:
            print(f"当前余额：{result['data']['balance']}")
        else:
            print(result)
            exit()
    
    # 查询加入的对接码
    def get_ydj(self, projectId, page=1) -> list[dict]:
        data = []
        headers = self.headers()
        for i in range(page):
            url = f'https://{self.host}/v1/bindings?keyword={projectId}&page={i+1}&size=20'
            result = rts(url, headers=headers)
            if result['code'] == 0:
                data.extend(result['data']['list'])  #追加到data列表末尾中
        return data

    # 更新已对接的对接码
    def update_ydj(self, ydj):
        data = []
        for i in ydj:
            if i['status'] == 'joined' and i['available'] > 0:
                data.append(i)
                continue
            #if ky == 0:
            if i['status'] == 'joined' and ky == 0:
                print(f"删除对接码：{i['projectName']}----{i['code']}（{i['available']}，价格:{i['price']}）")
                self.del_uid(i['code'])
        return data

    # 删除对接码
    def del_uid(self, code):
        url = f'https://{self.host}/v1/bindings/batch'
        codes = []
        codes.append(code)
        payload = {
        "action": "delete",
        "codes": codes
        }
        headers = self.headers()
        result = rts(url, method='POST', data=json.dumps(payload), headers=headers)
        print(f"删除对接码：{uids}")
        print(result['message'])
    
    # 搜索项目公开对接码
    def get_project_uid(self, sid, not_hd_list):
        url = f'https://{self.host}/v1/projects/{sid}/public-codes'
        headers = self.headers()
        result = rts(url, headers=headers)
        if result['code'] != 0 or result['code'] is None:
            print(url)
            print(result)
            exit()
        new_data = []
        for item in result['data']:
            ky = item['available']
            hd_list = item['prefixes']
            if ky <= 50: #可用数量不足跳过
                continue
            if set(hd_list).issubset(not_hd_list): # 判断对接码的列表号段元素是否全部存在于not_hd_list列表中，如果全部存在则跳过
                continue
            if set(item['provinces']).issubset(notAdd_sheng): # 判断对接码的列表地区元素是否全部存在于notAdd_sheng列表中，如果全部存在则跳过
                continue
            if item['contact'] in notAdd_lxfs: # item的卡商用户名存在于RemoveLxfs中，则运行
                continue
            new_data.append(item)
        sorted_data = sorted(new_data, key=lambda x: float(x['price']))
        return sorted_data
    
    # 加入对接码
    def add_uid(self, code):
        url = f'https://{self.host}/api.php?type=4&djm={djm}'
        codes = []
        codes.append(code)
        payload = {
          "codes": codes
        }
        headers = self.headers()
        result = rts(url, method='POST', data=json.dumps(payload), headers=headers)
        if result['code'] == 0:
            for i in result['data']['results']:
                print(f"{i['code']}：{i['message']}")
           
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
            zxky = d['available']
            ydjsl += 1
            kysl += zxky
            all_ydj.append(d)
            if ydjsl >= config['ydjsl'] and kysl >= config['kysl']:
                return
                
        uid_config_list = self.get_project_uid(config['search_sid'], config['notAdd_hd'])
        for dd in uid_config_list:
            print(f"添加对接码：{dd['projectName']}----{dd['code']}（{dd['available']}，价格:{dd['price']}）")
            self.add_uid(dd['uid'])
            zxky = dd['available']
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
            name = item['projectName']
            if name not in grouped_data:
                grouped_data[name] = []
            grouped_data[name].append(item)

        # 2. 准备排序用的列表
        # 结构：[ {'name': 名称, 'items': [项目列表], 'max_price': 该组最高价}, ... ]
        sorted_groups = []

        for name, items in grouped_data.items():
            # 先对组内的项目按价格降序排序
            items.sort(key=lambda x: float(x['price']), reverse=True)
            
            # 获取该组中最高的一个价格，用于组与组之间的排序
            max_price = float(items[0]['price']) if items else 0
            
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
                uid = item['code']
                zxky = item['available']
                price = item['price']
                
                # 打印单行详情
                print(f"{uid}（{zxky}，价格:{price}）")
                
                # 提取"可用"后面的数字进行累加
                total_available += zxky

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
        ydj_uids = {d['code'] for d in ydj_list}
        
        # 2. 获取候选项目列表
        get_project_list = self.get_project_uid(config['search_sid'], config['notAdd_hd'])
        
        # 3. 将已对接的和候选的合并（按 uid 去重）
        all_projects_dict = {d['code']: d for d in ydj_list}
        for d in get_project_list:
            if d['code'] not in all_projects_dict:
                all_projects_dict[d['code']] = d
                
        # 4. 【核心改动】多级排序逻辑：
        #   - 权重 1: float(x['yhj'])           -> 价格越低越靠前
        #   - 权重 2: 0 if is_docked else 1      -> 同价格下，已对接的(0)排在未对接的(1)前面
        #   - 权重 3: str(x['uid'])              -> 同价格且状态相同下，按 UID 固定排序，保证结果稳定
        project_list = sorted(
            all_projects_dict.values(),
            key=lambda x: (
                float(x['price']), 
                0 if x['code'] in ydj_uids else 1, 
                str(x['code'])
            )
        )
        
        # 5. 遍历挑选
        for d in project_list:
            # 如果没对接过，执行添加
            if d['code'] not in ydj_uids:
                print(f"添加对接码：{d['projectName']}----{d['code']}（{d['available']}，价格:{d['price']}）")
                self.add_uid(d['code'])
                ydj_uids.add(d['code'])
            
            zxky = d['available']
            ydjsl += 1
            kysl += zxky
            list1.append(d)
            all_ydj.append(d)
            
            if ydjsl >= config['ydjsl'] and kysl >= config['kysl']:
                break
          
        # 6. 删除多余/被淘汰的对接码
        selected_uids = {d['code'] for d in list1}
        for d in ydj_list:
            if d['code'] not in selected_uids:
                print(f"删除多余/高价{d['projectName']}对接码")
                self.del_uid(d['code'])
                

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
            pass
           # project_ydj = self.check_hd(project_ydj, config['notAdd_hd'])
        
        if config['zddj'] == "1":
            self.zddj_1(project_ydj, config)
        elif config['zddj'] == "2":
            self.zddj_2(project_ydj, config)
            
           
if __name__ == '__main__':
    haozhu = HaoZhu(token)
    haozhu.getSummary()
    all_ydj = []
    
    for d in hz_config['data']:
        haozhu.main(d)
    
    haozhu.process_and_print(all_ydj) # 打印已对接的对接码
    print(f"总请求数量：{request_count}")
