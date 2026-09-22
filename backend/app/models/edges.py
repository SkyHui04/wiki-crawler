from typing import Annotated

from app.models.base import BaseEdge, LatticeIndex


class WikiHeadLinkEdge(BaseEdge):
    url: Annotated[str, LatticeIndex]
