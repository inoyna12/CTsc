import requests
import re,time
from tools.tool import rts, randomSleep
from tools.githubFile import GithubFile

share_true = {}
share_false = {}


gh_jlyh = GithubFile('吉利银河/jlyh.json')

def yezi(phone):
    url = "http://az.yezi56.com:90/api/get_mobile"
    payload = {
      'token': f"hsgxkGEB3O0cOlPPMcKOPV25gJVvMf 4rUEayVlar 60BM6cQ26p045npF89dlpXTHVRuOcbKoh8A/N/pyxadcQOaJd8VWiZIF0/yjCyKZ/QS84IvcxMwSS45/0R4n7yfwpMlqOx6gBNnrJMGSxAErM8Y9qDjtS9qOZbvkVvXx0=;project_id=720526;project_type=1;operator=0;loop=1;phone_num={phone}"
    }
    headers = {
      'User-Agent': "Mozilla/5.0 (Linux; Android 12; 22081212C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.146 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/29.333334)",
      'Accept': "application/json, text/plain, */*",
      'Accept-Encoding': "gzip, deflate",
      'Origin': "http://af.sqhyw.net:90",
      'X-Requested-With': "yezi.com",
      'Referer': "http://af.sqhyw.net:90/",
      'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    response = requests.post(url, data=payload, headers=headers).text
    pattern = r'\[(\d+----[A-Z0-9]+)\]'
    match = re.search(pattern, response)
    if match:
        code = match.group(1)
        return code
    else:
        print("未找到匹配内容")
        return False
    
for index, i in enumerate(gh_jlyh.lst, start=1):
    print(f"{index}：{i['phone']}")
    if i['sharestatus'] == 'true':
        project_id = yezi(i['phone'])
        if project_id:
            if project_id in share_true:
                share_true[project_id] += 1
            else:
                share_true[project_id] = 1
    else:
        project_id = yezi(i['phone'])
        if project_id:
            if project_id in share_false:
                share_false[project_id] += 1
            else:
                share_false[project_id] = 1
    print(f"可分享：{share_true}")
    print(f"不可分享：{share_false}")
    time.sleep(5)
