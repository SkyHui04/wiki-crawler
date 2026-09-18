from pydantic import BaseModel
from typing import Literal, Annotated

type LatticeIndexType = Literal["Exact", "FTS"]


class LatticeIndex:
    index_type: LatticeIndexType

    def __init__(self, index_type: LatticeIndexType = "Exact"):
        self.index_type = index_type


class BaseNode(BaseModel):
    id: Annotated[str, LatticeIndex("Exact")]

    @classmethod
    def get_node_type(cls) -> str:
        return cls.__name__

    @classmethod
    def get_node_labels(cls) -> list[str]:
        return [c.__name__ for c in cls.__mro__ if c not in BaseNode.__mro__]

    @classmethod
    def get_fields(cls) -> list[str]:
        return list(cls.model_fields.keys()) + list(cls.model_computed_fields.keys())

    @classmethod
    def get_indexed_fields(cls) -> dict[str, LatticeIndexType]:
        indexed_properties = {}

        for field_name, field_info in cls.model_fields.items():
            for metadata in field_info.metadata:
                if isinstance(metadata, LatticeIndex):
                    indexed_properties[field_name] = metadata.index_type

        # TODO: index computed fields

        return indexed_properties


class BaseEdge(BaseModel):
    id: Annotated[str, LatticeIndex("Exact")]

    @classmethod
    def get_edge_type(cls) -> str:
        return cls.__name__

    @classmethod
    def get_fields(cls) -> list[str]:
        return list(cls.model_fields.keys()) + list(cls.model_computed_fields.keys())

    @classmethod
    def get_indexed_fields(cls) -> dict[str, LatticeIndexType]:
        indexed_properties = {}

        for field_name, field_info in cls.model_fields.items():
            for metadata in field_info.metadata:
                if isinstance(metadata, LatticeIndex):
                    indexed_properties[field_name] = metadata.index_type

        return indexed_properties
