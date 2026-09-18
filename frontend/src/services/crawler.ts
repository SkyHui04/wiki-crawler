import type { CrawlerStatusResponse, CrawlerStartRequest } from '../types/api/crawler';
import type { BackendResponse } from '../types/backend_response';
import { backendGet, backendPost } from "./server"
import type { CrawlerConfig } from '../types/crawler_controller';

export async function startCrawler(config: CrawlerConfig): Promise<BackendResponse<CrawlerStatusResponse>> {
    const response = await backendPost<CrawlerStartRequest, CrawlerStatusResponse>(
        "/v1/crawler/start",
        {
            batch_size: config.batch_size,
            num_threads: config.num_threads
        }
    )
    return response;
}

export async function stopCrawler(): Promise<BackendResponse<CrawlerStatusResponse>> {
    const response = await backendPost<undefined, CrawlerStatusResponse>(
        "/v1/crawler/stop"
    )
    return response;
}

export async function getCrawlerStatus(): Promise<BackendResponse<CrawlerStatusResponse>> {
    const response = await backendGet<undefined, CrawlerStatusResponse>(
        "/v1/crawler/status"
    )
    return response;
}
