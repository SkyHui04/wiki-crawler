export interface BaseBackendResponse {
    httpStatus: number
}

export interface SuccessfulBackendResponse<T> extends BaseBackendResponse {
    result: "success"
    data: T
}

export interface ErrorBackendResponse extends BaseBackendResponse {
    result: "error"
    errorMessage: string
}

export type BackendResponse<T> = SuccessfulBackendResponse<T> | ErrorBackendResponse;
