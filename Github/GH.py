import datetime

from p_tqdm import p_map

from .utils import getUrl, deleteUrl, convertTime, uniqWorkflowList


class GH:
    def __init__(self, github_user, github_repo, github_token, expire_time):
        self.github_user = github_user
        self.github_repo = github_repo

        self.headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        self.getExpireTime(expire_time)

    def run(self):
        print(
            "--------------------------- Start to clean workflows ---------------------------"
        )

        workflows, workflows_count = self.listWorkflows()
        if workflows_count != None:
            print(f"Total workflows number: {workflows_count}")

            clean_ids = []

            for wf in workflows:
                created_time = convertTime(wf["created_at"])
                if created_time < self.expired_timestamp:
                    clean_ids.append(wf["id"])

            print("Plan to delete {} workflows\n".format(len(clean_ids)))
            result = p_map(self.deleteRun, clean_ids)
            result = list(filter(None, result))
            if result:
                print("\nFailed to delete these workflow runs:")
                for r in result:
                    print("* ID {}: {}".format(r[0], r[1]))

        print(
            "----------------------------------- Finished -----------------------------------"
        )

    def listWorkflows(self):
        workflows_url = "https://api.github.com/repos/{}/{}/actions/runs?status=completed&per_page=100".format(
            self.github_user, self.github_repo
        )
        result = getUrl(workflows_url, headers=self.headers).json()

        workflows_count = result.get("total_count")
        if workflows_count == None:
            print("Error: please check your configuration!")
            return None, None
        else:
            page_num = workflows_count // 100 + 1

            workflows = result["workflow_runs"]
            for i in range(2, page_num + 1):
                workflows_page_url = f"{workflows_url}&page={i}"
                workflows_this_page = getUrl(
                    workflows_page_url, headers=self.headers
                ).json()["workflow_runs"]
                workflows += workflows_this_page

            workflows = uniqWorkflowList(workflows)

            return workflows, workflows_count

    def deleteRun(self, run_id):
        delete_url = "https://api.github.com/repos/{}/{}/actions/runs/{}".format(
            self.github_user, self.github_repo, run_id
        )

        result = deleteUrl(delete_url, headers=self.headers)

        if result.status_code == 204:
            return None
        else:
            return run_id, result.text

    def getExpireTime(self, expire_time):
        now_time = datetime.datetime.now(tz=datetime.timezone.utc)
        days = hours = 0
        if expire_time.endswith("y"):
            days = int(expire_time.strip("y")) * 365

        if expire_time.endswith("m"):
            days = int(expire_time.strip("m")) * 30

        if expire_time.endswith("d"):
            days = int(expire_time.strip("d"))

        if expire_time.endswith("h"):
            hours = int(expire_time.strip("h"))

        expired_time = now_time - datetime.timedelta(days=days, hours=hours)
        self.expired_timestamp = datetime.datetime.timestamp(expired_time)
