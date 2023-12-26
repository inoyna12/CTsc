'''
cron: 10 0 * * *
new Env('nzqc重置');
'''

import json,random

filepath = "/ql/data/env/nzqc.json"
with open(filepath, "r") as f:
    data = json.load(f)
    
for i in data:
    i["sign"] = False
    i['share'] = 0
    
random.shuffle(data)  
with open(filepath, "w") as f:
    json.dump(data, f)    
    
print(len(data))
