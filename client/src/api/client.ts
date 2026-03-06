/**
 * Axios HTTP client — single configured instance for all REST calls.
 * Base URL is read from Expo's extra config so it's never hardcoded.
 */
import axios from "axios";
import Constants from "expo-constants";

const BASE_URL: string =
  (Constants.expoConfig?.extra?.apiBaseUrl as string) ?? "http://localhost:8000";

export const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 15_000,
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Centralised error surface — screens receive typed errors, not raw axios
    const message: string =
      error?.response?.data?.detail ?? error?.message ?? "Unknown API error";
    return Promise.reject(new Error(message));
  }
);
