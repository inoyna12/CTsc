'''
cron: 2 0 * * *
new Env('吉利汽车更新账号');
'''
import json
import os,random
from utils.github_file_manager import GithubFileManager

ql_filepath = "/ql/data/env/jlqc.json"

access_token = os.getenv('github_token')
repo_name = "inoyna12/updateTeam"
branch = "master"
gh_filepath = "吉利汽车/test.json"
#new_content = json.dumps([])
commit_message = f"Update {gh_filepath}"


fileManager = GithubFileManager(access_token)
with open(ql_filepath, 'r') as f:
    accountAll_list = json.load(f)
# with open(ql_filepath, 'w') as f:
    # json.dump(accountAll_list, f, indent=2)
fileManager.update_file_content(repo_name, gh_filepath, accountAll_list, commit_message, branch)
