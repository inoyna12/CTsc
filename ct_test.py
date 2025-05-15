import json

filepath = "/ql/data/env/jlqc.json"
with open(filepath, 'r') as f:
    my_list = json.load(f)

del_accounts = ['18501632796','19222699057','18501720352','18772451564','19222698894','19222698125','19270773419']
