from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import get_limiter
from app.core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)
app.state.limiter = get_limiter()
app.add_exception_handler(
    RateLimitExceeded, _rate_limit_exceeded_handler  # type: ignore
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origin_regex=rf"^https?://(localhost|127\.0\.0\.1):{FRONTEND_POST}$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers.v1 import crawler, graph

app.include_router(crawler.router)
app.include_router(graph.router)
