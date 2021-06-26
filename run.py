import os

from Github.GH import GH

if __name__ == "__main__":
    github_user = os.environ["GITHUB_USER"]
    github_repo = os.environ["GITHUB_REPO"]
    github_token = os.environ["GITHUB_TOKEN"]
    expire_time = os.environ["EXPIRE_TIME"]

    gh = GH(github_user, github_repo, github_token, expire_time)
    gh.run()
