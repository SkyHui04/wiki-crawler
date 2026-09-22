import asyncio
import traceback
from threading import Lock

from app.db.client import get_db_client
from app.schemas.crawler import CrawlerStatus
from app.services.crud import (
    get_explored_node_id_by_article,
    get_explored_node_id_by_link,
    rewire_unexplored_node,
    save_article,
)
from app.services.transform import extract_article
from app.services.wiki_query import ConcurrentQueryManager
from app.types.wiki_objects import WikiArticle, WikiArticleLink
from app.utils.atomic import AtomicCounter

CRAWL_TIMEOUT = 15.0


class Crawler:
    write_lock: Lock
    enabled: asyncio.Event
    shutdown: asyncio.Event
    task: asyncio.Task | None
    _batch_size: int = 16
    _num_threads: int = 16
    _crawl_request_counter: AtomicCounter = AtomicCounter(0)

    def __init__(self):
        self.write_lock = Lock()
        self.enabled = asyncio.Event()
        self.shutdown = asyncio.Event()
        self.task: asyncio.Task | None = None

    async def run(self):
        while not self.shutdown.is_set():
            await self.enabled.wait()
            to_be_explored: list[WikiArticleLink | None] = [None] * self._batch_size

            with ConcurrentQueryManager(num_threads=self._num_threads) as query_manager:
                while self.enabled.is_set() and not self.shutdown.is_set():
                    try:
                        # TODO: prioritise exploring existing leaves
                        to_be_explored = await asyncio.gather(
                            *[
                                self.crawl_once(query_manager, link)
                                for link in to_be_explored
                            ]
                        )
                    except (asyncio.CancelledError, KeyboardInterrupt):
                        raise
                    except RuntimeError as exc:
                        print(f"Crawler error: {exc}")
                        traceback.print_exc()

    async def crawl_once(
        self, query_manager: ConcurrentQueryManager, link: WikiArticleLink | None
    ) -> WikiArticleLink | None:
        async with asyncio.timeout(CRAWL_TIMEOUT):
            if self.shutdown.is_set() or not self.enabled.is_set():
                return None

            explored_node_id: int | None = None
            article: WikiArticle | None = None

            with get_db_client().read() as txn:
                crawl_request_id = self._crawl_request_counter.increment()

                url = link.link if link is not None else None
                print(f"[{crawl_request_id}] Exploring {url}")

                explored_node_id = get_explored_node_id_by_link(txn, url)
                if explored_node_id is not None:
                    print(f"[{crawl_request_id}] Link already explored: {url}")

            if explored_node_id is None:
                raw_html = await query_manager.assign_and_run(url)
                if raw_html is None:
                    print(f"[{crawl_request_id}] Fetch failed: {url}")
                    return None

                article = extract_article(raw_html)
                print(
                    f"[{crawl_request_id}] Article successfully extracted: {article.title}"
                )
                print(
                    f"[{crawl_request_id}] {len(article.content_links)} content links found"
                )

                with self.write_lock, get_db_client().write() as txn:
                    explored_node_id = get_explored_node_id_by_article(txn, article)
                    if explored_node_id is None:
                        save_article(txn, link, article)
                    else:
                        print(
                            f"[{crawl_request_id}] Article already explored: {article.title}"
                        )

                    txn.commit()

                print(
                    f"[{crawl_request_id}] Article successfully saved: {article.title}"
                )

            if explored_node_id is not None and link is not None:
                with self.write_lock, get_db_client().write() as txn:
                    rewire_unexplored_node(
                        txn=txn, url=link, explored_node_id=explored_node_id
                    )
                    txn.commit()

            return article.head_link if article else None

    def start(self):
        self.enabled.set()

    def stop(self):
        self.enabled.clear()

    async def close(self):
        self.shutdown.set()
        self.enabled.set()
        if self.task:
            await self.task

    @property
    def status(self) -> CrawlerStatus:
        if self.shutdown.is_set():
            return "Stopped"
        if self.enabled.is_set():
            return "Running"
        return "Idle"

    @property
    def batch_size(self) -> int:
        return self._batch_size

    @property
    def num_threads(self) -> int:
        return self._num_threads

    @batch_size.setter
    def batch_size(self, value: int) -> None:
        if self.status == "Running":
            raise RuntimeError(f"Illegal modification when status is {self.status}.")
        else:
            self._batch_size = value

    @num_threads.setter
    def num_threads(self, value: int) -> None:
        if self.status == "Running":
            raise RuntimeError(f"Illegal modification when status is {self.status}.")
        else:
            self._num_threads = value


_crawler = Crawler()


def get_crawler() -> Crawler:
    return _crawler
