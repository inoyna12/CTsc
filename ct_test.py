'''
cron: 0 0 * * *
new Env('测试脚本');
'''
import json
filepath = "/ql/data/env/jlqc.json"
with open(filepath, 'r') as f:
    atAll_list = json.load(f)

for i, at_dict in enumerate(atAll_list):
    if at_dict['phone'] == '19941326235':
        del atAll_list[i]
        break
        
with open(filepath, 'w') as f:
    json.dump(atAll_list, f, indent=2)
