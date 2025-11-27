/**
 * API client configuration with TanStack Query hooks.
 *
 * This module provides a centralized API client and React Query hooks
 * for all backend endpoints.
 */

import { QueryClient } from "@tanstack/react-query";

/**
 * TanStack Query client configuration.
 */
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
    },
    mutations: {
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
    },
  },
});

/**
 * Get API base URL from environment variables.
 */
export function getApiBaseURL(): string {
  return import.meta.env.VITE_API_URL || "http://localhost:8000";
}

/**
 * Generic API request function with error handling.
 */
export async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const baseURL = getApiBaseURL();
  const url = `${baseURL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`API request failed: ${endpoint}`, error);
    throw error;
  }
}

/**
 * Upload file with multipart/form-data.
 */
export async function uploadFile<T>(
  endpoint: string,
  file: File,
  additionalData?: Record<string, string>
): Promise<T> {
  const baseURL = getApiBaseURL();
  const url = `${baseURL}${endpoint}`;

  const formData = new FormData();
  formData.append("file", file);

  if (additionalData) {
    Object.entries(additionalData).forEach(([key, value]) => {
      formData.append(key, value);
    });
  }

  try {
    const response = await fetch(url, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`File upload failed: ${endpoint}`, error);
    throw error;
  }
}

/**
 * Health check API call.
 */
export async function healthCheck(): Promise<{ status: string; version: string; timestamp: string }> {
  return apiRequest<{ status: string; version: string; timestamp: string }>("/api/v1/health");
}

