'''
cron: 36 0 * * *
new Env('nzqc重置');
'''

import json,random

filepath = "/ql/data/env/nzqc.json"
with open(filepath, "r") as f:
    data = json.load(f)
    
for i in data:
    i["sign"] = False
    i['share'] = 0
    i['comment'] = 0
   
with open(filepath, "w") as f:
    json.dump(data, f)    
    
print(len(data))
#random.shuffle(account_list)
