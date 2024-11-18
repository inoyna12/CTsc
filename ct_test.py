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
    gh_ap100 = GithubFile("吉利汽车/ap100.json")
    gh_ap150 = GithubFile("吉利汽车/ap150.json")
    ap100_list = []
    ap150_list = []
    for i in gh_jlqc.lst:
        dct = {
            'phone': i['phone'],
            'password': i['password'],
            'availablePoint': i['availablePoint']
        }
        if float(i['availablePoint']) >= 100:
            ap100_list.append(dct)
        if float(i['availablePoint']) >= 150:
            ap150_list.append(dct)

    ap100lst = sorted(ap100_list, key=lambda x: float(x['availablePoint']), reverse=True)
    print(len(ap100lst))
    ap150lst = sorted(ap150_list, key=lambda x: float(x['availablePoint']), reverse=True)
    print(len(ap150lst))
    
    gh_ap100.update(ap100lst)
    gh_ap150.update(ap150lst)


jlyh()
jlqc()
