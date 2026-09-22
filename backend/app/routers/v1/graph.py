from fastapi import APIRouter

from app.db.client import get_db_client
from app.schemas.graph import GraphResponse
from app.services.crud import fetch_graph

router = APIRouter(prefix="/v1/graph", tags=["graph"])


@router.get("/get_all")
async def get_graph() -> GraphResponse:
    with get_db_client().read() as txn:
        graph = fetch_graph(txn)

    return GraphResponse(graph=graph)
