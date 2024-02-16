'''
cron: 0 0 * * *
new Env('测试脚本');
'''
import json
filepath = "/ql/data/env/dyxw.json"
with open(filepath, 'r', encoding='utf-8') as file:
    data_list = json.load(file)

new_key_value_pairs = {'ref_code': None, 'taskStatus': False}

for d in data_list:
    d.update(new_key_value_pairs)
    
with open(filepath, 'w', encoding='utf-8') as file:
    json.dump(data_list, file, indent=2)
