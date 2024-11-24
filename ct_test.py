import json


ql_jlyh_filepath = "/ql/data/env/jlyh.json"
with open(ql_jlyh_filepath, 'r') as f:
    all_data = json.load(f)
    
for i in all_data:
    i['signdate'] = ''
    
with open(ql_jlyh_filepath, 'w') as f:
     json.dump(all_data, f, indent=2)
