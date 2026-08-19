import type { AuthResponse, CareerProfile, ResumeAnalysisResponse, StoredCareerProfileResponse, User } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

type ApiErrorBody = {
  error?: { code?: string; message?: string };
};

async function request<T>(path: string, options: RequestInit = {}, token?: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers
    }
  });

  if (!response.ok) {
    let body: ApiErrorBody = {};
    try {
      body = (await response.json()) as ApiErrorBody;
    } catch {
      body = {};
    }
    throw new Error(body.error?.message ?? `Request failed with status ${response.status}`);
  }

  return (await response.json()) as T;
}

export const api = {
  signup: (body: { full_name: string; email: string; password: string }) =>
    request<AuthResponse>("/api/v1/auth/signup", { method: "POST", body: JSON.stringify(body) }),
  login: (body: { email: string; password: string }) =>
    request<AuthResponse>("/api/v1/auth/login", { method: "POST", body: JSON.stringify(body) }),
  me: (token: string) => request<User>("/api/v1/auth/me", {}, token),
  saveOnboarding: (
    token: string,
    body: {
      career_status: string | null;
      preferred_work_mode: string | null;
      career_goals: string | null;
      resume_creation_requested: boolean;
      career_profile: CareerProfile;
    }
  ) =>
    request<StoredCareerProfileResponse>(
      "/api/v1/onboarding/career-profile",
      { method: "POST", body: JSON.stringify(body) },
      token
    ),
  getMyProfile: (token: string) =>
    request<StoredCareerProfileResponse>("/api/v1/career-profile/me/current", {}, token),
  updateMyProfile: (token: string, career_profile: CareerProfile) =>
    request<StoredCareerProfileResponse>(
      "/api/v1/career-profile/me/current",
      { method: "PUT", body: JSON.stringify({ career_profile }) },
      token
    ),
  analyzeResume: async (token: string, file: File): Promise<ResumeAnalysisResponse> => {
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch(`${API_BASE_URL}/api/v1/resume/analyze`, {
      method: "POST",
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      body: formData,
    });
    if (!response.ok) {
      let body: { error?: { code?: string; message?: string } } = {};
      try { body = await response.json(); } catch { body = {}; }
      throw new Error(body.error?.message ?? `Request failed with status ${response.status}`);
    }
    return (await response.json()) as ResumeAnalysisResponse;
  },
};
