import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.services.crawler import get_crawler
from app.db.client import get_db_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not get_db_client().is_open:
        get_db_client().open()

    get_crawler().task = asyncio.create_task(get_crawler().run())
    yield
    await get_crawler().close()

    if get_db_client().is_open:
        get_db_client().close()
