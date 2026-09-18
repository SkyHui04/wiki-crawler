import {BACKEND_PORT} from "../core/config"
import type {BackendResponse} from "../types/backend_response"
import axios, { type AxiosResponse } from 'axios';

function getApiUrl(path: string): string {
    return `http://127.0.0.1:${BACKEND_PORT}${path}`
}

export async function backendGet<RequestT, ResponseT>(endpoint: string, params?: RequestT): Promise<BackendResponse<ResponseT>> {
    const response = await axios.get<ResponseT, AxiosResponse<ResponseT>, object, RequestT>(
        getApiUrl(endpoint),
        {
            params: params
        }
    )
    if (response.status == 200) {
        return {
            result: "success",
            httpStatus: response.status,
            data: response.data
        }
    } else {
        return {
            result: "error",
            httpStatus: response.status,
            errorMessage: response.statusText
        }
    }
}

export async function backendPost<RequestT, ResponseT>(endpoint: string, payload?: RequestT): Promise<BackendResponse<ResponseT>> {
    const response = await axios.post<ResponseT, AxiosResponse<ResponseT>, RequestT, object>(
        getApiUrl(endpoint),
        payload
    )
    if (response.status == 200) {
        return {
            result: "success",
            httpStatus: response.status,
            data: response.data
        }
    } else {
        return {
            result: "error",
            httpStatus: response.status,
            errorMessage: response.statusText
        }
    }
}
