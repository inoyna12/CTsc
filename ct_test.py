from tools.githubFile import GithubFile

def jlyh():
    gh_jlyh = GithubFile("吉利银河/jlyh.json")
    gh_ap150 = GithubFile("吉利银河/ap150.json")
    new_list = []
    for i in gh_jlyh.lst:
        if int(i['availablePoints']) >= 150:
            dct = {
                'phone': i['phone'],
                'password': i['password'],
                'availablePoints': i['availablePoints']
            }
            new_list.append(dct)
    lst = sorted(new_list, key=lambda x: int(x['availablePoints']), reverse=True)
    print(len(lst))
    gh_ap150.update(lst)
    
def jlqc():
    gh_jlqc = GithubFile("吉利汽车/jlqc.json")
    gh_ap150 = GithubFile("吉利汽车/ap150.json")
    new_list = []
    for i in gh_jlqc.lst:
        if float(i['availablePoint']) >= 150:
            dct = {
                'phone': i['phone'],
                'password': i['password'],
                'availablePoint': i['availablePoint']
            }
            new_list.append(dct)
    lst = sorted(new_list, key=lambda x: float(x['availablePoint']), reverse=True)
    print(len(lst))
    gh_ap150.update(lst)


jlyh()
jlqc()
