from typing import Annotated, Literal

from pydantic import computed_field

from app.models.base import BaseNode, LatticeIndex

type WikiArticleNodeStatus = Literal["Unexplored", "Explored"]


class WikiArticleNode(BaseNode):
    @computed_field
    @property
    def status(self) -> WikiArticleNodeStatus:
        return "Unexplored"


class WikiArticleExploredNode(WikiArticleNode):
    title: Annotated[str, LatticeIndex]

    @computed_field
    @property
    def status(self) -> WikiArticleNodeStatus:
        return "Explored"
