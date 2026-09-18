from app.models.base import BaseEdge, LatticeIndex
from typing import Annotated


class WikiHeadLinkEdge(BaseEdge):
    url: Annotated[str, LatticeIndex]
