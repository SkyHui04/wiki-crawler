from pydantic import BaseModel
from typing import Optional


class NodeSchema(BaseModel):
    id: str
    title: str | None
    label: str | None


class EdgeSchema(BaseModel):
    id: str
    url: str
    source: str
    target: str
    label: str | None


class GraphSchema(BaseModel):
    nodes: list[NodeSchema]
    edges: list[EdgeSchema]
    collapsedNodeIds: list[str]


class GraphResponse(BaseModel):
    graph: GraphSchema
