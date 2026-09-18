import {useState, useEffect} from "react"
import type { CrawlerStatus } from "../../../types/api/crawler"
import type { CrawlerConfig } from "../../../types/crawler_controller";
import { startCrawler, stopCrawler, getCrawlerStatus } from "../../../services/crawler"


const CHECK_CRAWLER_STATUS_INTERVAL = 500;


export default function CrawlerController() {
    const [crawlerStatus, setCrawlerStatus] = useState<CrawlerStatus>("Idle");
    const [crawlerBatchSize, setCrawlerBatchSize] = useState<number>(8);
    const [crawlerNumThreads, setCrawlerNumThreads] = useState<number>(8);

    let allowModifyConfig: boolean;
    if (crawlerStatus == "Running") {
        allowModifyConfig = false;
    } else {
        allowModifyConfig = true;
    }

    const crawlerConfig: CrawlerConfig = {
        batch_size: crawlerBatchSize,
        num_threads: crawlerNumThreads
    }

    const onClickStart = () => {
        startCrawler(crawlerConfig).then(response => {
            if (response.result == "success") {
                setCrawlerStatus(response.data.status);
            }
        })
    }

    const onClickStop = () => {
        stopCrawler().then(response => {
            if (response.result == "success") {
                setCrawlerStatus(response.data.status);
            }
        })
    }

    useEffect(() => {
        const intervalId = setInterval(() => {
            getCrawlerStatus().then(response => {
                if (response.result == "success") {
                    setCrawlerStatus(response.data.status);
                }
            })
        }, CHECK_CRAWLER_STATUS_INTERVAL);

        return () => clearInterval(intervalId)
    }, []);

    return (
        <div>
            <h1>
                Crawler Controller
            </h1>
            <p>
                Status: {crawlerStatus}
            </p>
            <section>
                <label>
                    Batch Size
                </label>
                <input
                    type="number"
                    value={crawlerBatchSize}
                    onChange={e => setCrawlerBatchSize(Number.parseInt(e.target.value))}
                    min={1}
                    max={16}
                    step={1}
                    disabled={!allowModifyConfig}
                />
            </section>
            <section>
                <label>
                    Number of Threads
                </label>
                <input
                    type="number"
                    value={crawlerNumThreads}
                    onChange={e => setCrawlerNumThreads(Number.parseInt(e.target.value))}
                    min={1}
                    max={16}
                    step={1}
                    disabled={!allowModifyConfig}
                />
            </section>
            <button
                onClick={onClickStart}
                disabled={crawlerStatus != "Idle"}
            >
                Start
            </button>
            <button
                onClick={onClickStop}
                disabled={crawlerStatus != "Running"}
            >
                Stop
            </button>
        </div>
    )
}
