from typing import Literal
from pydantic import BaseModel

type CrawlerStatus = Literal[
    "Idle",
    "Running",
    "Stopped",
]


class CrawlerStartRequest(BaseModel):
    batch_size: int
    num_threads: int


class CrawlerStatusResponse(BaseModel):
    status: CrawlerStatus
    batch_size: int
    num_threads: int
