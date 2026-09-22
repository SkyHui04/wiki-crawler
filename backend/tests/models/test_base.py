import pytest
from app.models.base import LatticeIndexableModel, LatticeIndex, LatticeIndexType
from pydantic import computed_field, Field
from typing import Annotated


class DummyLatticeIndexableModel(LatticeIndexableModel):
    regular_field: str
    indexed_field_1: Annotated[str, LatticeIndex("Exact")]
    indexed_field_2: str = Field(json_schema_extra={"lattice_index": "Exact"})

    @computed_field
    @property
    def regular_computed_field(self) -> str:
        return self.regular_field[::-1]

    @computed_field(
        json_schema_extra={"lattice_index": "Exact"},
    )
    @property
    def indexed_computed_field(self) -> str:
        return self.indexed_field_1[::-1]


class DoublyIndexedModel(LatticeIndexableModel):
    # illegal behaviour
    doubly_indexes_field: Annotated[str, LatticeIndex("FTS")] = Field(
        json_schema_extra={"lattice_index": "Exact"}
    )


class InvalidFieldPropertyModel(LatticeIndexableModel):
    # illegal behaviour
    invalid_property_field: str = Field(json_schema_extra={"lattice_index": "foobar"})


def test_indexable_model_get_fields():
    expected = [
        "regular_field",
        "indexed_field_1",
        "indexed_field_2",
        "regular_computed_field",
        "indexed_computed_field",
    ]
    actual = DummyLatticeIndexableModel.get_fields()

    assert sorted(expected) == sorted(actual)


def test_indexable_model_get_indexed_fields():
    expected = [
        "indexed_field_1",
        "indexed_field_2",
        "indexed_computed_field",
    ]
    actual = DummyLatticeIndexableModel.get_indexed_fields()

    assert sorted(expected) == sorted(actual)


def test_doubly_indexed_fields():
    with pytest.raises(ValueError):
        DoublyIndexedModel.get_indexed_fields()


def test_invalid_property_fields():
    with pytest.raises(ValueError):
        InvalidFieldPropertyModel.get_indexed_fields()
