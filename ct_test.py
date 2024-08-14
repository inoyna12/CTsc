'''
cron: 2 0 * * *
new Env('吉利汽车更新账号');
'''
import json
import os,random
from github import Github


ql_filepath = "/ql/data/env/jlqc.json"
g = Github(os.getenv('github_token'))
repo = g.get_repo("inoyna12/updateTeam")
file_path_in_repo = "吉利汽车/test.json"
commit_message = 'Added a json file'

with open(ql_filepath, 'r') as file:
    content = file.read()


repo.create_file(file_path_in_repo, commit_message, content)
