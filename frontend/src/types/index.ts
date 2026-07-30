export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  role: "user" | "admin";
  created_at: string;
  updated_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  name: string;
  email: string;
  username: string;
  password: string;
  confirmPassword?: string;
}

export interface PredictionResult {
  id: string;
  text: string;
  label: "REAL" | "FAKE" | "UNCERTAIN";
  confidence: number;
  real_score: number;
  fake_score: number;
  indicators: PredictionIndicator[];
  source_url?: string;
  created_at: string;
  user_id?: string;
}

export interface PredictionIndicator {
  name: string;
  value: number;
  description: string;
  severity: "low" | "medium" | "high";
}

export interface PredictionRequest {
  text: string;
  source_url?: string;
  include_indicators?: boolean;
}

export interface HistoryItem {
  id: string;
  text_preview: string;
  label: "REAL" | "FAKE" | "UNCERTAIN";
  confidence: number;
  created_at: string;
}

export interface HistoryFilters {
  label?: "REAL" | "FAKE" | "UNCERTAIN";
  start_date?: string;
  end_date?: string;
  search?: string;
  page?: number;
  limit?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

export interface DashboardStats {
  total_analyses: number;
  fake_detected: number;
  real_verified: number;
  average_confidence: number;
  analyses_today: number;
  analyses_this_week: number;
  fake_percentage: number;
  real_percentage: number;
}

export interface ChartDataPoint {
  date: string;
  real: number;
  fake: number;
  total: number;
}

export interface Report {
  id: string;
  title: string;
  prediction_id: string;
  summary: string;
  content: ReportSection[];
  generated_at: string;
  format: "pdf" | "html" | "json";
}

export interface ReportSection {
  title: string;
  content: string;
  type: "text" | "chart" | "table" | "indicator";
  data?: Record<string, unknown>;
}

export interface ApiError {
  detail: string;
  status_code: number;
}

export type Theme = "light" | "dark" | "system";

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface PredictionState {
  currentPrediction: PredictionResult | null;
  isAnalyzing: boolean;
  error: string | null;
  history: HistoryItem[];
}
