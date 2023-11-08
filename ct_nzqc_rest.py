'''
cron: 16 0 * * *
new Env('nzqc测试');
'''

import json,random

filepath = "/ql/data/env/nzqc.json"
with open(filepath, "r") as f:
    data = json.load(f)
print(len(data))

for info in data:
    del info['comment']
    del info['reserve']
    del info['reserve2']

with open(filepath, "w") as f:
    json.dump(data, f)
