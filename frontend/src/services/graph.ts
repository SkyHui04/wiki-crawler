import type { GraphResponse } from '../types/api/graph';
import type { BackendResponse } from '../types/backend_response';
import { backendGet } from "./server"

export async function getGraph(): Promise<BackendResponse<GraphResponse>> {
    const response = await backendGet<undefined, GraphResponse>(
        "/v1/graph/get_all"
    )
    return response;
}
