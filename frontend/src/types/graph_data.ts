
import type { GraphNode, GraphEdge } from "reagraph";

export interface NodeData extends GraphNode {
    title?: string
}

export interface EdgeData extends GraphEdge {
    url?: string
}

export interface GraphData {
  nodes: NodeData[];
  edges: EdgeData[];
  collapsedNodeIds: string[];
}
