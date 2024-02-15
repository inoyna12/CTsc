from github import Github

class GithubFileManager:
    def __init__(self, access_token):
        self.github = Github(access_token)

    def get_repo(self, repo_name):
        try:
            repo = self.github.get_repo(repo_name)
            return repo
        except Exception as e:
            print(f"Error accessing repository: {e}")
            return None

    def get_file_content(self, repo_name, file_path, branch="main"):
        repo = self.get_repo(repo_name)
        if repo is not None:
            try:
                file_content = repo.get_contents(file_path, ref=branch)
                return file_content.decoded_content.decode()
            except Exception as e:
                print(f"Error getting file content: {e}")
        return None

    def update_file_content(self, repo_name, file_path, content, commit_message, branch="main"):
        repo = self.get_repo(repo_name)
        if repo is not None:
            try:
                file_sha = repo.get_contents(file_path, ref=branch).sha
                repo.update_file(file_path, commit_message, content, file_sha, branch=branch)
                print(f"File {file_path} updated successfully on repo {repo_name}")
                return True
            except Exception as e:
                print(f"Error updating file content: {e}")
        return False
