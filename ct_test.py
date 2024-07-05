'''
cron: 0 0 * * *
new Env('测试脚本');
'''
import json
filepath = "/ql/data/env/jlqc.json"
with open(filepath, 'r') as f:
    atAll_list = json.load(f)

for at_dict in atAll_list:
    if at_dict['phone'] == '19941326235':
        del atAll_list[at_dict]
        break
        
with open(filepath, 'w') as f:
    json.dump(atAll_list, f, indent=2)
