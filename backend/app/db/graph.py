from pydantic import BaseModel
from app.models.base import BaseNode, BaseEdge
from app.db.client import get_db_client
from typing import Any
from latticedb import Transaction
import json


def create_node(txn: Transaction, node: BaseNode) -> int:
    labels: list[str] = node.get_node_labels()

    if not labels:
        raise RuntimeError(
            f"Invalid class {node.__class__.__name__}. Make sure the class inherits `BaseNode`."
        )

    properties = node.model_dump(exclude_computed_fields=False)

    db_node = txn.create_node(labels=labels, properties=properties)

    return db_node.id


def create_edge(txn: Transaction, edge: BaseEdge, from_id: int, to_id: int) -> int:
    db_edge = txn.create_edge(
        from_id,
        to_id,
        edge.get_edge_type(),
        properties=edge.model_dump(exclude_computed_fields=False),
    )

    return db_edge.id


def replace_node(txn: Transaction, node_id: int, node: BaseNode) -> int:
    labels: list[str] = node.get_node_labels()

    if not labels:
        raise RuntimeError(
            f"Invalid class {node.__class__.__name__}. Make sure the class inherits `BaseNode`."
        )

    db_old_node = txn.get_node(node_id=node_id)
    if db_old_node is None:
        raise RuntimeError(f"Node [{node_id}] does not exist.")

    is_child_class = all([label in labels for label in db_old_node.labels])
    if not is_child_class:
        raise RuntimeError(
            f"{node.__class__.__name__} is not a child class of node with labels: {db_old_node.labels}"
        )

    extra_labels = [label for label in labels if label not in db_old_node.labels]

    if extra_labels:
        txn.query(
            "MATCH (n) WHERE id(n) = $id SET n:" + ":".join(extra_labels),
            parameters={"id": node_id},
        )

    new_properties = node.model_dump(exclude_computed_fields=False)

    for key, value in new_properties.items():
        txn.set_property(node_id, key, value)

    return node_id


MAX_ROWS_PER_QUERY = 1024


def _format_properties(properties: dict[str, Any] | None) -> str:
    if properties:
        return (
            "{"
            + ", ".join([f"{k}: {json.dumps(v)}" for k, v in properties.items()])
            + "}"
        )
    else:
        return ""


def db_read_dict(
    txn: Transaction, query: str, parameters: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    query_result = txn.query(cypher=query, parameters=parameters)

    result: list[dict[str, Any]] = []

    for _ in range(MAX_ROWS_PER_QUERY):
        row = query_result.fetchone()
        if row is None:
            break
        result.append(row)

    return result


def db_read_model[T: BaseModel](
    txn: Transaction, cls: type[T], query: str, parameters: dict[str, Any] | None = None
) -> list[T]:
    query_result = txn.query(cypher=query, parameters=parameters)

    result: list[T] = []

    for _ in range(MAX_ROWS_PER_QUERY):
        row = query_result.fetchone()
        if row is None:
            break
        result.append(cls.model_validate(row))

    return result


def find_nodes_by_properties[T: BaseNode](
    txn: Transaction, cls: type[T], properties: dict[str, Any]
) -> list[T]:
    returned = ", ".join([f"n.{field} AS {field}" for field in cls.get_fields()])
    query = f"MATCH (n:{cls.get_node_type()} {_format_properties(properties)}) RETURN {returned}"
    return db_read_model(txn, cls, query)


def find_node_ids_by_properties[T: BaseNode](
    txn: Transaction, cls: type[T], properties: dict[str, Any]
) -> list[int]:
    query = f"MATCH (n:{cls.get_node_type()} {_format_properties(properties)}) RETURN id(n) AS id"
    return [int(row["id"]) for row in db_read_dict(txn, query)]


def find_edges_by_properties[T: BaseEdge, A: BaseNode, B: BaseNode](
    txn: Transaction,
    edge_cls: type[T],
    from_cls: type[A],
    to_cls: type[B],
    properties: dict[str, Any],
) -> list[T]:
    returned = ", ".join([f"e.{field} AS {field}" for field in edge_cls.get_fields()])
    query = f"MATCH (a:{from_cls.get_node_type()})-[e:{edge_cls.get_edge_type()} {_format_properties(properties)}]->(b:{to_cls.get_node_type()}) RETURN {returned}"
    return db_read_model(txn, edge_cls, query)


class DBEdgeId(BaseModel):
    edge_id: int
    from_id: int
    to_id: int


def find_edge_ids_by_properties[T: BaseEdge, A: BaseNode, B: BaseNode](
    txn: Transaction,
    edge_cls: type[T],
    from_cls: type[A],
    to_cls: type[B],
    edge_properties: dict[str, Any] | None = None,
    from_properties: dict[str, Any] | None = None,
    to_properties: dict[str, Any] | None = None,
) -> list[DBEdgeId]:
    query = f"MATCH (a:{from_cls.get_node_type()} {_format_properties(from_properties)})-[e:{edge_cls.get_edge_type()} {_format_properties(edge_properties)}]->(b:{to_cls.get_node_type()} {_format_properties(to_properties)}) RETURN id(e) AS edge_id, id(a) AS from_id, id(b) AS to_id"
    return [DBEdgeId.model_validate(row) for row in db_read_dict(txn, query)]


def get_all_node_ids[N: BaseNode](txn: Transaction, node_cls: type[N]) -> list[int]:
    return txn.get_nodes_by_label(node_cls.get_node_type())


def get_all_edge_ids[E: BaseEdge](
    txn: Transaction, edge_cls: type[E], node_ids: list[int]
) -> list[DBEdgeId]:
    edges_by_id: dict[int, DBEdgeId] = {}

    for node_id in node_ids:
        incoming_edges = [
            edge.id
            for edge in txn.get_incoming_edges_by_type(
                node_id, edge_cls.get_edge_type()
            )
        ]
        outgoing_edges = [
            edge.id
            for edge in txn.get_outgoing_edges_by_type(
                node_id, edge_cls.get_edge_type()
            )
        ]

        for edge_id in incoming_edges:
            edges_by_id[edge_id] = edges_by_id.get(
                edge_id, DBEdgeId(edge_id=edge_id, from_id=-1, to_id=-1)
            )
            edges_by_id[edge_id].to_id = node_id

        for edge_id in outgoing_edges:
            edges_by_id[edge_id] = edges_by_id.get(
                edge_id, DBEdgeId(edge_id=edge_id, from_id=-1, to_id=-1)
            )
            edges_by_id[edge_id].from_id = node_id

    return [
        edge_id
        for edge_id in edges_by_id.values()
        if edge_id.from_id != -1 and edge_id.to_id != -1
    ]


def get_node_properties_dict[N: BaseNode](
    txn: Transaction, node_cls: type[N], node_id: int
) -> dict[str, Any]:
    returned = ", ".join([f"n.{field} AS {field}" for field in node_cls.get_fields()])
    query = f"MATCH (n) WHERE id(n) = $id RETURN {returned}"
    results = db_read_dict(txn, query, {"id": node_id})
    return results[0]


def get_node_properties[N: BaseNode](
    txn: Transaction, node_cls: type[N], node_id: int
) -> N:
    returned = ", ".join([f"n.{field} AS {field}" for field in node_cls.get_fields()])
    query = f"MATCH (n) WHERE id(n) = $id RETURN {returned}"
    results = db_read_model(txn, node_cls, query, {"id": node_id})
    return results[0]


def get_edge_properties_dict[E: BaseEdge](
    txn: Transaction, edge_cls: type[E], edge_id: int
) -> dict[str, Any]:
    returned = ", ".join([f"e.{field} AS {field}" for field in edge_cls.get_fields()])
    query = f"MATCH (a)-[e]->(b) WHERE id(e) = $id RETURN {returned}"
    results = db_read_dict(txn, query, {"id": edge_id})
    return results[0]


def get_edge_properties[E: BaseEdge](
    txn: Transaction, edge_cls: type[E], edge_id: int
) -> E:
    returned = ", ".join([f"e.{field} AS {field}" for field in edge_cls.get_fields()])
    query = f"MATCH (a)-[e]->(b) WHERE id(e) = $id RETURN {returned}"
    results = db_read_model(txn, edge_cls, query, {"id": edge_id})
    return results[0]
