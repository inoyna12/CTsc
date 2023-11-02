'''
cron: 16 0 * * *
new Env('jlqc测试');
'''

import json,random

filepath = "/ql/data/env/jlqc.json"
with open(filepath, "r") as f:
    data = json.load(f)
print(len(data))

unique_data = []
seen_mobiles = set()

for item in data:
    mobile = item["mobile"]
    if mobile not in seen_mobiles:
        unique_data.append(item)
        seen_mobiles.add(mobile)
    else:
        print(mobile)

print(len(unique_data))

with open(filepath, "w") as f:
    json.dump(unique_data, f)
