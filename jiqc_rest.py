'''
cron: 16 0 * * *
new Env('jlqc测试');
'''

import json,random

filepath = "/ql/data/env/jlqc.json"
with open(filepath, "r") as f:
    data = json.load(f)
print(len(data))

for info in data:
    del info['create']
    del info['reserve']
    del info['reserve2']
    info['signDay'] = None

with open(filepath, "w") as f:
    json.dump(data, f)
