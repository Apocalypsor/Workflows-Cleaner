import datetime

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def getUrl(url: str, headers=None, retry=5, timeout=10):
    retry_strategy = Retry(total=retry, backoff_factor=0.1)

    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    response = http.get(url, headers=headers, timeout=timeout)

    return response


def deleteUrl(url: str, headers=None, retry=5, timeout=10):
    retry_strategy = Retry(total=retry, backoff_factor=0.1)

    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    response = http.delete(url, headers=headers, timeout=timeout)

    return response


def convertTime(time_string):
    """
    time_string: 2021-06-26T07:30:33Z
    """

    datetime_obj = datetime.datetime.strptime(
        time_string, "%Y-%m-%dT%H:%M:%SZ"
    ).replace(tzinfo=datetime.timezone.utc)
    time_stamp = int(datetime_obj.timestamp())
    return time_stamp


def uniqWorkflowList(list):
    result = []
    uniq_hash = set()

    for l in list:
        if l["id"] not in uniq_hash:
            uniq_hash.add(l["id"])
            result.append(l)

    return result
