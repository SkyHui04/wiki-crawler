from latticedb import Database, LatticeAlreadyExistsError
from app.core.config import LATTICE_DB_PATH
from app.models.base import BaseNode, BaseEdge
import app.models.nodes
import app.models.edges
import inspect

NODE_MODELS: list[type[BaseNode]] = [
    clazz
    for _, clazz in inspect.getmembers(
        app.models.nodes, lambda obj: inspect.isclass(obj) and issubclass(obj, BaseNode)
    )
    if clazz.__module__ == app.models.nodes.__name__
]

EDGE_MODELS: list[type[BaseEdge]] = [
    clazz
    for _, clazz in inspect.getmembers(
        app.models.edges, lambda obj: inspect.isclass(obj) and issubclass(obj, BaseEdge)
    )
    if clazz.__module__ == app.models.edges.__name__
]


def create_indices(db: Database):
    try:
        for NodeModel in NODE_MODELS:
            for field_name, index_type in NodeModel.get_indexed_fields().items():
                match index_type:
                    case "Exact":
                        db.create_node_property_index(
                            NodeModel.get_node_type(), field_name
                        )
                        break
                    case "FTS":
                        db.create_node_fts_index(NodeModel.get_node_type(), field_name)
                        break

        for EdgeModel in EDGE_MODELS:
            for field_name, index_type in EdgeModel.get_indexed_fields().items():
                match index_type:
                    case "Exact":
                        db.create_edge_property_index(
                            EdgeModel.get_edge_type(), field_name
                        )
                        break
                    case "FTS":
                        db.create_edge_fts_index(EdgeModel.get_edge_type(), field_name)
                        break

    except LatticeAlreadyExistsError:
        print("Index already exists.")


_db = Database(LATTICE_DB_PATH, create=True)
_db.open()

create_indices(db=_db)


def get_db_client() -> Database:
    return _db
