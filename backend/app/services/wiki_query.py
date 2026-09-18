import requests
from ratelimit import limits, sleep_and_retry
from app.utils.concurrency import ConcurrentTaskManager

_RANDOM_WIKI_URL = "https://en.wikipedia.org/wiki/Special:Random"


@sleep_and_retry
@limits(calls=20, period=6)
def query_wiki_page(url: str | None = None) -> str | None:
    url = url or _RANDOM_WIKI_URL
    headers = {"User-Agent": "WikiCrawler/0.1.0 (CreeperSky91358@gmail.com)"}
    response = requests.request("GET", url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(response.reason)
        return None


class ConcurrentQueryManager(ConcurrentTaskManager[str | None, str | None]):
    @staticmethod
    def run_sync(parameter: str | None) -> str | None:
        url: str | None = parameter
        return query_wiki_page(url)
