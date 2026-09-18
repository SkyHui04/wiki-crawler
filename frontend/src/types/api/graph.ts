/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export interface EdgeSchema {
  id: string;
  url: string;
  source: string;
  target: string;
  label: string | null;
}
export interface GraphResponse {
  graph: GraphSchema;
}
export interface GraphSchema {
  nodes: NodeSchema[];
  edges: EdgeSchema[];
  collapsedNodeIds: string[];
}
export interface NodeSchema {
  id: string;
  title: string | null;
  label: string | null;
}
