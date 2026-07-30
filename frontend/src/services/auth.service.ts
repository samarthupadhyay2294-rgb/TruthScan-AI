import api from "./api";
import type {
  LoginCredentials,
  RegisterData,
  User,
} from "@/types";

interface BackendUser {
  id: number;
  email: string;
  username: string;
  full_name: string | null;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
}

interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  user: User;
}

function mapUser(data: BackendUser): User {
  return {
    id: String(data.id),
    email: data.email,
    name: data.full_name || data.username,
    role: data.is_admin ? "admin" : "user",
    created_at: data.created_at,
    updated_at: data.created_at,
  };
}

async function fetchCurrentUser(): Promise<User> {
  const data = await api.get<BackendUser>("/auth/me");
  return mapUser(data);
}

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const tokenData = await api.post<TokenResponse>("/auth/login", credentials);
    localStorage.setItem("truthlens_access_token", tokenData.access_token);

    const user = await fetchCurrentUser();
    return {
      access_token: tokenData.access_token,
      refresh_token: tokenData.access_token,
      user,
    };
  },

  async register(data: RegisterData): Promise<AuthResponse> {
    await api.post<BackendUser>("/auth/signup", {
      email: data.email,
      username: data.username,
      password: data.password,
      full_name: data.name,
    });

    return this.login({ email: data.email, password: data.password });
  },

  async getCurrentUser(): Promise<User> {
    return fetchCurrentUser();
  },

  async logout(): Promise<void> {
    return Promise.resolve();
  },

  async forgotPassword(email: string): Promise<{ message: string }> {
    return api.post<{ message: string }>("/auth/forgot-password", { email });
  },

  async resetPassword(token: string, newPassword: string): Promise<{ message: string }> {
    return api.post<{ message: string }>("/auth/reset-password", {
      token,
      new_password: newPassword,
    });
  },
};
