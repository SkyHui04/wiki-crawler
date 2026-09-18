/* tslint:disable */
/* eslint-disable */
/**
/* This file was automatically generated from pydantic models by running pydantic2ts.
/* Do not modify it by hand - just update the pydantic models and then re-run the script
*/

export type CrawlerStatus = "Idle" | "Running" | "Stopped";

export interface CrawlerStartRequest {
  batch_size: number;
  num_threads: number;
}
export interface CrawlerStatusResponse {
  status: CrawlerStatus;
  batch_size: number;
  num_threads: number;
}
