'''
cron: */6 * * * *
new Env('番茄小说开宝箱');
'''

import requests
import json

def baoxiang():
    url = 'https://i.snssdk.com/luckycat/novel/v1/task/done/treasure_task?_request_from=web&iid=3521071482679901&device_id=2230266336385260&ac=5g&channel=wandoujia&aid=1967&app_name=novelapp&version_code=325&version_name=3.2.5.32&device_platform=android&ssmix=a&device_type=22081212C&device_brand=Redmi&language=zh&os_api=31&os_version=12&openudid=d381a0046ef00d14&manifest_version_code=325&resolution=1080*2197&dpi=424&update_version_code=32532&_rticket=1683320854950&_rticket=1683320854954&gender=1&comment_tag_c=3&vip_state=0&category_style=1&oaid=fc723391358dedbf&cdid=b45d8622-62ec-4063-8fab-2859218b51f8&act_token=yL9DCgFC5PTVl7B35BqsdURm2uQky0b9hWd5wrwp6MXmcyeTy12STLen8-EB3eAFJTr-YuCYScJzhSsUma2zZw&act_hash=19809d690e291b449b9aa9d51d241aca&cookie_base=TcLOx7lo4kw1oPURPEdgulfKkGvg_l9qJLx2JBAqcsRzMVZMiqK6pGYsp6Bkbig5FBsC1_j00SpPh2UscmQpsDzDlUWWxORQVIImVQW0f4E&cookie_data=PFc4FQN94WCBXUz7zJ6o-g&luckycat_version_name=3.0.0-alpha.32-blank&luckycat_version_code=300032&status_bar_height=33&ip=10.1.10.1&new_bookshelf=true'
    headers = {
        'Host': 'i.snssdk.com',
        'Connection': 'keep-alive',
        'Cookie': 'excgd=20230506; store-region=cn-js; install_id=3521071482679901; ttreq=1$3ff02c1109405a343382d0919f3d2a09abb34d1d; MONITOR_WEB_ID=2230266336385260; passport_csrf_token=31892c209e5c14124a247bc66fb16770; passport_csrf_token_default=31892c209e5c14124a247bc66fb16770; d_ticket=0330b6ed935de8f4fcf0dc86a45442390ed4b; odin_tt=b05622bcb58dbde50308bd2a30ebd5ad391a1b0b8a8a8aad4695b88f9d87c079a0cd31fc4225c30835288b16786daa90142571996680acf55d9e8b37c2a5ecea4f35ab2cb4a988a9c24eeeb34217af6e; n_mh=TRBbPoctpE56JXGmFIF_5NGP7T4HQem8pchz2XPHBPw; sid_guard=3431f598aae3f1a226aef85e40028d4f%7C1683320737%7C5184000%7CTue%2C+04-Jul-2023+21%3A05%3A37+GMT; uid_tt=8b02ece29ff2e162f94565f4333422b2; uid_tt_ss=8b02ece29ff2e162f94565f4333422b2; sid_tt=3431f598aae3f1a226aef85e40028d4f; sessionid=3431f598aae3f1a226aef85e40028d4f; sessionid_ss=3431f598aae3f1a226aef85e40028d4f; store-region-src=uid',
        'X-SS-QUERIES': 'dGMFEAAAHUPRTG%2BloBlJl%2B9Wim8BMfLET5CxLCCoiSDBr6L8YqmfT2H%2FRc0J1VrOjLmiUV5Lw64SZLU%2B%2FCyFfqGuLRFqydrZj6m5nZ5YqwQUTfQjonFePFws%2BQPjUaWV6JJ6GknDw3u%2FdDOUfSUvyYM9G4F%2FwZn6p%2FaF67oWGQKfuOAYreBG7XRG2dylnIowLME%2F3XhRlIMmNE4KQdCtV78boWZmiZTaFJ8U8hmR6Q9xVgiHFPAFPYMlwEMLUaij7Nrywax9',
        'X-SS-REQ-TICKET': '1683320854956',
        'gender': '1',
        'sdk-version': '2',
        'X-Tt-Token': '003431f598aae3f1a226aef85e40028d4f03ae8d2fc7ad4846344dfd24f729eb0c5a1ce814343f78633d8d009a5ebddb3d870f51cce522323b1f3ac606d4846d8e8f1f644185dafe381789600afe16b66d24269908d3a22da91cc8129951fd778499d-1.0.1',
        'passport-sdk-version': '18',
        'Content-Type': 'application/json; charset=utf-8',
        'X-SS-STUB': '99914B932BD37A50B983C5E7C90AE93B',
        'x-tt-trace-id': '00-edbddb360d7ec6a58bc18ec6337c07af-edbddb360d7ec6a5-01',
        'User-Agent': 'com.dragon.read/325 (Linux; U; Android 12; zh_CN; 22081212C; Build/SKQ1.220303.001; Cronet/TTNetVersion:4df3ca9d 2019-11-25)',
        'X-Khronos': '1683320854',
        'X-Gorgon': '0408306b0001d1486f65071b872acda3476273fcc50da22bf537',
    }
    data = '{}'
    response = requests.post(url=url, headers=headers, data=data)
    result = response.json()
    print(result)
baoxiang()

    
