from tools.githubFile import GithubFile

gh = GithubFile('test.json')
cre = {"phone": 1}
gh.lst.append(cre)
gh.update(gh.lst)
