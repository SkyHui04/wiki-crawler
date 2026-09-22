from fastapi import APIRouter

from app.schemas.crawler import CrawlerStartRequest, CrawlerStatusResponse
from app.services.crawler import Crawler, get_crawler

router = APIRouter(prefix="/v1/crawler", tags=["crawler"])


def _get_crawler_status_response(crawler: Crawler) -> CrawlerStatusResponse:
    return CrawlerStatusResponse(
        status=crawler.status,
        batch_size=crawler.batch_size,
        num_threads=crawler.num_threads,
    )


@router.post("/start")
async def start_crawler(request: CrawlerStartRequest) -> CrawlerStatusResponse:
    if get_crawler().status == "Running":
        raise RuntimeError("Crawler is already Running.")

    get_crawler().batch_size = request.batch_size
    get_crawler().num_threads = request.num_threads
    get_crawler().start()

    return _get_crawler_status_response(crawler=get_crawler())


@router.post("/stop")
async def stop_crawler() -> CrawlerStatusResponse:
    get_crawler().stop()
    return _get_crawler_status_response(crawler=get_crawler())


@router.get("/status")
async def crawler_status() -> CrawlerStatusResponse:
    return _get_crawler_status_response(crawler=get_crawler())
