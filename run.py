import os

from Github.GH import GH

if __name__ == "__main__":
    github_repo = os.environ["GITHUB_REPO"]
    github_token = os.environ["GITHUB_TOKEN"]
    expire_time = os.environ["EXPIRE_TIME"]

    print("Clean Workflows for Repo:", f"{github_repo}\n")
    gh = GH(github_repo, github_token, expire_time)
    gh.run()
