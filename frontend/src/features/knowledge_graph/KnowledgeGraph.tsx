
import { useState, useEffect } from 'react';
import { GraphCanvas } from 'reagraph';
import type { GraphData } from '../../types/graph_data';
import { convertGraphSchema } from '../../utils/graph_schema_convertor';
import { getGraph } from '../../services/graph';


const KNOWLEDGE_GRAPH_UPDATE_INTERVAL = 500;

export default function KnowledgeGraph() {
    const [graphData, setGraphData] = useState<GraphData>();

    useEffect(() => {
        const intervalId = setInterval(() => {
            getGraph().then(response => {
                if (response.result == "success") {
                    setGraphData(convertGraphSchema(response.data.graph));
                }
            })
        }, KNOWLEDGE_GRAPH_UPDATE_INTERVAL);

        return () => clearInterval(intervalId)
    }, []);

    return (
        graphData ? (
            <div style={{height: 400, width: 800, position: "relative"}}>
                <GraphCanvas
                    nodes={graphData.nodes}
                    edges={graphData.edges}
                    collapsedNodeIds={graphData.collapsedNodeIds}
                />
            </div>
        ) : (
            <span>Loading graph...</span>
        )
    )
}

