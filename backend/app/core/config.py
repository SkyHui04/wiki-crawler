from slowapi import Limiter
from slowapi.util import get_remote_address
from pathlib import Path
import os


def _getenv(key: str) -> str:
    result = os.getenv(key)

    if result is None:
        raise RuntimeError("Missing environment variable")

    return result


LATTICE_DB_PATH = Path(__file__).parents[2].resolve() / "data" / "graph.db"
BACKEND_PORT = int(os.getenv("BACKEND_PORT") or "5000")
FRONTEND_POST = int(os.getenv("FRONTEND_PORT") or "3000")
RESET_DB_ON_RUN = os.getenv("RESET_DB_ON_RUN", "False").lower() == "true"

_limiter = Limiter(key_func=get_remote_address)


def get_limiter() -> Limiter:
    return _limiter
