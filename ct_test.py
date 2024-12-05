from tools.githubFile import GithubFile
import json

ql_path = "/ql/data/env/fy.json"

create_list = []
create_dict = {
    'phone': '15050425338',
    'token': 'user:token:app:1705601:evos-6ebd45ebd06523e3bc4609cd94af52ac',
    'networkState': 'WIFI',
    'osVersion': '12',
    'model': '22081212C',
    'brand': 'Xiaomi'
}
create_list.append(create_dict)
with open(ql_path, 'w') as f:
    json.dump(create_list, f, indent=2)
    
gh_fy = GithubFile("福域/fy.json")
gh_fy.update(create_list)
