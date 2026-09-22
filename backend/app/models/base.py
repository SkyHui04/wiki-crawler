from abc import ABC
from typing import Annotated, Literal

from pydantic import BaseModel

type LatticeIndexType = Literal["Exact", "FTS"]

_LATTICE_INDEX_TYPES: tuple[LatticeIndexType, ...] = ("Exact", "FTS")


class LatticeIndex:
    index_type: LatticeIndexType

    def __init__(self, index_type: LatticeIndexType = "Exact"):
        self.index_type = index_type


class LatticeIndexableModel(ABC, BaseModel):
    """
    Fields in LatticeIndexableModel can be automatically extracted for
    indexing in Lattice Database by the following methods: \n
    1.  Annotate the field with :class:`~app.models.base.LatticeIndex` using :class:`~typing.Annotated`.
    This does not work for computed fields.
    ```python
    indexed_field: Annotated[str, LatticeIndex("Exact")]
    ```
    2.  Add `"lattice_index"` to `json_schema_extra`.
    ```python
    @computed_field(
        json_schema_extra={"lattice_index": "Exact"},
    )
    @property
    def indexed_computed_field(self) -> str:
        ...
    ```
    """

    @classmethod
    def get_fields(cls) -> list[str]:
        return list(cls.model_fields.keys()) + list(cls.model_computed_fields.keys())

    @classmethod
    def get_indexed_fields(cls) -> dict[str, LatticeIndexType]:
        indexed_properties: dict[str, LatticeIndexType] = {}

        for field_name, field_info in cls.model_fields.items():
            for metadata in field_info.metadata:
                if isinstance(metadata, LatticeIndex):
                    indexed_properties[field_name] = metadata.index_type

        for field_name, field_info in (
            cls.model_fields | cls.model_computed_fields
        ).items():
            if field_info.json_schema_extra is not None and not callable(
                field_info.json_schema_extra
            ):
                field_properties = field_info.json_schema_extra
                if "lattice_index" not in field_properties:
                    continue

                if field_properties["lattice_index"] in _LATTICE_INDEX_TYPES:
                    if field_name in indexed_properties:
                        raise ValueError(
                            f"The field {field_name} is set as Lattice Index in more than one place."
                        )
                    else:
                        indexed_properties[field_name] = field_properties[
                            "lattice_index"
                        ]
                else:
                    raise ValueError(
                        f"The lattice_index property of field {field_name} must take "
                        f"the following values: {_LATTICE_INDEX_TYPES}\n"
                        f"Instead, this is found: {field_properties["lattice_index"]}"
                    )

        return indexed_properties


class BaseNode(LatticeIndexableModel):
    id: Annotated[str, LatticeIndex("Exact")]

    @classmethod
    def get_node_type(cls) -> str:
        return cls.__name__

    @classmethod
    def get_node_labels(cls) -> list[str]:
        return [c.__name__ for c in cls.__mro__ if c not in BaseNode.__mro__]


class BaseEdge(LatticeIndexableModel):
    id: Annotated[str, LatticeIndex("Exact")]

    @classmethod
    def get_edge_type(cls) -> str:
        return cls.__name__
