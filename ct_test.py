import json,datetime
from tools.githubFile import GithubFile

today_date = datetime.datetime.now().strftime("%m-%d")

ql_jlyh_filepath = "/ql/data/env/jlyh.json"
with open(ql_jlyh_filepath, 'r') as f:
    all_data = json.load(f)

index = 0
   
for i in all_data:
    if i['signdate'] == today_date:
        index += 1
    if index > 70:
        i['signdate'] = ''

gh_jlyh = GithubFile('吉利银河/jlyh.json')
gh_jlyh.update(all_data)    
with open(ql_jlyh_filepath, 'w') as f:
     json.dump(all_data, f, indent=2)
