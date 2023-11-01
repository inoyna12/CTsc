'''
cron: 10 0 * * *
new Env('jlqc重置');
'''

import json,random

filepath = "/ql/data/env/jlqc.json"
with open(filepath, "r") as f:
    data = json.load(f)

for i in data:
    i["sign"] = False
    i['create'] = False
            
random.shuffle(data)  
with open(filepath, "w") as f:
    json.dump(data, f)    
    
print(len(data))
