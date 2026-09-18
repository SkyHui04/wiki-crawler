from app.types.wiki_objects import WikiArticle, WikiArticleLink
from app.models.nodes import (
    WikiArticleNode,
    WikiArticleExploredNode,
)
from app.models.edges import WikiHeadLinkEdge
from app.schemas.graph import GraphSchema, NodeSchema, EdgeSchema
from app.db.graph import (
    create_node,
    create_edge,
    find_edge_ids_by_properties,
    find_node_ids_by_properties,
    replace_node,
    get_all_node_ids,
    get_all_edge_ids,
    get_edge_properties,
    get_node_properties,
    get_node_properties_dict,
)
from latticedb import Transaction
import uuid


def get_explored_node_id_by_link(txn: Transaction, url: str | None) -> int | None:
    if url is None:
        return None

    head_link_edge_ids = find_edge_ids_by_properties(
        txn=txn,
        edge_cls=WikiHeadLinkEdge,
        from_cls=WikiArticleExploredNode,
        to_cls=WikiArticleExploredNode,
        edge_properties={"url": url},
    )

    if len(head_link_edge_ids) > 0:
        return head_link_edge_ids[0].to_id
    else:
        return None


def get_explored_node_id_by_article(
    txn: Transaction, article: WikiArticle
) -> int | None:
    article_node_ids = find_node_ids_by_properties(
        txn=txn, cls=WikiArticleExploredNode, properties={"title": article.title}
    )

    if len(article_node_ids) > 0:
        return article_node_ids[0]
    else:
        return None


def save_article(
    txn: Transaction, url: WikiArticleLink | None, article: WikiArticle
) -> bool:
    """precondition: url not explored + article not explored + from_title article is explored"""

    to_article_node = WikiArticleExploredNode(id=str(uuid.uuid4()), title=article.title)
    to_article_node_id: int

    if url is None:
        to_article_node_id = create_node(txn, to_article_node)

    else:
        to_article_node_id = find_edge_ids_by_properties(
            txn=txn,
            edge_cls=WikiHeadLinkEdge,
            from_cls=WikiArticleExploredNode,
            to_cls=WikiArticleNode,
            edge_properties={"url": url.link},
            from_properties={"title": url.from_title},
        )[0].to_id
        replace_node(txn=txn, node_id=to_article_node_id, node=to_article_node)

    if article.head_link is not None:
        discovered_link = WikiHeadLinkEdge(
            id=str(uuid.uuid4()), url=article.head_link.link
        )
        new_article_node = WikiArticleNode(id=str(uuid.uuid4()))
        new_article_node_id = create_node(txn, new_article_node)
        create_edge(
            txn=txn,
            edge=discovered_link,
            from_id=to_article_node_id,
            to_id=new_article_node_id,
        )

    return True


def rewire_unexplored_node(
    txn: Transaction, url: WikiArticleLink, explored_node_id: int
) -> bool:
    """Replace the unexplored node (created by the given url) with an explored article."""

    edge_id = find_edge_ids_by_properties(
        txn=txn,
        edge_cls=WikiHeadLinkEdge,
        from_cls=WikiArticleExploredNode,
        to_cls=WikiArticleNode,
        edge_properties={"url": url.link},
        from_properties={"title": url.from_title},
    )[0]
    from_article_node_id = edge_id.from_id
    unexplored_node_id = edge_id.to_id

    print(f"[DEBUG] {from_article_node_id}, {unexplored_node_id}, {explored_node_id}")

    link_edge = WikiHeadLinkEdge(id=str(uuid.uuid4()), url=url.link)

    create_edge(
        txn=txn, edge=link_edge, from_id=from_article_node_id, to_id=explored_node_id
    )
    txn.delete_node(node_id=unexplored_node_id)

    return True


def fetch_graph(txn: Transaction) -> GraphSchema:
    node_ids = get_all_node_ids(txn=txn, node_cls=WikiArticleNode)
    edge_ids = get_all_edge_ids(txn=txn, edge_cls=WikiHeadLinkEdge, node_ids=node_ids)

    node_models: list[WikiArticleNode] = []

    for node_id in node_ids:
        node_properties = get_node_properties_dict(
            txn=txn, node_cls=WikiArticleNode, node_id=node_id
        )

        status = str(node_properties["status"])
        if status == "Explored":
            node_models.append(
                get_node_properties(
                    txn=txn, node_cls=WikiArticleExploredNode, node_id=node_id
                )
            )
        else:
            node_models.append(
                get_node_properties(txn=txn, node_cls=WikiArticleNode, node_id=node_id)
            )

    edge_models: list[tuple[WikiHeadLinkEdge, int, int]] = [
        (
            get_edge_properties(
                txn=txn, edge_cls=WikiHeadLinkEdge, edge_id=edge_id.edge_id
            ),
            edge_id.from_id,
            edge_id.to_id,
        )
        for edge_id in edge_ids
    ]

    nodes = [
        (
            NodeSchema(id=node_model.id, title=node_model.title, label=node_model.title)
            if isinstance(node_model, WikiArticleExploredNode)
            else NodeSchema(id=node_model.id, title=None, label=None)
        )
        for node_model in node_models
    ]

    edges = [
        EdgeSchema(
            id=edge_model.id,
            url=edge_model.url,
            source=str(txn.get_property(from_id, "id")),
            target=str(txn.get_property(to_id, "id")),
            label=edge_model.url,
        )
        for (edge_model, from_id, to_id) in edge_models
    ]

    return GraphSchema(nodes=nodes, edges=edges, collapsedNodeIds=[])
