
import type { GraphSchema, NodeSchema, EdgeSchema } from "../types/api/graph";
import type { GraphData, NodeData, EdgeData } from "../types/graph_data";

export function convertNodeSchema(node: NodeSchema): NodeData {
    return {
        id: node.id,
        title: node.title || undefined,
        label: node.label || undefined
    }
}

export function convertEdgeSchema(edge: EdgeSchema): EdgeData {
    return {
        id: edge.id,
        url: edge.url,
        source: edge.source,
        target: edge.target,
        label: edge.label || undefined
    }
}

export function convertGraphSchema(graph: GraphSchema): GraphData {
    return {
        nodes: graph.nodes.map(convertNodeSchema),
        edges: graph.edges.map(convertEdgeSchema),
        collapsedNodeIds: graph.collapsedNodeIds
    }
}
